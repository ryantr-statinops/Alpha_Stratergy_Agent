#!/usr/bin/env python3
"""
Count Round-2 strategies from output/index.csv manifest and generate STATS.md.
Stage_2 strategies are tracked in output/index.csv (agent writes directly).

Dimensions reported (separate tables):
  - Total indexed
  - By mode (time_series / cross_sectional)
  - By universe (VN-SMALL-CAP / VN-MID-CAP / VN-LARGE-CAP)
  - By universe x mode matrix

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

MODES = ["time_series", "cross_sectional"]
UNIVERSES = ["VN-SMALL-CAP", "VN-MID-CAP", "VN-LARGE-CAP"]


def load_index(path: str) -> list:
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def generate_stats(index_rows: list):
    by_mode = {m: 0 for m in MODES}
    by_universe = {u: 0 for u in UNIVERSES}
    matrix = {u: {m: 0 for m in MODES} for u in UNIVERSES}
    invalid = []

    for r in index_rows:
        mode = (r.get("mode") or "").strip()
        universe = (r.get("universe") or "").strip()

        if mode in by_mode:
            by_mode[mode] += 1
        else:
            invalid.append(f"invalid mode '{mode}'")
        if universe in by_universe:
            by_universe[universe] += 1
        else:
            invalid.append(f"invalid universe '{universe}'")
        if mode in MODES and universe in UNIVERSES:
            matrix[universe][mode] += 1

    with open(STATS_PATH, "w", encoding="utf-8") as f:
        f.write(f"# Strategy Statistics (Round 2)\n\n")
        f.write(f"_Auto-generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n\n")
        f.write(f"## Total\n\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"|--------|:-----:|\n")
        f.write(f"| Total indexed | {len(index_rows)} |\n")
        f.write(f"| time_series | {by_mode['time_series']} |\n")
        f.write(f"| cross_sectional | {by_mode['cross_sectional']} |\n\n")

        f.write(f"## By Universe\n\n")
        f.write(f"| Universe | Count |\n")
        f.write(f"|----------|:-----:|\n")
        for u in UNIVERSES:
            f.write(f"| {u} | {by_universe[u]} |\n")

        f.write(f"\n## Universe x Mode\n\n")
        f.write(f"| Universe | time_series | cross_sectional |\n")
        f.write(f"|----------|:-----------:|:---------------:|\n")
        for u in UNIVERSES:
            f.write(f"| {u} | {matrix[u]['time_series']} | {matrix[u]['cross_sectional']} |\n")

        if invalid:
            f.write(f"\n## Invalid rows\n\n")
            f.write("| Issue |\n|-------|\n")
            for msg in invalid:
                f.write(f"| {msg} |\n")

    print(f"Generated: {STATS_PATH}")
    print(f"  Total: {len(index_rows)}")
    print(f"  time_series: {by_mode['time_series']} | cross_sectional: {by_mode['cross_sectional']}")
    for u in UNIVERSES:
        print(f"  {u}: {by_universe[u]}")


def main():
    if not os.path.isfile(INDEX_PATH):
        print(f"[!] No index found at {INDEX_PATH}")
        print("    Stage-2 strategies live in output/stage_2/ and are tracked in output/index.csv.")
        sys.exit(1)
    generate_stats(load_index(INDEX_PATH))


if __name__ == "__main__":
    main()
