#!/usr/bin/env python3
"""Fetch yearly summary-table rows (GET-only) for stage-2 strategies.

Year-by-year stability is the primary validation gate: aggregate train Sharpe is
inflated by the 2020-21 bull, so a candidate must show Sharpe >= 0 in >= 4 of 5
years (2020-2024) and hold up in 2022 (the only honest train year, VNIndex
crash) to be considered robust.

Endpoints (read-only):
  /strategies/{id}/stages/{stage}/summary-table  -> data: [ {time, cagr, sharpe, ...} ]

Usage:
  python tools/fetch_yearly_tables.py --strategy-id DSbhQzWjPi --strategy-id 6hZhskaS1Y
  python tools/fetch_yearly_tables.py --from-csv-prefix VnSmallCsFinancialNetPayout
  python tools/fetch_yearly_tables.py --from-csv-universe VN-SMALL-CAP --from-csv-prefix VnSmallCsValueTrend

No CSV writes; never mutates an editor.
"""

import argparse
import os
import sys
import time

import requests
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import build_latest, getf, load_results_csv, row_status
from submit_and_check import BASE_DIR, build_headers

TABLE_URL = "https://api.xnoquant.io/xalpha-api/v1/strategies/{strategy_id}/stages/{stage}/summary-table"
STAGES = ("simulate", "train", "test")
MARKET_REGIME = {
    2020: ("bull-ish (COVID recovery; Sharpe 1.7-2.0)", "maniac"),
    2021: ("bull peak (VNIndex high; Sharpe 1.4-2.0)", "mania"),
    2022: ("crash (VNIndex correction; Sharpe -0.3..-0.9)", "honest"),
    2023: ("recovery (Sharpe 0.66-1.15)", "moderate"),
    2024: ("mature/chop (Sharpe 0.75-1.06)", "moderate"),
}


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--strategy-id", action="append", default=[],
                   help="Strategy id(s) to fetch (repeatable)")
    p.add_argument("--from-csv-prefix", default="",
                   help="Pick latest SIMULATED rows whose filename starts with this")
    p.add_argument("--from-csv-universe", default="",
                   help="Universe filter when picking from CSV")
    p.add_argument("--scan-pass-train", action="store_true",
                   help="Scan ALL latest SIMULATED rows with train_sharpe >= 1.0 "
                        "(Gate 1-3 only, simulate stage). Compact output.")
    p.add_argument("--out", default="",
                   help="CSV output path for scan summary (Gate 1-3 flags)")
    p.add_argument("--csv", default=os.path.join("backtest", "results_stage_2.csv"))
    p.add_argument("--delay", type=float, default=1.0)
    return p.parse_args()


def fetch_yearly(session, strategy_id, stage):
    url = TABLE_URL.format(strategy_id=strategy_id, stage=stage)
    try:
        resp = session.get(url)
        if resp.status_code != 200:
            return None
        return (resp.json().get("data") or []) or None
    except Exception:
        return None


def pick_from_csv(prefix, universe, csv_path):
    rows = load_results_csv(csv_path)
    latest = build_latest(rows)
    out = []
    for r in latest.values():
        if row_status(r) != "SIMULATED":
            continue
        if universe and r.get("universe") != universe:
            continue
        fn = (r.get("filename") or "").replace(".py", "")
        if prefix and not fn.startswith(prefix):
            continue
        sid = (r.get("strategy_id") or "").strip()
        if sid:
            out.append((fn, sid))
    return out


def gate_eval(yearly):
    """Stability gates on the 2020-2024 full-window (simulate) table."""
    if not yearly:
        return None
    years = [r for r in yearly if (r.get("time") or "") and int(r["time"][:4]) < 2025]
    if not years:
        return None
    pos = [r for r in years if (r.get("sharpe") or 0) >= 0]
    y2022 = next((r for r in years if r["time"].startswith("2022")), None)
    y2024 = next((r for r in years if r["time"].startswith("2024")), None)
    return {
        "n_years": len(years),
        "pos_years": len(pos),
        "gate_4of5": len(pos) >= 4,
        "sharpe_2022": (y2022 or {}).get("sharpe"),
        "sharpe_2024": (y2024 or {}).get("sharpe"),
    }


def gate_pass(gate):
    """Strict bar: >=4/5 positive years, 2022 >= 0, 2024 >= 0."""
    if not gate or gate["n_years"] < 5:
        return False
    return (gate["gate_4of5"]
            and (gate["sharpe_2022"] or 0) >= 0
            and (gate["sharpe_2024"] or 0) >= 0)


