#!/usr/bin/env python3
"""Layer 4 Economic Validation (static/offline).

Cross-statement consistency checks for every cross-sectional alpha under
output/stage_2. Unlike Layer 3 (factor quality), Layer 4 validates data truth:
does the strategy pair the right statements at the right frequency, and does it
mix annual into quarterly ratios (suspected root cause of the 22 zero files)?

Data sources (offline, no API calls):
  1. strategy .py files under output/stage_2/**/cross_sectional/
  2. backtest/results_stage_2.csv for metrics (matched by filename)
"""

from __future__ import annotations

import argparse
import csv
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGE2 = os.path.join(ROOT, "output", "stage_2")
RESULTS = os.path.join(ROOT, "backtest", "results_stage_2.csv")
DEFAULT_OUT = os.path.join(ROOT, "backtest", "economic_validation.csv")

# Pair definitions used by MASTER Layer 4. Each entry: (check_name, list of
# regex fragments matching field families on either side of the pair).
CHECKS = [
    ("ni_vs_cfo", "net_profit", "operating_activities"),
    ("inventory_vs_revenue", "inventor", "revenue"),
    ("receivables_vs_revenue", "receivable", "revenue"),
    ("debt_vs_interest", "borrowing", "interest"),
    ("capex_vs_ppe", "fixed_assets", "tangible_fixed_assets"),
    ("dividend_vs_cfo", "dividend", "operating_activities"),
]


def discover_alpha_files():
    files = []
    for universe in ("vn_large_cap", "vn_mid_cap", "vn_small_cap"):
        d = os.path.join(STAGE2, universe, "cross_sectional")
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".py"):
                files.append((universe, fn, os.path.join(d, fn)))
    return files


def classify_field(field: str) -> tuple[str, str]:
    """Return (statement, frequency). statement in {is, bs, cf, pv, univ}."""
    if field.startswith(("pv_", "in_universe")):
        return "pv", "daily"
    if field.startswith("fun_is_"):
        return "is", "quarterly" if "_quarterly_panel" in field else "annual"
    if field.startswith("fun_bs_"):
        return "bs", "quarterly" if "_quarterly_panel" in field else "annual"
    if field.startswith("fun_cf_"):
        return "cf", "quarterly" if "_quarterly_panel" in field else "annual"
    return "unknown", "unknown"


def parse_alpha(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    fields = sorted(set(re.findall(r"self\.data\.([a-z_0-9]+_panel)", src)))
    non_pv = [f for f in fields if not f.startswith(("pv_", "in_universe"))]
    return {"fields": fields, "fundamentals": non_pv}


def run(alphas, results, out_path):
    rows = []
    for universe, fn, path in alphas:
        p = parse_alpha(path)
        fq = [classify_field(f) for f in p["fundamentals"]]
        freq_set = sorted({f for (_, f) in fq})
        has_annual = any(f == "annual" for (_, f) in fq)
        has_quarterly = any(f == "quarterly" for (_, f) in fq)

        # per-check presence: both sides of the pair available?
        check_flags = {}
        joined = ",".join(p["fundamentals"])
        for name, a_frag, b_frag in CHECKS:
            check_flags[name] = int(bool(re.search(a_frag, joined) and re.search(b_frag, joined)))

        # frequency mixing: an alpha that uses BOTH annual and quarterly
        # fundamentals in the same ratio block is a red flag.
        annual_fields = [f for f in p["fundamentals"] if "_annual_panel" in f]
        quarterly_fields = [f for f in p["fundamentals"] if "_quarterly_panel" in f]

        m = results.get(fn, {})
        rows.append({
            "file": f"{universe}/cross_sectional/{fn}",
            "filename": fn,
            "universe": universe.upper().replace("_", "-"),
            "status": str(m.get("status", "")),
            "n_fundamental_fields": len(p["fundamentals"]),
            "freqs": "+".join(freq_set),
            "uses_annual": int(has_annual),
            "uses_quarterly": int(has_quarterly),
            "mixed_annual_quarterly": int(has_annual and has_quarterly),
            **check_flags,
            "n_annual_fields": len(annual_fields),
            "n_quarterly_fields": len(quarterly_fields),
            "annual_fields": ",".join(annual_fields),
            "quarterly_fields": ",".join(quarterly_fields),
            "cagr": m.get("cagr", ""),
        })

    cols = [
        "file", "filename", "universe", "status",
        "n_fundamental_fields", "freqs", "uses_annual", "uses_quarterly",
        "mixed_annual_quarterly",
        "ni_vs_cfo", "inventory_vs_revenue", "receivables_vs_revenue",
        "debt_vs_interest", "capex_vs_ppe", "dividend_vs_cfo",
        "n_annual_fields", "n_quarterly_fields", "annual_fields",
        "quarterly_fields", "cagr",
    ]
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=cols)
        wr.writeheader()
        for r in rows:
            wr.writerow(r)
    return rows, cols


def summarize(rows, out_path):
    from collections import Counter
    n = len(rows)
    print(f"\n=== Layer 4 Economic Validation ===")
    print(f"Alphas analyzed : {n}")
    print(f"By universe     : {dict(Counter(r['universe'] for r in rows))}")
    print(f"Uses annual     : {sum(r['uses_annual'] for r in rows)}")
    print(f"Uses quarterly  : {sum(r['uses_quarterly'] for r in rows)}")
    print(f"MIXED an+q      : {sum(r['mixed_annual_quarterly'] for r in rows)}")
    print(f"Check presence (both sides available):")
    for name, _, _ in CHECKS:
        print(f"   {name}: {sum(r[name] for r in rows)}/{n}")
    print(f"\nWritten: {out_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args()

    alphas = discover_alpha_files()
    results = {}
    if os.path.exists(RESULTS):
        with open(RESULTS, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                fn = row.get("filename", "")
                if fn:
                    results[fn] = row

    rows, _ = run(alphas, results, args.out)
    summarize(rows, args.out)


if __name__ == "__main__":
    main()