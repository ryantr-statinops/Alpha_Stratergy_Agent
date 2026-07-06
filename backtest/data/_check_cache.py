"""Check what data we have cached."""
import pandas as pd

try:
    d = pd.read_parquet("backtest/data/cache/vn30f_daily.parquet")
    print(f"Daily: {len(d)} rows")
    print(f"  Range: {d['time'].min()} -> {d['time'].max()}")
    print(f"  Columns: {d.columns.tolist()}")
    print(f"  Head:\n{d.head(3)}")
    print(f"  Tail:\n{d.tail(3)}")
except Exception as e:
    print(f"No daily cache: {e}")

try:
    d = pd.read_parquet("backtest/data/cache/vn30f_5m.parquet")
    print(f"\n5m: {len(d)} rows")
    print(f"  Range: {d['time'].min()} -> {d['time'].max()}")
    print(f"  Unique days: {d['time'].dt.date.nunique()}")
except Exception as e:
    print(f"No 5m cache: {e}")
