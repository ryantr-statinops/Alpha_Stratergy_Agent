"""Quick backtest proof-of-concept using daily data."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from backtest.data.fetch_data import load_daily, resample
from backtest.evaluate import evaluate

# Load daily data
df = load_daily()
print(f"Daily data: {len(df)} rows")
print(f"  Range: {df['time'].min()} -> {df['time'].max()}")

# Test T01-B: MA Crossover on daily data
from backtest.runners.thesis_01 import T01_B, T01_F, T01_D
from backtest.runners.thesis_02 import T02_A, T02_E
from backtest.runners.thesis_03 import T03_C
from backtest.runners.thesis_04 import T04_A, T04_F

tests = [
    ("T01-B MA Crossover", T01_B, {"fast_window": 13, "slow_window": 34}),
    ("T01-D Quantile Breakout", T01_D, {"q_window": 20, "q_high": 0.9, "q_low": 0.1}),
    ("T01-F Z-Score Rev", T01_F, {"z_window": 20, "z_entry": 2.0}),
    ("T02-A Vol Breakout", T02_A, {"vol_window": 14, "vol_entry": 1.5}),
    ("T02-E NATR Regime", T02_E, {"natr_window": 14}),
    ("T03-C LinReg Slope", T03_C, {"lr_window": 14}),
]

print("\n=== Quick Backtest on Daily Data ===")
for label, func, params in tests:
    try:
        pos = func(df, **params)
        result_df = df.copy()
        result_df["position"] = pos
        metrics = evaluate(result_df, timeframe="1D")
        sharpe = metrics["sharpe"]
        cagr = metrics["cagr"]
        mdd = metrics["max_dd"]
        calmar = metrics["calmar"]
        pf = metrics["profit_factor"]
        print(f"  {label:25s} | Sharpe={sharpe:.2f} | CAGR={cagr:.2%} | MaxDD={mdd:.2%} | Calmar={calmar:.2f} | PF={pf:.2f}")
    except Exception as e:
        print(f"  {label:25s} | ERROR: {str(e)[:80]}")
