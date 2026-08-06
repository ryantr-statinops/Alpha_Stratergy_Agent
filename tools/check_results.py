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
    python tools/check_results.py --detail                 # Aggregate metrics + split status
    python tools/check_results.py --splits                 # Detailed Aggregate/Train/Test table
    python tools/check_results.py --detail --pass          # Detail + PASS only
    python tools/check_results.py --universe VN-SMALL-CAP  # Filter by universe
    python tools/check_results.py --csv path/to/file.csv
"""

import argparse
import fnmatch
import os
import sys

from common import (
    VALID_UNIVERSES, getf, load_results_csv, build_latest,
    stage_pass, timestamp_today, status_label,
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
    parser.add_argument("--editor", default=None,
                        help="Filter by editor_id (exact match or suffix like '03')")
    parser.add_argument("--editors", action="store_true",
                        help="Show summary per editor (count, avg sharpe, pass rate)")
    parser.add_argument("--detail", action="store_true",
                        help="Show aggregate metrics plus Aggregate/Train/Test PASS/FAIL")
    parser.add_argument("--splits", action="store_true",
                        help="Show detailed Aggregate/Train/Test metrics table")
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
        if args.editor:
            editor_id = (row.get("editor_id") or "").strip()
            # Match by exact or suffix (e.g. "03" matches "uuid-...-03")
            if args.editor != editor_id and not editor_id.endswith(args.editor):
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

    if args.detail or args.splits:
        header = f'{"FILEPATH":58s} {"UNIVERSE":14s} {"EDITOR":12s} {"Sharpe":>8s} {"CAGR":>8s} {"MaxDD":>10s} {"PF":>8s} {"Calmar":>8s}  {"AGG/TRAIN/TEST":16s} STATUS'
        print(header)
        print("-" * (len(header) + 4))
    else:
        header = f'{"FILEPATH":58s} {"UNIVERSE":14s} {"EDITOR":12s} {"Sharpe":>8s}  STATUS'
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

        if args.detail or args.splits:
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
            eid = (row.get("editor_id") or "-")[:12]
            try:
                stage_labels = ["PASS" if stage_pass(row, prefix) else "FAIL"
                                for prefix in ("", "train_", "test_")]
            except KeyError:
                stage_labels = ["INVALID"] * 3
            summary = "/".join(stage_labels)
            print(f'{fname:58s} {universe:14s} {eid:12s} {s_str:>8s} {c_str:>8s} {m_str:>10s} {p_str:>8s} {ca_str:>8s}  {summary:16s} {label}')
        else:
            s = getf(row, "sharpe")
            s_str = f"{s:.4f}" if s is not None else "N/A"
            eid = (row.get("editor_id") or "-")[:12]
            print(f'{fname:58s} {universe:14s} {eid:12s} {s_str:>8s}  {label}')

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

    # Editor summary
    if args.editors:
        by_editor = {}
        for key, row in latest.items():
            eid = (row.get("editor_id") or "none").strip() or "none"
            if eid not in by_editor:
                by_editor[eid] = {"total": 0, "pass": 0, "fail": 0, "sharpes": []}
            by_editor[eid]["total"] += 1
            label = status_label(row)
            if label == "PASS":
                by_editor[eid]["pass"] += 1
            elif label == "FAIL":
                by_editor[eid]["fail"] += 1
            s = getf(row, "sharpe")
            if s is not None:
                by_editor[eid]["sharpes"].append(s)
        print("\nBy editor:")
        print(f"  {'EDITOR':12s} {'TOTAL':>6s} {'PASS':>6s} {'FAIL':>6s} {'AVG_SHARPE':>10s}")
        print(f"  {'-'*12} {'-'*6} {'-'*6} {'-'*6} {'-'*10}")
        for eid in sorted(by_editor):
            stats = by_editor[eid]
            avg_s = sum(stats["sharpes"]) / len(stats["sharpes"]) if stats["sharpes"] else 0
            print(f"  {eid:12s} {stats['total']:6d} {stats['pass']:6d} {stats['fail']:6d} {avg_s:10.4f}")

    if args.splits:
        print("\nSplit metrics:")
        header = f'{"FILEPATH":58s} {"STAGE":9s} {"Sharpe":>8s} {"CAGR":>8s} {"MaxDD":>10s} {"PF":>8s} {"Calmar":>8s}  STATUS'
        print(header)
        print("-" * (len(header) + 4))
        for key in sorted(latest.keys()):
            row = latest[key]
            fname = row.get("filepath", "") or "-"
            for stage, prefix in (("Aggregate", ""), ("Train", "train_"), ("Test", "test_")):
                values = [getf(row, f"{prefix}{metric}")
                          for metric in ("sharpe", "cagr", "max_drawdown", "profit_factor", "calmar")]
                formatted = [f"{value:.4f}" if value is not None else "N/A" for value in values]
                try:
                    split_label = "PASS" if stage_pass(row, prefix) else "FAIL"
                except KeyError:
                    split_label = "INVALID"
                print(f'{fname:58s} {stage:9s} {formatted[0]:>8s} {formatted[1]:>8s} '
                      f'{formatted[2]:>10s} {formatted[3]:>8s} {formatted[4]:>8s}  {split_label}')


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
