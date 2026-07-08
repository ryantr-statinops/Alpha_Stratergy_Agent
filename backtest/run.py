"""
Alpha Bot Backtest Engine — Orchestrator
Reads template configs from tools/generate_strategies.py to mirror output/ exactly.
"""
import os, sys, time, pandas as pd, numpy as np
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backtest.data.fetch_data import fetch_5m, fetch_daily, resample
from backtest.backtest import run_strategy
from backtest.regime import detect_regime, strategy_allowed, regime_label

# Import generator configs for exact parameter mirroring
from tools.generate_strategies import TEMPLATES as GEN_TEMPLATES, TF_WINDOWS, ADX_ENTRY, ADX_EXIT, ADX_ENTRY_WEAK

# Import all thesis runners
from backtest.runners import thesis_01 as th01
from backtest.runners import thesis_02 as th02
from backtest.runners import thesis_03 as th03
from backtest.runners import thesis_04 as th04
from backtest.runners import thesis_05 as th05
from backtest.runners import thesis_06 as th06
from backtest.runners import thesis_07 as th07
from backtest.runners import thesis_08 as th08
from backtest.runners import thesis_09 as th09
from backtest.runners import thesis_10 as th10
from backtest.runners import thesis_11 as th11

# ---------------------------------------------------------------------------
# Map template base name → backtest function
# ---------------------------------------------------------------------------
FUNC_MAP = {
    # Thesis 01
    "T01-A": th01.T01_A,
    "T01-B": th01.T01_B,
    "T01-C": th01.T01_C,
    "T01-D": th01.T01_D,
    "T01-E": th01.T01_E,
    "T01-F": th01.T01_F,
    "T01-G": th01.T01_G,
    # Thesis 02
    "T02-A": th02.T02_A,
    "T02-B": th02.T02_B,
    "T02-C": th02.T02_C,
    "T02-D": th02.T02_D,
    "T02-E": th02.T02_E,
    "T02-F": th02.T02_F,
    # Thesis 03
    "T03-A": th03.T03_A,
    "T03-B": th03.T03_B,
    "T03-C": th03.T03_C,
    "T03-D": th03.T03_D,
    "T03-E": th03.T03_E,
    # Thesis 04
    "T04-A": th04.T04_A,
    "T04-B": th04.T04_B,
    "T04-C": th04.T04_C,
    "T04-D": th04.T04_D,
    "T04-E": th04.T04_E,
    "T04-F": th04.T04_F,
    "T04-G": th04.T04_G,
    # Thesis 05
    "T05-A": th05.T05_A,
    "T05-B": th05.T05_B,
    "T05-C": th05.T05_C,
    "T05-D": th05.T05_D,
    "T05-E": th05.T05_E,
    "T05-F": th05.T05_F,
    "T05-G": th05.T05_G,
    # Thesis 06
    "T06-A": th06.T06_A,
    "T06-B": th06.T06_B,
    "T06-C": th06.T06_C,
    "T06-D": th06.T06_D,
    "T06-E": th06.T06_E,
    # Thesis 07
    "T07-A": th07.T07_A,
    "T07-B": th07.T07_B,
    "T07-C": th07.T07_C,
    "T07-D": th07.T07_D,
    "T07-E": th07.T07_E,
    # Thesis 08
    "T08-A": th08.T08_A,
    "T08-B": th08.T08_B,
    "T08-C": th08.T08_C,
    "T08-D": th08.T08_D,
    "T08-E": th08.T08_E,
    # Thesis 09
    "T09-A": th09.T09_A,
    "T09-B": th09.T09_B,
    "T09-C": th09.T09_C,
    # Thesis 10
    "T10-A": th10.T10_A,
    "T10-B": th10.T10_B,
    "T10-C": th10.T10_C,
    # Thesis 11
    "T11-A": th11.T11_A,
    "T11-B": th11.T11_B,
    "T11-C": th11.T11_C,
}

TF_LOOKUP = {5: "5min", 15: "15min", 30: "30min", 60: "60min"}
TF_LABEL  = {5: "5m", 15: "15m", 30: "30m", 60: "60m"}