def scan_pass_train(session, args):
    """Gate 1-3 scan across every latest SIMULATED row with train_sharpe >= 1.0."""
    import csv as _csv
    rows = load_results_csv(args.csv)
    latest = build_latest(rows)
    cands = []
    for r in latest.values():
        if row_status(r) != "SIMULATED":
            continue
        tr = getf(r, "train_sharpe")
        if tr is None or tr < 1.0:
            continue
        if args.from_csv_universe and r.get("universe") != args.from_csv_universe:
            continue
        cands.append(r)
    cands.sort(key=lambda r: -(getf(r, "train_sharpe") or 0))

    print(f"Gate 1-3 scan over {len(cands)} train-pass strategies "
          f"(train_sharpe >= 1.0) | strict bar: >=4/5 yr+, 2022>=0, 2024>=0\n")
    header = ("FILENAME", "UNIVERSE", "POS/N", "2022", "2024", "GATE")
    print(f"{'filename':<46}{'univ':<14}{'pos/n':>6}{'2022':>8}{'2024':>8}  gate")
    out_rows = []
    passed = failed = 0
    for i, r in enumerate(cands, 1):
        sid = (r.get("strategy_id") or "").strip()
        fn = (r.get("filename") or "")
        if not sid:
            continue
        yearly = fetch_yearly(session, sid, "simulate")
        gate = gate_eval(yearly)
        ok = gate_pass(gate)
        if ok:
            passed += 1
        else:
            failed += 1
        y22 = gate["sharpe_2022"] if gate else None
        y24 = gate["sharpe_2024"] if gate else None
        posn = f"{gate['pos_years']}/{gate['n_years']}" if gate else "n/a"
        tag = "PASS" if ok else "FAIL"
        print(f"{fn:<46}{r.get('universe',''):<14}{posn:>6}"
              f"{y22 if y22 is not None else float('nan'):>8.2f}"
              f"{y24 if y24 is not None else float('nan'):>8.2f}  {tag}")
        out_rows.append({
            "filename": fn, "universe": r.get("universe", ""),
            "train_sharpe": getf(r, "train_sharpe"),
            "pos_years": gate["pos_years"] if gate else None,
            "n_years": gate["n_years"] if gate else None,
            "sharpe_2022": y22, "sharpe_2024": y24,
            "gate": tag,
        })
        if i < len(cands) and args.delay > 0:
            time.sleep(args.delay)
    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8") as f:
            w = _csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
            w.writeheader()
            w.writerows(out_rows)
        print(f"\nWrote {len(out_rows)} rows to {args.out}")
    print(f"\n=== GATE 1-3: PASS {passed} | FAIL {failed} | survival {passed/(passed+failed):.2f} ===")
    return passed, failed


def main():
    args = parse_args()
    token = os.getenv("XNO_TOKEN")
    if not token:
        raise SystemExit("[ERROR] Missing XNO_TOKEN in .env")
    if args.scan_pass_train:
        if args.strategy_id or args.from_csv_prefix:
            raise SystemExit("[ERROR] --scan-pass-train is standalone; do not combine with "
                             "--strategy-id / --from-csv-prefix")
        if not args.strategy_id and not args.from_csv_prefix:
            session = requests.Session()
            session.headers.update(build_headers(token))
            scan_pass_train(session, args)
            return 0
    if not args.strategy_id and not args.from_csv_prefix:
        raise SystemExit("[ERROR] Provide --strategy-id or --from-csv-prefix (or --scan-pass-train)")

    targets = [(sid, sid) for sid in args.strategy_id]
    if args.from_csv_prefix:
        targets += pick_from_csv(args.from_csv_prefix, args.from_csv_universe, args.csv)

    session = requests.Session()
    session.headers.update(build_headers(token))

    for label, sid in targets:
        print(f"\n{'='*80}\n{label}  ({sid})")
        tables = {st: fetch_yearly(session, sid, st) for st in STAGES}
        sim_table = tables["simulate"]
        gate = gate_eval(sim_table)
        if gate:
            flag = "PASS-GATE1" if (gate["gate_4of5"] and (gate["sharpe_2022"] or 0) >= -0.2) else "FAIL-GATE1"
            print(f"GATE1 year-by-year (2020-24): positive {gate['pos_years']}/{gate['n_years']}"
                  f" | 2022 Sharpe {gate['sharpe_2022'] if gate['sharpe_2022'] is not None else 'n/a'}"
                  f" | 2024 Sharpe {gate['sharpe_2024'] if gate['sharpe_2024'] is not None else 'n/a'}"
                  f"  ->  {flag}")
        for st in STAGES:
            table = tables[st]
            print(f"\n[{st}] summary-table")
            if not table:
                print("  (no data)")
                continue
            print(f"  {'time':<6}{'cagr':>8}{'sharpe':>8}{'calmar':>8}{'maxdd':>9}{'pf':>7}  regime")
            for r in sorted(table, key=lambda x: x.get("time") or ""):
                year = int((r.get("time") or "0")[:4])
                if year >= 2025:
                    continue
                reg = MARKET_REGIME.get(year, ("", ""))
                print(f"  {r.get('time',''):<6}{getf(r,'cagr') or float('nan'):>8.2f}"
                      f"{getf(r,'sharpe') or float('nan'):>8.2f}"
                      f"{getf(r,'calmar') or float('nan'):>8.2f}"
                      f"{(getf(r,'max_drawdown') or float('nan'))*100:>8.1f}%"
                      f"{getf(r,'profit_factor') or float('nan'):>7.2f}  {reg[0]}")
        time.sleep(args.delay)
    return 0


if __name__ == "__main__":
    sys.exit(main())
