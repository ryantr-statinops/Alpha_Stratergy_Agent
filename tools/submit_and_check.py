#!/usr/bin/env python3
"""
Submit strategy files to XNOQuant and fetch backtest metrics automatically.

Interactive mode: enter one file path at a time, type 'done' to finish.

Results are saved to: backtest/results.csv
"""

import requests
import json
import time
import os
import sys
import csv
from datetime import datetime

# ── CONFIG ── UPDATE THESE IF SESSION EXPIRES ──
EDITOR_ID = "a1619c25-f370-4461-9d47-ddfd2deb66dc"
TOKEN = "xq_pnLDPtb8VvmwVYPMnVDZehjSqsx1K8hr2vU"
# ──────────────────────────────────────────────

BASE = f"https://api.xnoquant.io/xalpha-api/v2/editors/{EDITOR_ID}"
HEADERS = {
    "accept": "application/json",
    "authorization": f"Bearer {TOKEN}",
    "content-type": "application/json",
    "origin": "https://alpha.xnoquant.io",
    "referer": "https://alpha.xnoquant.io/",
}
WAIT_SECONDS = 10
CSV_PATH = os.path.join("backtest", "results.csv")

session = requests.Session()
session.headers.update(HEADERS)


def print_help():
    print("""
=== XNOQuant Submit & Check Tool (Interactive) ===

Usage:
  python tools/submit_and_check.py

Nhap duong dan file alpha, go 'done' de ket thuc.

Ket qua duoc luu vao: backtest/results.csv
""")


def get_strategy_id() -> str | None:
    try:
        r = session.get(f"{BASE}/info")
        if r.status_code == 200:
            data = r.json()
            ids = data.get("data", {}).get("strategy_ids", [])
            return ids[0] if ids else None
    except Exception:
        pass
    return None


def fetch_metrics(strategy_id: str) -> dict:
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


def format_metrics(metrics: dict) -> str:
    parts = []
    for key, label in [("cagr", "CAGR"), ("sharpe", "Sharpe"), ("calmar", "Calmar"),
                        ("max_drawdown", "MaxDD"), ("profit_factor", "PF")]:
        val = metrics.get(key)
        if val is not None:
            parts.append(f"{label}: {val:.4f}")
        else:
            parts.append(f"{label}: N/A")
    return " | ".join(parts)


def save_to_csv(filename: str, status: str, metrics: dict):
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    file_exists = os.path.isfile(CSV_PATH)
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "filename": filename,
        "status": status,
        "cagr": metrics.get("cagr", ""),
        "sharpe": metrics.get("sharpe", ""),
        "calmar": metrics.get("calmar", ""),
        "max_drawdown": metrics.get("max_drawdown", ""),
        "profit_factor": metrics.get("profit_factor", ""),
    }
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def submit_and_check(fpath: str, index: int, total: int) -> bool:
    if not os.path.isfile(fpath):
        print(f"  [!] File khong ton tai: {fpath}")
        return False

    with open(fpath, encoding="utf-8") as f:
        code = f.read()

    name = os.path.basename(fpath)

    max_retries = 5
    for attempt in range(1, max_retries + 1):
        r1 = session.put(f"{BASE}/update", json={"code": code})
        r2 = session.post(f"{BASE}/verify")
        time.sleep(2)
        r3 = session.post(f"{BASE}/simulate")

        ok = all(s in (200, 201, 204) for s in (r1.status_code, r2.status_code, r3.status_code))
        detail = ""
        if not ok:
            for r, label in [(r1, "PUT"), (r2, "VERIFY"), (r3, "SIMULATE")]:
                if r.status_code not in (200, 201, 204):
                    try:
                        detail += f" {label}:{r.text[:200]}"
                    except:
                        pass

        print(f"  PUT: {r1.status_code} | VERIFY: {r2.status_code} | SIMULATE: {r3.status_code} "
              f"{'[OK]' if ok else '[FAIL]'}  {name}{detail}")

        if ok:
            break

        is_rate_limit = r1.status_code == 429 or r2.status_code == 429 or r3.status_code == 429
        if not is_rate_limit or attempt == max_retries:
            save_to_csv(name, "FAIL", {})
            return False

        wait = 15
        print(f"  => Rate limit, retry in {wait}s (attempt {attempt}/{max_retries})...")
        time.sleep(wait)

    print(f"  Doi {WAIT_SECONDS}s de fetch ket qua...")
    time.sleep(WAIT_SECONDS)

    strategy_id = get_strategy_id()
    if strategy_id:
        metrics = fetch_metrics(strategy_id)
        if metrics:
            save_to_csv(name, "OK", metrics)
            print(f"  => {format_metrics(metrics)}")
        else:
            save_to_csv(name, "OK", {})
            print(f"  => Metrics: N/A (co the simulation chua hoan tat)")
    else:
        save_to_csv(name, "OK", {})
        print(f"  => Khong lay duoc strategy_id")

    return True


def main():
    print("=== XNOQuant Submit & Check Tool (Interactive) ===\n")
    print("Nhap duong dan file alpha (hoac 'done' de ket thuc):\n")

    ok_count = 0
    total = 0
    while True:
        fpath = input(">>> ").strip()
        if not fpath:
            continue
        if fpath.lower() == "done":
            break
        total += 1
        name = os.path.basename(fpath)
        print(f"[{total}] {name}")
        if submit_and_check(fpath, total, None):
            ok_count += 1
        print()

    print(f"=== Hoan thanh: {total} submitted, {ok_count} OK ===")
    print(f"Ket qua da luu vao {CSV_PATH}")


if __name__ == "__main__":
    main()
