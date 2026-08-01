#!/usr/bin/env python3
"""
Submit strategy files to XNOQuant and fetch backtest metrics automatically.

Interactive mode: enter one file path at a time, type 'done' to finish.
Batch mode: submit all discovered strategy files (filtered by universe).

Results are saved to: backtest/results_stage_2.csv

Universe handling (safe for a single editor):
  - The script NEVER changes the XNOQuant universe via API.
  - The user must select the universe manually in the editor UI BEFORE submit.
  - `--universe` FILTERS which files are submitted (by cap folder), it is NOT
    an override tag. The universe written to CSV is always derived from the
    file's cap folder (output/stage_2/<cap>/<mode>/<file>.py).
  - Batch mode refuses to submit files from multiple caps in one run.
  - A live batch run requires explicit confirmation of the editor universe.

Config via .env file (create .env in project root):
    XNO_EDITOR_ID=<UUID>
    XNO_TOKEN=<token>

No hardcoded fallbacks — .env is required for LIVE submission only.
--dry-run never touches the network.
"""

import requests
import json
import time
import os
import sys
import csv
import argparse
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from common import format_metrics, load_previous_results

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

CSV_PATH = os.path.join("backtest", "results_stage_2.csv")
WAIT_SECONDS = 10
POLL_TIMEOUT = 90
POLL_INTERVAL = 5

VALID_UNIVERSES = {"VN-SMALL-CAP", "VN-MID-CAP", "VN-LARGE-CAP"}
CAP_TO_UNIVERSE = {
    "vn_small_cap": "VN-SMALL-CAP",
    "vn_mid_cap": "VN-MID-CAP",
    "vn_large_cap": "VN-LARGE-CAP",
}
VALID_MODES = {"time_series", "cross_sectional"}

# Result statuses
STATUS_SIMULATED = "SIMULATED"
STATUS_UPDATE_FAILED = "UPDATE_FAILED"
STATUS_VERIFY_FAILED = "VERIFY_FAILED"
STATUS_SIMULATE_FAILED = "SIMULATE_FAILED"
STATUS_RATE_LIMITED = "RATE_LIMITED"
STATUS_METRICS_TIMEOUT = "METRICS_TIMEOUT"
STATUS_NO_STRATEGY_ID = "NO_STRATEGY_ID"

CSV_FIELDS = [
    "timestamp", "filepath", "filename", "universe", "mode",
    "status", "strategy_id", "cagr", "sharpe", "calmar",
    "max_drawdown", "profit_factor", "error",
]


def require_env():
    """Return (editor_id, token, base_url) or None if missing."""
    editor_id = os.getenv("XNO_EDITOR_ID")
    token = os.getenv("XNO_TOKEN")
    if not editor_id or not token:
        print("[ERROR] Missing XNO_EDITOR_ID or XNO_TOKEN in .env")
        print("  Create .env in project root (see .env.example).")
        return None
    base = f"https://api.xnoquant.io/xalpha-api/v2/editors/{editor_id}"
    return editor_id, token, base


def build_headers(token: str) -> dict:
    return {
        "accept": "application/json",
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
        "origin": "https://alpha.xnoquant.io",
        "referer": "https://alpha.xnoquant.io/",
    }


def get_strategy_id(session, base: str) -> str | None:
    try:
        r = session.get(f"{base}/info")
        if r.status_code == 200:
            data = r.json()
            ids = data.get("data", {}).get("strategy_ids", [])
            return ids[0] if ids else None
    except Exception:
        pass
    return None


def fetch_metrics(session, strategy_id: str) -> dict:
    url = f"https://api.xnoquant.io/xalpha-api/v1/strategies/{strategy_id}/stages/simulate/summary-aggregate"
    try:
        r = session.get(url)
        if r.status_code == 200:
            data = r.json().get("data", {})
            if data:
                return {
                    "cagr": data.get("cagr", 0) or 0,
                    "sharpe": data.get("sharpe", 0) or 0,
                    "calmar": data.get("calmar", 0) or 0,
                    "max_drawdown": data.get("max_drawdown", 0) or 0,
                    "profit_factor": data.get("profit_factor", 0) or 0,
                }
    except Exception:
        pass
    return {}


def wait_for_metrics(session, strategy_id: str, timeout: int = POLL_TIMEOUT) -> dict:
    """Poll simulate summary until metrics are ready or timeout. Returns {} on timeout."""
    elapsed = 0
    while elapsed < timeout:
        metrics = fetch_metrics(session, strategy_id)
        if metrics:
            return metrics
        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL
    return {}


