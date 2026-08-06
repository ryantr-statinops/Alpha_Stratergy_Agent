#!/usr/bin/env python3
"""Layer 3 Factor Diagnostics (static/offline).

Reads every cross-sectional alpha .py under output/stage_2, parses the field set
(self.data.*_panel), the feature/op set (self.feat.* / self.op.*), and the
eligibility block, then emits per-alpha diagnostics used as a pre-submit gate.

Data sources (both offline, no API calls):
  1. strategy .py files under output/stage_2/**/cross_sectional/
  2. backtest/results_stage_2.csv for the metrics columns (matched by filename)

The whitelist of valid panel fields is parsed from syntax/data_syntax.md so an
alpha using a non-existent or wrong-frequency field is flagged (this class of
bug is the suspected root cause of the 22 files returning 0.0000).
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGE2 = os.path.join(ROOT, "output", "stage_2")
SYNTAX = os.path.join(ROOT, "syntax", "data_syntax.md")
RESULTS = os.path.join(ROOT, "backtest", "results_stage_2.csv")
DEFAULT_OUT = os.path.join(ROOT, "backtest", "factor_diagnostics.csv")


# ---------------------------------------------------------------------------
# Plumbing
# ---------------------------------------------------------------------------

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


def parse_field_whitelist(limit=None):
    """Collect every backquoted _panel field token from data_syntax.md."""
    if not os.path.exists(SYNTAX):
        return set()
    fields = set()
    with open(SYNTAX, encoding="utf-8") as fh:
        text = fh.read()
    for tok in re.findall(r"`([a-z_0-9]+_panel)`", text):
        # normalize the wildcard form: fun_bs_total_assets_*_panel -> keep as-is
        fields.add(tok.replace("*.", ""))
    return fields


import re  # noqa: E402


def freq_of(field: str) -> str:
    if "_quarterly_panel" in field:
        return "quarterly"
    if "_annual_panel" in field:
        return "annual"
    if field.startswith(("pv_", "in_universe")):
        return "daily"
    return "unknown"


def parse_alpha(path: str) -> dict:
    """Return a bundle of parsed signals from an alpha .py file."""
    with open(path, encoding="utf-8") as fh:
        src = fh.read()

    fields_panel = sorted(set(re.findall(r"self\.data\.([a-z_0-9]+_panel)", src)))
    fields = [f for f in fields_panel if not f.startswith(("pv_", "in_universe"))]
    pv = sorted(set(f for f in fields_panel if f.startswith("pv_")))
    has_in_universe = "in_universe_panel" in src

    feat_ops = sorted(set(re.findall(r"self\.feat\.([a-z_0-9_]+)\(", src)))
    op_ops = sorted(set(re.findall(r"self\.op\.([a-z_0-9_]+)\(", src)))

    has_financial_gate = (
        "is_financial" in src
        or ("gw_premium" in src and "is_financial" in src)
    )
    has_liquidity_gate = "liquidity_rank" in src or "rank(traded_value" in src
    has_pos_denom = bool(re.search(r">\s*0|>\s*0\.0|>\s*0\.15", src))
    has_set_positions = "set_portfolio_positions(" in src

    return {
        "fields": fields,
        "pv": pv,
        "has_in_universe": has_in_universe,
        "feat_ops": feat_ops,
        "op_ops": op_ops,
        "has_financial_gate": has_financial_gate,
        "has_liquidity_gate": has_liquidity_gate,
        "has_pos_denom": has_pos_denom,
        "has_set_positions": has_set_positions,
    }


# ---------------------------------------------------------------------------
# Results CSV helpers
# ---------------------------------------------------------------------------

def load_results() -> dict:
    """Map filename -> latest metrics row keyed by strategy name."""
    if not os.path.exists(RESULTS):
        return {}
    latest = {}
    with open(RESULTS, encoding="utf-8") as fh:
        rd = csv.DictReader(fh)
        for row in rd:
            fn = row.get("filename", "")
            if not fn:
                continue
            status = row.get("status", "")
            # keep the LAST (latest timestamp) row per filename with a status
            latest[fn] = row
    return latest


# ---------------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------------

def run(whitelist, alphas, results, out_path):
    rows = []
    for universe, fn, path in alphas:
        p = parse_alpha(path)

        unknown = [f for f in p["fields"] if f not in whitelist]
        # breakdown by frequency of *used* fundamental fields
        fq = {}
        for f in p["fields"]:
            fq[re.split(r"_", f)[-1].replace("_panel", "")] = (
                fq.get(re.split(r"_", f)[-1].replace("_panel", ""), 0) + 1
            )
        annual = sum(1 for f in p["fields"] if "_annual_panel" in f)
        quarterly = sum(1 for f in p["fields"] if "_quarterly_panel" in f)
        daily = len(p["pv"])

        m = results.get(fn + ".py", results.get(fn, {}))
        row = {
            "file": f"{universe}/cross_sectional/{fn}",
            "filename": fn,
            "universe": universe.upper().replace("_", "-"),
            "mode": "cross_sectional",
            "status": str(m.get("status", "")),
            "n_fields": len(p["fields"]),
            "n_pv_fields": daily,
            "n_quarterly": quarterly,
            "n_annual": annual,
            "field_valid": "yes" if not unknown else "no: " + ",".join(unknown),
            "all_fields_valid": not bool(unknown),
            "has_universe_gate": int(p["has_in_universe"]),
            "has_financial_gate": int(p["has_financial_gate"]),
            "has_liquidity_gate": int(p["has_liquidity_gate"]),
            "has_pos_denominator": int(p["has_pos_denom"]),
            "has_positions_api": int(p["has_set_positions"]),
            "n_feat_ops": len(p["feat_ops"]),
            "n_op_ops": len(p["op_ops"]),
            "feat_ops": ",".join(p["feat_ops"]),
            "op_ops": ",".join(p["op_ops"]),
            "train_sharpe": m.get("train_sharpe", ""),
            "test_sharpe": m.get("test_sharpe", ""),
            "train_cagr": m.get("train_cagr", ""),
            "test_cagr": m.get("test_cagr", ""),
            "cagr": m.get("cagr", ""),
            "sharpe": m.get("sharpe", ""),
            "profit_factor": m.get("profit_factor", ""),
            "max_drawdown": m.get("max_drawdown", ""),
        }
        rows.append(row)

    # write CSV
    cols = [
        "file", "filename", "universe", "mode", "status",        "n_fields", "n_pv_fields", "n_quarterly", "n_annual",
        "field_valid", "all_fields_valid",
        "has_universe_gate", "has_financial_gate", "has_liquidity_gate",
        "has_pos_denominator", "has_positions_api",
        "n_feat_ops", "n_op_ops", "feat_ops", "op_ops",
        "train_sharpe", "test_sharpe", "train_cagr", "test_cagr",
        "cagr", "sharpe", "profit_factor", "max_drawdown",
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
    bad_field = [r for r in rows if not r["all_fields_valid"]]
    no_gate = [r for r in rows if not r["has_universe_gate"]]
    no_fin = [r for r in rows if not r["has_financial_gate"]]
    zero = [r for r in rows if r["status"] == "SIMULATED" and
            r["cagr"] != "" and abs(float(r["cagr"])) < 1e-9]
    uni_counter = Counter(r["universe"] for r in rows)
    print(f"\n=== Layer 3 Factor Diagnostics ===")
    print(f"Alphas analyzed : {n}")
    print(f"By universe     : {dict(uni_counter)}")
    print(f"Invalid fields  : {len(bad_field)}")
    for r in bad_field[:25]:
        print(f"   {r['filename']}: {r['field_valid']}")
    print(f"Missing universe gate: {len(no_gate)}")
    print(f"Missing financial gate: {len(no_fin)}")
    print(f"Simulated CAGR==0 files: {len(zero)}")
    for r in zero[:25]:
        print(f"   {r['filename']}")
    print(f"\nWritten: {out_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero if any alpha has invalid field")
    args = ap.parse_args()

    alphas = discover_alpha_files()
    whitelist = parse_field_whitelist()
    results = load_results()
    rows, _ = run(whitelist, alphas, results, args.out)
    summarize(rows, args.out)

    if args.strict and any(not r["all_fields_valid"] for r in rows):
        sys.exit(1)


if __name__ == "__main__":
    main()