def run_all():
    print("=" * 60)
    print("Alpha Bot Backtest Engine")
    print("=" * 60)

    # 1. Fetch data
    print("\n[1/4] Fetching data...")
    df_5m = fetch_5m(force=False)
    if df_5m.empty:
        print("No 5m data, falling back to daily...")
        df_daily = fetch_daily(force=False)
        if df_daily.empty:
            print("ERROR: No data available.")
            return
        data_cache = {"1D": df_daily}
    else:
        print(f"  5m data: {len(df_5m)} rows, {df_5m['time'].min()} -> {df_5m['time'].max()}")
        data_cache = {}
        for tf in [5, 15, 30, 60]:
            rule = TF_LOOKUP[tf]
            data_cache[rule] = resample(df_5m, rule)
            print(f"  {TF_LABEL[tf]}: {len(data_cache[rule])} rows")

    # 2. Count total variants
    n_total = 0
    for tmpl in GEN_TEMPLATES:
        n_total += len(tmpl["timeframes"])
        if tmpl["params"]:
            pv = list(tmpl["params"].values())
            n_total *= len(pv[0]) if pv else 1

    # Detect market regime from daily data
    df_daily = data_cache.get("1D", next(iter(data_cache.values())))
    regime = detect_regime(df_daily, "1D")
    rlabel = regime_label(regime)
    print(f"\n[2/4] Market regime: {rlabel} (score={regime['regime_score']})")
    print(f"  Running {n_total} variants from {len(GEN_TEMPLATES)} template configs...")

    results = []
    seq = 0
    t0 = time.time()

    for tmpl in GEN_TEMPLATES:
        name = tmpl["name"]
        thesis = tmpl["thesis"]
        descr = tmpl["descr"]
        fixed = tmpl["fixed"]
        param_grid = tmpl["params"]
        timeframes = tmpl["timeframes"]

        # Resolve function
        base = name.split("_")[0] if "_" in name else name
        import re
        m = re.match(r"(T\d\d-[A-Z])", name)
        base = m.group(1) if m else name

        # Regime filter
        if not strategy_allowed(regime, base):
            continue

        func = FUNC_MAP.get(base)
        if func is None:
            print(f"  Skipping {name}: no backtest function for base '{base}'")
            continue

        param_keys = list(param_grid.keys())
        param_vals = list(param_grid.values())
        combos = list(product(*param_vals)) if param_vals else [()]

        for tf in timeframes:
            rule = TF_LOOKUP.get(tf)
            if rule is None:
                continue
            df_tf = data_cache.get(rule)
            if df_tf is None or len(df_tf) < 100:
                continue

            tf_defaults = {
                "rsi_window":    TF_WINDOWS[tf]["rsi"],
                "adx_window":    TF_WINDOWS[tf]["adx"],
                "vol_window":    TF_WINDOWS[tf]["vol"],
                "roc_window":    TF_WINDOWS[tf]["roc"],
                "ema_window":    TF_WINDOWS[tf]["ema"],
                "return_window": TF_WINDOWS[tf]["return_periods"],
                "max_cycle_period": TF_WINDOWS[tf]["max_cycle"],
                "adx_entry":     ADX_ENTRY[tf],
                "adx_exit":      ADX_EXIT[tf],
                "adx_entry_weak": ADX_ENTRY_WEAK[tf],
                "return_exit_threshold": 0.0002,
                "vol_exit_mult": 2.0,
            }

            for combo in combos:
                seq += 1
                params = dict(fixed)
                for i, k in enumerate(param_keys):
                    params[k] = combo[i]
                for k, v in tf_defaults.items():
                    if k not in params:
                        params[k] = v

                try:
                    metrics = run_strategy(
                        df_tf, func, params,
                        timeframe=TF_LABEL.get(tf, "5m"),
                        enable_exit_enhance=True,
                        enable_freeze=True,
                    )
                    metrics["seq"] = seq
                    metrics["template"] = name
                    metrics["thesis"] = thesis
                    metrics["timeframe"] = TF_LABEL.get(tf, "5m")
                    metrics["params"] = ";".join(f"{k}={v}" for k, v in sorted(params.items()))
                    results.append(metrics)
                except Exception as e:
                    print(f"  [{seq}] {name} {TF_LABEL.get(tf)}: {str(e)[:80]}")

                if seq % 200 == 0:
                    elapsed = time.time() - t0
                    print(f"  Progress: {seq}/{n_total} ({elapsed:.0f}s)")

    # 3. Export
    print(f"\n[3/4] Exporting {len(results)} results...")
    df_out = pd.DataFrame(results)
    csv_path = os.path.join(os.path.dirname(__file__), "results.csv")
    df_out.to_csv(csv_path, index=False)
    print(f"  Saved to {csv_path}")

    # 4. Top 20
    print(f"\n[4/4] Top 20 by Sharpe:")
    if len(results) > 0:
        top = df_out.sort_values("sharpe", ascending=False).head(20)
        for _, r in top.iterrows():
            print(f"  #{int(r['seq']):04d} | {r['template']:12s} | {r['timeframe']:4s} | "
                  f"Sharpe={r['sharpe']:.2f} | CAGR={r['cagr']:.2%} | "
                  f"MaxDD={r['max_dd']:.2%} | Calmar={r['calmar']:.2f}")

    print(f"\nDone! {len(results)} variants completed.")


if __name__ == "__main__":
    run_all()