def infer_universe_from_path(fpath: str) -> str:
    """Derive universe from output/stage_2/<cap>/<mode>/<file>.py layout."""
    norm = fpath.replace("\\", "/")
    parts = norm.split("/")
    for i, p in enumerate(parts):
        if p == "stage_2" and i + 1 < len(parts):
            return CAP_TO_UNIVERSE.get(parts[i + 1].lower(), "")
    return ""


def infer_mode_from_path(fpath: str) -> str:
    norm = fpath.replace("\\", "/")
    parts = norm.split("/")
    for i, p in enumerate(parts):
        if p == "stage_2" and i + 1 < len(parts) and i + 2 < len(parts):
            if parts[i + 2] in VALID_MODES:
                return parts[i + 2]
    return ""


def resolve_universe(fpath: str, explicit: str) -> str:
    """Universe always comes from the cap folder. Explicit is a FILTER, not an override.
    Returns '' when unknown — callers must fail closed."""
    return infer_universe_from_path(fpath)


def load_index() -> list:
    """Read output/index.csv as the manifest source of truth. Returns list of dict rows."""
    idx_path = os.path.join(BASE_DIR, "output", "index.csv")
    if not os.path.isfile(idx_path):
        return []
    with open(idx_path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def discover_batch_files() -> list:
    """Discover Round-2 strategy files from the manifest (output/index.csv).
    Only .py files that are BOTH in the manifest and on disk are eligible."""
    files = []
    for row in load_index():
        fp = (row.get("filepath") or "").strip()
        if not fp:
            continue
        rel = os.path.join(BASE_DIR, "output", "stage_2", *fp.split("/"))
        if fp.endswith(".py") and os.path.isfile(rel):
            files.append(rel)
    return sorted(set(files))


def filter_files_by_universe(files: list, universe: str) -> tuple:
    """Return (matching, skipped). Fails closed on unknown universe."""
    if universe not in VALID_UNIVERSES:
        return [], files
    matching, skipped = [], []
    for f in files:
        if infer_universe_from_path(f) == universe:
            matching.append(f)
        else:
            skipped.append(f)
    return matching, skipped


def split_by_universe(files: list) -> dict:
    groups = {}
    for f in files:
        u = infer_universe_from_path(f)
        groups.setdefault(u, []).append(f)
    return groups


def save_to_csv(row: dict):
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    file_exists = os.path.isfile(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def make_row(filepath: str, universe: str, status: str, metrics: dict = None,
             strategy_id: str = "", error: str = "") -> dict:
    metrics = metrics or {}
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "filepath": filepath.replace("\\", "/").split("output/stage_2/")[-1],
        "filename": os.path.basename(filepath),
        "universe": universe,
        "mode": infer_mode_from_path(filepath),
        "status": status,
        "strategy_id": strategy_id,
        "cagr": metrics.get("cagr", ""),
        "sharpe": metrics.get("sharpe", ""),
        "calmar": metrics.get("calmar", ""),
        "max_drawdown": metrics.get("max_drawdown", ""),
        "profit_factor": metrics.get("profit_factor", ""),
        "error": error,
    }


def rel_filepath(filepath: str) -> str:
    """Relative manifest-style filepath (vn_small_cap/time_series/File.py)."""
    return filepath.replace("\\", "/").split("output/stage_2/")[-1]


def run_http_sequence(env, filepath: str, name: str, universe: str, index: int, total: int) -> bool:
    """Live PUT -> verify -> simulate -> poll metrics. Returns True if submit attempt ran."""
    editor_id, token, base = env
    session = requests.Session()
    session.headers.update(build_headers(token))

    with open(filepath, encoding="utf-8") as f:
        code = f.read()

    max_retries = 5
    for attempt in range(1, max_retries + 1):
        r1 = session.put(f"{base}/update", json={"code": code})
        if r1.status_code not in (200, 201, 204):
            is_rate_limit = r1.status_code == 429
            if is_rate_limit and attempt < max_retries:
                print(f"  => Rate limit (PUT), retry in 15s (attempt {attempt}/{max_retries})...")
                time.sleep(15)
                continue
            save_to_csv(make_row(filepath, universe, STATUS_UPDATE_FAILED, error=r1.text[:200]))
            print(f"  PUT: {r1.status_code} [FAIL]  {name} {r1.text[:200]}")
            return False

        r2 = session.post(f"{base}/verify")
        time.sleep(2)
        if r2.status_code not in (200, 201, 204):
            is_rate_limit = r2.status_code == 429
            if is_rate_limit and attempt < max_retries:
                print(f"  => Rate limit (VERIFY), retry in 15s (attempt {attempt}/{max_retries})...")
                time.sleep(15)
                continue
            save_to_csv(make_row(filepath, universe, STATUS_VERIFY_FAILED, error=r2.text[:200]))
            print(f"  PUT: {r1.status_code} | VERIFY: {r2.status_code} [FAIL]  {name} {r2.text[:200]}")
            return False

        r3 = session.post(f"{base}/simulate")
        if r3.status_code not in (200, 201, 204):
            is_rate_limit = r3.status_code == 429
            if is_rate_limit and attempt < max_retries:
                print(f"  => Rate limit (SIMULATE), retry in 15s (attempt {attempt}/{max_retries})...")
                time.sleep(15)
                continue
            save_to_csv(make_row(filepath, universe, STATUS_SIMULATE_FAILED, error=r3.text[:200]))
            print(f"  PUT: {r1.status_code} | VERIFY: {r2.status_code} | SIMULATE: {r3.status_code} [FAIL]  {name} {r3.text[:200]}")
            return False

        print(f"  PUT: {r1.status_code} | VERIFY: {r2.status_code} | SIMULATE: {r3.status_code} [OK]  {name}")
        break

    print(f"  Poll metrics (timeout {POLL_TIMEOUT}s)...")
    strategy_id = get_strategy_id(session, base)
    if not strategy_id:
        save_to_csv(make_row(filepath, universe, STATUS_NO_STRATEGY_ID, error="no strategy_id from /info"))
        print("  => Khong lay duoc strategy_id")
        return True

    metrics = wait_for_metrics(session, strategy_id)
    if metrics:
        save_to_csv(make_row(filepath, universe, STATUS_SIMULATED, metrics, strategy_id))
        print(f"  => {format_metrics(metrics)}")
    else:
        save_to_csv(make_row(filepath, universe, STATUS_METRICS_TIMEOUT, {}, strategy_id,
                             error="simulate summary not ready within timeout"))
        print("  => Metrics: N/A (simulation chua hoan tat trong timeout)")

    return True


def confirm_universe(editor_id: str, universe: str, files: list, assume_yes: bool) -> bool:
    print("\n=== CONFIRM BEFORE LIVE SUBMIT ===")
    print(f"  Editor ID      : {editor_id}")
    print(f"  Editor universe: MUST be '{universe}' selected manually in XNOQuant UI")
    print(f"  Files ({len(files)}):")
    for f in files:
        print(f"    - {f.replace(os.sep, '/')}")
    print("=" * 40)
    if assume_yes:
        print("  (--yes: confirmed automatically)")
        return True
    resp = input(f"\n  Editor tren XNOQuant dang chon '{universe}'? (y/N): ").strip().lower()
    return resp == "y"


def run_files_mode(files: list, args) -> int:
    universe = args.universe or ""
    if universe and universe not in VALID_UNIVERSES:
        print(f"[ERROR] Invalid --universe '{universe}' (allowed: {', '.join(sorted(VALID_UNIVERSES))})")
        return 1

    inferred = {infer_universe_from_path(f) for f in files}
    if not universe:
        if len(inferred) == 1 and "" not in inferred:
            universe = inferred.pop()
        elif "" in inferred:
            print("[ERROR] Cannot infer universe from path(s) — file outside output/stage_2/<cap>/")
            return 1
        else:
            print(f"[ERROR] --files spans multiple universes: {sorted(inferred)}. Use --universe to filter.")
            return 1

    if any(infer_universe_from_path(f) != universe for f in files):
        print(f"[ERROR] --files includes file(s) not in universe '{universe}'")
        return 1

    if not args.force:
        previous = load_previous_results(CSV_PATH)
        kept = []
        for fpath in files:
            key = (rel_filepath(fpath), universe)
            if key in previous and previous[key]:
                print(f"  => '{os.path.basename(fpath)}' da pass cho '{universe}', skip (dung --force de submit lai)")
            else:
                kept.append(fpath)
        files = kept
        if not files:
            print("[!] Khong co file nao can submit (tat ca da pass).")
            return 0

    print("=== XNOQuant Submit & Check Tool (Files Mode) ===\n")
    env = None if args.dry_run else require_env()
    if not args.dry_run and not env:
        return 1
    if not args.dry_run and not confirm_universe(env[0], universe, files, args.yes):
        print("  => Aborted by user (universe not confirmed).")
        return 1

    ok_count = 0
    total = len(files)
    for i, fpath in enumerate(files, 1):
        name = os.path.basename(fpath)
        print(f"[{i}/{total}] {name}")
        if args.dry_run:
            print(f"  (dry-run) would submit to universe '{universe}' — no HTTP call")
            ok_count += 1
            continue
        if run_http_sequence(env, fpath, name, universe, i, total):
            ok_count += 1
        print()
    print(f"=== Hoan thanh: {ok_count}/{total} submitted OK ===")
    print(f"Ket qua da luu vao {CSV_PATH}")
    return 0


def run_batch_mode(args) -> int:
    files = discover_batch_files()
    if not files:
        print("[!] Khong tim thay file strategy nao trong output/index.csv + output/stage_2/")
        return 1

    if args.universe:
        if args.universe not in VALID_UNIVERSES:
            print(f"[ERROR] Invalid --universe '{args.universe}' (allowed: {', '.join(sorted(VALID_UNIVERSES))})")
            return 1
        universe = args.universe
        matching, skipped = filter_files_by_universe(files, universe)
        files = matching
    else:
        groups = {u: f for u, f in split_by_universe(files).items() if u}
        if len(groups) == 1:
            universe = next(iter(groups))
        else:
            print("[ERROR] Batch contains files from multiple universes.")
            print("  Single editor => must run one cap at a time. Use --universe:")
            for u in sorted(groups):
                print(f"    --universe {u}  ({len(groups[u])} file(s))")
            return 1

    files = sorted(files)
    start_idx = max(args.start - 1, 0)
    if start_idx:
        files = files[start_idx:]
    if args.limit is not None:
        files = files[: max(args.limit, 0)]
    if args.test:
        files = files[:1]
    if not files:
        print(f"[!] Khong co file nao trong universe '{universe}'")
        return 1

    # Skip files that already PASSED for this exact (filepath, universe)
    if not args.force:
        previous = load_previous_results(CSV_PATH)
        kept, skip_count = [], 0
        for fpath in files:
            key = (rel_filepath(fpath), universe)
            if key in previous and previous[key]:
                skip_count += 1
            else:
                kept.append(fpath)
        files = kept
        if skip_count:
            print(f"  => Skipped {skip_count} file(s) da pass cho universe '{universe}' (dung --force de submit lai)")
        if not files:
            print(f"[!] Tat ca file trong '{universe}' da pass. Khong co gi de submit.")
            return 0

    print(f"=== XNOQuant Submit & Check Tool (Batch: {universe}) ===\n")

    env = None if args.dry_run else require_env()
    if not args.dry_run and not env:
        return 1
    if not args.dry_run and not confirm_universe(env[0], universe, files, args.yes):
        print("  => Aborted by user (universe not confirmed).")
        return 1

    ok_count = 0
    total = len(files)
    for i, fpath in enumerate(files, 1):
        name = os.path.basename(fpath)
        print(f"[{i}/{total}] {name}")
        if args.dry_run:
            print(f"  (dry-run) would submit to universe '{universe}' — no HTTP call")
            ok_count += 1
            continue
        if run_http_sequence(env, fpath, name, universe, i, total):
            ok_count += 1
        print()

    print(f"=== Hoan thanh: {ok_count}/{total} submitted OK ===")
    print(f"Ket qua da luu vao {CSV_PATH}")
    return 0


def parse_args():
    parser = argparse.ArgumentParser(description="Submit strategies to XNOQuant and fetch metrics.")
    parser.add_argument("--batch", action="store_true", help="Submit discovered strategy files (filtered by universe).")
    parser.add_argument("--test", action="store_true", help="LIVE submit only the first file of the selected universe.")
    parser.add_argument("--start", type=int, default=1, help="1-based start index for batch mode.")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of files to submit in batch mode.")
    parser.add_argument("--files", nargs="+", default=None, help="Submit specific file(s) by path (must be one universe).")
    parser.add_argument("--universe", default="",
                        help="Filter which cap to submit (VN-SMALL-CAP / VN-MID-CAP / VN-LARGE-CAP). Required when batch spans caps.")
    parser.add_argument("--dry-run", action="store_true", help="No HTTP calls — only print editor/universe/files.")
    parser.add_argument("--yes", action="store_true", help="Auto-confirm the editor universe prompt (no stdin).")
    parser.add_argument("--force", action="store_true", help="Re-submit even if (filepath, universe) already passed.")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.files:
        return run_files_mode(args.files, args)
    if args.batch:
        return run_batch_mode(args)

    # Interactive mode
    print("=== XNOQuant Submit & Check Tool (Interactive) ===\n")
    print("Nhap duong dan file alpha (hoac 'done' de ket thuc):\n")
    env = require_env()
    if not env:
        return 1

    while True:
        fpath = input(">>> ").strip()
        if not fpath:
            continue
        if fpath.lower() == "done":
            break
        universe = infer_universe_from_path(fpath)
        if not universe:
            print("  [!] Khong infer duoc universe tu path — file phai nam trong output/stage_2/<cap>/")
            continue
        print(f"[submit] {os.path.basename(fpath)} (universe {universe})")
        run_http_sequence(env, fpath, os.path.basename(fpath), universe, 1, None)
        print()

    print("=== Interactive session finished ===")
    print(f"Ket qua da luu vao {CSV_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
