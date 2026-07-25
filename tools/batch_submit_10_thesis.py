#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from submit_and_check import submit_and_check

files = [
    "output/thesis_39_gap_open_reversion/T39_gap_open_reversion.py",
    "output/thesis_40_liquidity_void_rebound/T40_liquidity_void_rebound.py",
    "output/thesis_41_entropy_trend_filter/T41_entropy_trend_filter.py",
    "output/thesis_42_price_impact_decay/T42_price_impact_decay.py",
    "output/thesis_43_session_transition_drift/T43_session_transition_drift.py",
    "output/thesis_44_volume_cluster_persistence/T44_volume_cluster_persistence.py",
    "output/thesis_45_tail_risk_momentum/T45_tail_risk_momentum.py",
    "output/thesis_46_intraday_liquidity_skew/T46_intraday_liquidity_skew.py",
    "output/thesis_47_funding_basis_carry/T47_funding_basis_carry.py",
    "output/thesis_48_range_expansion_followthrough/T48_range_expansion_followthrough.py",
]

total = len(files)
ok_count = 0
for idx, fp in enumerate(files):
    name = fp.split("/")[-1]
    print(f"\n[{idx+1}/{total}] {name}")
    if submit_and_check(fp, idx+1, total):
        ok_count += 1

print(f"\n=== Hoan thanh: {total} submitted, {ok_count} OK ===")
