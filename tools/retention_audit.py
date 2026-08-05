#!/usr/bin/env python3
"""Retention audit for stage-2 strategies — multiple-testing math + parameter plateau.

Reads backtest/results_stage_2.csv, dedups to latest per (filepath, universe),
and for every SIMULATED family reports:

  N        candidates tested
  PassTr   Sharpe(train) >= 1.2
  PassBoth Sharpe(train) >= 1.2 and Sharpe(test) >= 1.2
  ExpFP    expected false positives among PassTr at alpha=0.05
  Retain   PassBoth / PassTr (survival ratio)

A survival ratio near the nominal alpha (5%) means train-pass is dominated by
statistical luck, not durable edge.

GET-only — reads the CSV, never touches the network.
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import build_latest, getf, load_results_csv, row_status, row_key

DEFAULT_CSV = os.path.join("backtest", "results_stage_2.csv")
TRAIN_MIN = 1.2
TEST_MIN = 1.2
ALPHA = 0.05


def family_of(filename):
    """Group a filename into a family by stripping a trailing P<digits> variant tag."""
    name = (filename or "").replace(".py", "").strip()
    return re.sub(r"P\d{2,}$", "", name)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--csv", default=DEFAULT_CSV)
    p.add_argument("--universe", default="", help="Filter exact universe")
    p.add_argument("--min-candidates", type=int, default=1,
                   help="Only show families with at least this many candidates")
    p.add_argument("--plateau", action="store_true",
                   help="Print per-variant train/test for variant families")
    p.add_argument("--min-variants", type=int, default=3,
                   help="Plateau: only families with >= this many variants")
    return p.parse_args()


def main():
    args = parse_args()
    rows = load_results_csv(args.csv)
    latest = build_latest(rows)
    sim = [r for r in latest.values() if row_status(r) == "SIMULATED"]
    if args.universe:
        sim = [r for r in sim if r.get("universe") == args.universe]

    fam = {}
    for r in sim:
        fam.setdefault(family_of(r.get("filename")), []).append(r)

    print(f"{'Family':<44}{'N':>4}{'PassTr':>7}{'Both':>6}{'ExpFP':>6}{'Retain':>8}")
    print("-" * 78)
    rows_out = []
    for base in sorted(fam, key=lambda b: -len(fam[b])):
        group = fam[base]
        if len(group) < args.min_candidates:
            continue
        pass_tr = [r for r in group if (getf(r, "train_sharpe") or 0) >= TRAIN_MIN]
        pass_both = [r for r in pass_tr if (getf(r, "test_sharpe") or 0) >= TEST_MIN]
        exp_fp = ALPHA * len(pass_tr)
        retain = len(pass_both) / len(pass_tr) if pass_tr else 0.0
        rows_out.append((base, group, pass_tr, pass_both))
        print(f"{base:<44}{len(group):>4}{len(pass_tr):>7}{len(pass_both):>6}"
              f"{exp_fp:>6.1f}{retain:>8.2f}")

    if args.plateau:
        print("\n=== Parameter plateau (variant train/test) ===")
        for base, group, pass_tr, pass_both in rows_out:
            if len(group) < args.min_variants:
                continue
            print(f"\n{base}  (train_sharpe, test_sharpe)")
            for r in sorted(group, key=lambda r: -(getf(r, "train_sharpe") or 0)):
                ts = getf(r, "train_sharpe") or float("nan")
                te = getf(r, "test_sharpe") or float("nan")
                print(f"  {r.get('filename'):<44} Tr {ts:6.2f}  Te {te:6.2f}")

    tot_tr = sum(len(gt) for _, _, gt, _ in rows_out)
    tot_both = sum(len(gb) for _, _, _, gb in rows_out)
    print("\n" + "-" * 78)
    print(f"TOTAL families shown: {len(rows_out)} | PassTr {tot_tr} | PassBoth {tot_both}"
          f" | survival {tot_both/tot_tr:.2f} (alpha={ALPHA})" if tot_tr else "no rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
