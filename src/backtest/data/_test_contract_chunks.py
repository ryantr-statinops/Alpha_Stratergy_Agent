"""Test specific contract code for 5m data in chunks."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import time as ttime
import pandas as pd
from vnstock import Market

m = Market()

# Test VN30F2506 (June 2025 contract) - full 5m data in small chunks
print("=== VN30F2506: March 2025 in 3-day chunks ===")
all_data = []
cur = pd.Timestamp("2025-03-01")
end = pd.Timestamp("2025-03-31")
while cur < end:
    chunk = min(cur + pd.Timedelta(days=3), end)
    try:
        df = m.futures("VN30F2506").ohlcv(
            start=cur.strftime("%Y-%m-%d"),
            end=chunk.strftime("%Y-%m-%d"),
            interval="5m", source="VCI"
        )
        if df is not None and len(df):
            all_data.append(df)
            r = f"{df['time'].min()} -> {df['time'].max()}"
            print(f"  {cur.date()} -> {chunk.date()}: {len(df):5d} rows, {r}")
    except Exception as exc:
        safe = str(exc).encode('ascii', errors='replace').decode('ascii')
        print(f"  {cur.date()} -> {chunk.date()}: {safe[:150]}")
    cur = chunk
    ttime.sleep(0.3)

if all_data:
    full = pd.concat(all_data, ignore_index=True)
    full = full.drop_duplicates(subset=["time"]).sort_values("time").reset_index(drop=True)
    print(f"\nTotal: {len(full)} rows")
    print(f"Range: {full['time'].min()} -> {full['time'].max()}")
    print(f"Unique days: {full['time'].dt.date.nunique()}")

    # Test resampling
    for rule, label in [("15min", "15m"), ("30min", "30m"), ("60min", "60m")]:
        from backtest.data.fetch_data import resample as rs_func
        rs = rs_func(full, rule)
        print(f"  Resample {label}: {len(rs)} rows")
