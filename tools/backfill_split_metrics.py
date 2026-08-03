#!/usr/bin/env python3
"""Read-only split-metric audit with explicit opt-in append backfill."""

import argparse
import os
import sys
import time

import requests
from dotenv import load_dotenv

from common import build_latest, flatten_stage_metrics, format_metrics, load_results_csv
from submit_and_check import (
    BASE_DIR, CSV_PATH, POLL_TIMEOUT, STATUS_SIMULATED, build_headers, make_row,
    save_to_csv, wait_for_metrics,
)

load_dotenv(os.path.join(BASE_DIR, ".env"))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fetch Aggregate/Train/Test metrics for existing SIMULATED rows. "
                    "Default is read-only; --write appends enriched rows.")
    parser.add_argument("--csv", default=CSV_PATH, help="Results CSV path")
    parser.add_argument("--universe", default="", help="Filter exact universe")
    parser.add_argument("--prefix", default="", help="Filter filepath prefix")
    parser.add_argument("--write", action="store_true",
                        help="Append enriched rows (without this flag, no CSV writes)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Explicit read-only mode (the default); GET requests still run")
    parser.add_argument("--delay", type=float, default=2.0,
                        help="Seconds between strategies (default: 2)")
    parser.add_argument("--timeout", type=int, default=POLL_TIMEOUT,
                        help="Per-strategy polling timeout")
    return parser.parse_args()


def select_candidates(rows, universe="", prefix=""):
    simulated = [row for row in rows
                 if (row.get("status") or "").strip().upper() == STATUS_SIMULATED
                 and (row.get("strategy_id") or "").strip()]
    latest = build_latest(simulated)
    return [row for row in latest.values()
            if (not universe or row.get("universe") == universe)
            and (not prefix or (row.get("filepath") or "").startswith(prefix))]


def main():
    args = parse_args()
    if args.write and args.dry_run:
        raise SystemExit("[ERROR] --write and --dry-run are mutually exclusive")
    token = os.getenv("XNO_TOKEN")
    if not token:
        raise SystemExit("[ERROR] Missing XNO_TOKEN in .env")

    candidates = select_candidates(load_results_csv(args.csv), args.universe, args.prefix)
    if not candidates:
        print("No matching SIMULATED rows with strategy_id found.")
        return 0

    mode = "WRITE (append-only)" if args.write else "DRY-RUN (GET only, no CSV writes)"
    print(f"Backfill audit: {len(candidates)} candidate(s) | {mode}")
    session = requests.Session()
    session.headers.update(build_headers(token))
    completed = 0
    for index, source in enumerate(candidates, 1):
        strategy_id = source["strategy_id"].strip()
        filepath = source.get("filepath") or ""
        print(f"[{index}/{len(candidates)}] {filepath} ({strategy_id})")
        stages = wait_for_metrics(session, strategy_id, args.timeout)
        if not stages:
            print("  Aggregate/Train/Test not all ready; skipped")
        else:
            for stage, label in (("simulate", "Aggregate"), ("train", "Train"), ("test", "Test")):
                print(f"  {label:9s}: {format_metrics(stages[stage])}")
            if args.write:
                row = make_row(filepath, source.get("universe") or "", STATUS_SIMULATED,
                               flatten_stage_metrics(stages), strategy_id)
                row["filename"] = source.get("filename") or os.path.basename(filepath)
                row["mode"] = source.get("mode") or ""
                save_to_csv(row, args.csv)
                print("  Appended enriched row")
            completed += 1
        if index < len(candidates) and args.delay > 0:
            time.sleep(args.delay)
    print(f"Complete: {completed}/{len(candidates)} summaries ready")
    return 0


if __name__ == "__main__":
    sys.exit(main())
