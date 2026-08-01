#!/usr/bin/env python3
"""
Consolidated results checker — Round 2 (results_stage_2.csv).

Usage:
    python tools/check_results.py                          # All results (latest per filepath)
    python tools/check_results.py --pattern MF_*.py        # Filter by glob
    python tools/check_results.py --today                  # Today only
    python tools/check_results.py --prefix MF              # Filter by prefix
    python tools/check_results.py --pass                   # PASS only
    python tools/check_results.py --fail                   # FAIL only
    python tools/check_results.py --detail                 # Full 5-metric table
    python tools/check_results.py --detail --pass          # Detail + PASS only
    python tools/check_results.py --universe VN-SMALL-CAP  # Filter by universe
    python tools/check_results.py --csv path/to/file.csv
"""

import argparse
import fnmatch
import os
import sys

from common import (
    VALID_UNIVERSES, getf, is_pass, load_results_csv, build_latest,
    timestamp_today, status_label,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Review backtest results from results CSV")
    parser.add_argument("--pattern", default=None, help="Glob pattern to filter filepaths (e.g. VnTop*.py)")
    parser.add_argument("--today", action="store_true", help="Filter to today's date only")
    parser.add_argument("--prefix", default=None, help="Filter by filepath prefix (e.g. vn_small_cap)")
    parser.add_argument("--pass", dest="show_pass", action="store_true", help="Show PASS files only")
    parser.add_argument("--fail", dest="show_fail", action="store_true", help="Show FAIL files only")
    parser.add_argument("--universe", default=None,
                        help="Filter by universe (VN-SMALL-CAP / VN-MID-CAP / VN-LARGE-CAP)")
    parser.add_argument("--detail", action="store_true", help="Show full table with all 5 metrics")
    parser.add_argument("--csv", default="backtest/results_stage_2.csv", help="Path to results CSV")
    return parser.parse_args()


def filter_rows(latest, args):
    result = {}
    today_str = timestamp_today()

    if args.universe and args.universe not in VALID_UNIVERSES:
        raise SystemExit(f"[ERROR] Invalid --universe '{args.universe}' "
                         f"(allowed: {', '.join(sorted(VALID_UNIVERSES))})")

    for key, row in latest.items():
        fname = row.get("filepath", "")
        if args.pattern and not fnmatch.fnmatch(fname, args.pattern):
            continue
        if args.prefix and not fname.startswith(args.prefix):
            continue
        if args.universe and row.get("universe") != args.universe:
            continue
        if args.today:
            ts = row.get("timestamp", "")
            if not ts.startswith(today_str):
                continue
        label = status_label(row)
        if args.show_pass and label != "PASS":
            continue
        if args.show_fail and label != "FAIL":
            continue
        result[key] = row
    return result


def print_results(latest, args):
    if not latest:
        print("No matching results found.")
        return

    if args.detail:
        header = f'{"FILEPATH":58s} {"UNIVERSE":14s} {"Sharpe":>8s} {"CAGR":>8s} {"MaxDD":>10s} {"PF":>8s} {"Calmar":>8s}  STATUS'
        print(header)
        print("-" * (len(header) + 4))
    else:
        header = f'{"FILEPATH":58s} {"UNIVERSE":14s} {"Sharpe":>8s}  STATUS'
        print(header)
        print("-" * (len(header) + 4))

    pass_count = 0
    fail_count = 0
    for key in sorted(latest.keys()):
        row = latest[key]
        fname = row.get("filepath", "") or "-"
        universe = row.get("universe", "") or "-"
        label = status_label(row)
        if label == "PASS":
            pass_count += 1
        elif label == "FAIL":
            fail_count += 1

        if args.detail:
            s = getf(row, "sharpe")
            c = getf(row, "cagr")
            m = getf(row, "max_drawdown")
            p = getf(row, "profit_factor")
            ca = getf(row, "calmar")
            s_str = f"{s:.4f}" if s is not None else "N/A"
            c_str = f"{c:.4f}" if c is not None else "N/A"
            m_str = f"{m:.4f}" if m is not None else "N/A"
            p_str = f"{p:.4f}" if p is not None else "N/A"
            ca_str = f"{ca:.4f}" if ca is not None else "N/A"
            print(f'{fname:58s} {universe:14s} {s_str:>8s} {c_str:>8s} {m_str:>10s} {p_str:>8s} {ca_str:>8s}  {label}')
        else:
            s = getf(row, "sharpe")
            s_str = f"{s:.4f}" if s is not None else "N/A"
            print(f'{fname:58s} {universe:14s} {s_str:>8s}  {label}')

    total = len(latest)
    other = total - pass_count - fail_count
    print(f"\nPASS: {pass_count}  FAIL: {fail_count}  OTHER(PENDING/ERROR/INVALID): {other}  TOTAL: {total}")

    by_universe = {}
    for key, row in latest.items():
        u = row.get("universe", "") or "-"
        by_universe.setdefault(u, [0, 0])
        label = status_label(row)
        if label == "PASS":
            by_universe[u][0] += 1
        elif label == "FAIL":
            by_universe[u][1] += 1
    if len(by_universe) > 1:
        print("\nBy universe (PASS/FAIL):")
        for u in sorted(by_universe):
            p, fl = by_universe[u]
            print(f"  {u:14s} {p}/{fl}")


def main():
    args = parse_args()
    rows = load_results_csv(args.csv)
    if not rows:
        print(f"No data found in {args.csv}")
        sys.exit(1)

    latest = build_latest(rows)
    filtered = filter_rows(latest, args)
    print_results(filtered, args)


if __name__ == "__main__":
    main()
