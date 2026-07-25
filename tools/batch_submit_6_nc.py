#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from submit_and_check import submit_and_check

files = [
    "output/niche_alpha/NC_NATR_EXPANSION_ADX_15min.py",
    "output/niche_alpha/NC_ROLLING_RANK_BREAKOUT_ADX_15min.py",
    "output/niche_alpha/NC_TSF_BREAKOUT_ADX_15min.py",
    "output/niche_alpha/NC_TRANGE_BREAKOUT_ADX_15min.py",
    "output/niche_alpha/NC_ENGULFING_ADX_15min.py",
    "output/niche_alpha/NC_HAMMER_DOJI_REVERSAL_ADX_15min.py",
]

total = len(files)
ok_count = 0
for idx, fp in enumerate(files):
    name = os.path.basename(fp)
    print(f"\n[{idx+1}/{total}] {name}")
    if submit_and_check(fp, idx+1, total):
        ok_count += 1

print(f"\n=== Hoan thanh: {total} submitted, {ok_count} OK ===")
