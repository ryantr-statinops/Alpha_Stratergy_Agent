"""Quick fetch test: limited date range to test pipeline."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from backtest.data.fetch_data import fetch_5m, fetch_daily, resample

# Test fetching 5m for just 1 month
print("=== Fetching 5m: June 2025 ===")
import time as ttime
from vnstock import Market
import pandas as pd

m = Market()
all_data = []
cur = pd.Timestamp("2025-06-01")
end = pd.Timestamp("2025-06-10")
while cur < end:
    chunk = min(cur + pd.Timedelta(days=3), end)
    try:
        df = m.futures("VN30F1M").ohlcv(
            start=cur.strftime("%Y-%m-%d"),
            end=chunk.strftime("%Y-%m-%d"),
            interval="5m", source="VCI"
        )
        if df is not None and len(df):
            all_data.append(df)
            r = f"{df['time'].min()} -> {df['time'].max()}"
            print(f"  {cur.date()} -> {chunk.date()}: {len(df)} rows, {r}")
    except Exception as exc:
        safe = str(exc).encode('ascii', errors='replace').decode('ascii')
        print(f"  {cur.date()} -> {chunk.date()}: {safe[:150]}")
    cur = chunk
    ttime.sleep(0.3)

if all_data:
    full = pd.concat(all_data, ignore_index=True)
    full = full.drop_duplicates(subset=["time"]).sort_values("time").reset_index(drop=True)
    print(f"\nTotal: {len(full)} rows, {full['time'].min()} -> {full['time'].max()}")

    # Test resampling
    print("\n=== Resample tests ===")
    for rule, label in [("15min", "15m"), ("30min", "30m"), ("60min", "60m")]:
        rs = resample(full, rule)
        print(f"  {label}: {len(rs)} rows, {rs['time'].min()} -> {rs['time'].max()}")
else:
    print("No 5m data. Trying contract codes...")
    for sym in ["VN30F2506"]:
        df = m.futures(sym).ohlcv(start="2025-03-01", end="2025-03-10", interval="5m", source="VCI")
        if df is not None and len(df):
            print(f"  {sym}: {len(df)} rows, {df['time'].min()} -> {df['time'].max()}")
