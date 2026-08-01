#!/usr/bin/env python3
"""
Count Round-2 strategies from output/index.csv manifest and generate STATS.md.
Stage_2 strategies are tracked in output/index.csv (agent writes directly).

Usage:
    python tools/update_guide_stats.py
"""

import os
import sys
import csv
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT_DIR, "output", "index.csv")
STATS_PATH = os.path.join(ROOT_DIR, "output", "STATS.md")


def load_index(path: str) -> list:
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def generate_stats(index_rows: list):
    by_mode = {"time_series": 0, "cross_sectional": 0}
    by_universe = {}
    by_stage = {}
    total = len(index_rows)

    for r in index_rows:
        mode = (r.get("mode") or "").strip()
        universe = (r.get("universe") or "").strip()
        cap = (r.get("filepath") or "").strip().split("/")[0]
        if mode in by_mode:
            by_mode[mode] += 1
        if universe:
            by_universe[universe] = by_universe.get(universe, 0) + 1
        if cap:
            by_stage[cap] = by_stage.get(cap, 0) + 1

    with open(STATS_PATH, "w", encoding="utf-8") as f:
        f.write(f"# Strategy Statistics (Round 2)\n\n")
        f.write(f"_Auto-generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"|--------|:-----:|\n")
        f.write(f"| Total indexed | {total} |\n")
        f.write(f"| time_series | {by_mode['time_series']} |\n")
        f.write(f"| cross_sectional | {by_mode['cross_sectional']} |\n")
        if by_universe:
            for u in sorted(by_universe):
                f.write(f"| {u} | {by_universe[u]} |\n")
        if by_stage:
            for s in sorted(by_stage):
                f.write(f"| {s} | {by_stage[s]} |\n")

    print(f"Generated: {STATS_PATH}")
    print(f"  Total: {total}")
    print(f"  time_series: {by_mode['time_series']} | cross_sectional: {by_mode['cross_sectional']}")
    for u in sorted(by_universe):
        print(f"  {u}: {by_universe[u]}")


def main():
    if not os.path.isfile(INDEX_PATH):
        print(f"[!] No index found at {INDEX_PATH}")
        print("    Stage-2 strategies live in output/stage_2/ and are tracked in output/index.csv.")
        sys.exit(1)
    generate_stats(load_index(INDEX_PATH))


if __name__ == "__main__":
    main()
