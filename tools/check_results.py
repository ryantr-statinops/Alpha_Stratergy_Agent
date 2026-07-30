#!/usr/bin/env python3
"""
Consolidated results checker — replaces check_detail.py, check_files.py,
check_new.py, check_today.py, report_results.py.

Usage:
    python tools/check_results.py                          # All results (latest per file)
    python tools/check_results.py --pattern MF_*.py        # Filter by glob
    python tools/check_results.py --today                  # Today only
    python tools/check_results.py --prefix MF              # Filter by prefix
    python tools/check_results.py --pass                   # PASS only
    python tools/check_results.py --fail                   # FAIL only
    python tools/check_results.py --detail                 # Full 5-metric table
    python tools/check_results.py --detail --pass          # Detail + PASS only
    python tools/check_results.py --csv backtest/results.csv
"""

import argparse
import fnmatch
import os
import sys

from common import PASS_THRESHOLDS, getf, is_pass, load_results_csv, build_latest, timestamp_today


def parse_args():
    parser = argparse.ArgumentParser(description="Review backtest results from results.csv")
    parser.add_argument("--pattern", default=None, help="Glob pattern to filter filenames (e.g. MF_*.py)")
    parser.add_argument("--today", action="store_true", help="Filter to today's date only")
    parser.add_argument("--prefix", default=None, help="Filter by filename prefix (e.g. MF, SF, NC)")
    parser.add_argument("--pass", dest="show_pass", action="store_true", help="Show PASS files only")
    parser.add_argument("--fail", dest="show_fail", action="store_true", help="Show FAIL files only")
    parser.add_argument("--detail", action="store_true", help="Show full table with all 5 metrics")
    parser.add_argument("--csv", default="backtest/results.csv", help="Path to results CSV")
    return parser.parse_args()


def filter_rows(latest, args):
    result = {}
    today_str = timestamp_today()

    for fname, row in latest.items():
        if args.pattern and not fnmatch.fnmatch(fname, args.pattern):
            continue
        if args.prefix and not fname.startswith(args.prefix):
            continue
        if args.today:
            ts = row.get("timestamp", "")
            if not ts.startswith(today_str):
                continue
        passes = is_pass(row)
        if args.show_pass and not passes:
            continue
        if args.show_fail and passes:
            continue
        result[fname] = row

    return result


def print_results(latest, args):
    if not latest:
        print("No matching results found.")
        return

    if args.detail:
        header = f'{"FILE":50s} {"S=1.3":>8s} {"C=0.15":>8s} {"MD=-0.35":>10s} {"PF=1.2":>8s} {"CA=1.1":>8s}  STATUS'
        print(header)
        print("-" * (len(header) + 4))
    else:
        header = f'{"FILE":50s} {"Sharpe":>8s}  STATUS'
        print(header)
        print("-" * 64)

    pass_count = 0
    for fname in sorted(latest.keys()):
        row = latest[fname]
        passes = is_pass(row)

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
            label = "PASS" if passes else "FAIL"
            print(f'{fname:50s} {s_str:>8s} {c_str:>8s} {m_str:>10s} {p_str:>8s} {ca_str:>8s}  {label}')
        else:
            s = getf(row, "sharpe")
            s_str = f"{s:.4f}" if s is not None else "N/A"
            label = "PASS" if passes else "FAIL"
            print(f'{fname:50s} {s_str:>8s}  {label}')

        if passes:
            pass_count += 1

    total = len(latest)
    print(f"\nPASS: {pass_count}/{total}  FAIL: {total - pass_count}/{total}")


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