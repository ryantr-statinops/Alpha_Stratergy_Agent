"""Test if 5m data works with very small chunks (2-3 days at a time)."""
from vnstock import Market
import pandas as pd
import time as ttime

m = Market()

# Try fetching 5m data for March 2025 in 3-day chunks
print("=== 5m chunked: March 2025 ===")
all_data = []
cur = pd.Timestamp("2025-03-01")
end = pd.Timestamp("2025-03-20")
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
            print(f"  {cur.date()} -> {chunk.date()}: {len(df)} rows, {r}")
    except Exception as exc:
        safe = str(exc).encode('ascii', errors='replace').decode('ascii')
        print(f"  {cur.date()} -> {chunk.date()}: ERROR - {safe[:100]}")
    cur = chunk
    ttime.sleep(0.5)

if all_data:
    full = pd.concat(all_data, ignore_index=True)
    full = full.drop_duplicates(subset=["time"]).sort_values("time")
    print(f"\nTotal: {len(full)} rows")
    print(f"Range: {full['time'].min()} -> {full['time'].max()}")
    print(f"Unique days: {full['time'].dt.date.nunique()}")
    full.to_parquet("backtest/data/cache/vn30f2506_5m_test.parquet", index=False)
else:
    print("No data retrieved")

print()
print("=== Try fetching '1m' data (maybe higher resolution gives more?) ===")
try:
    df = m.futures("VN30F2506").ohlcv(
        start="2025-03-01", end="2025-03-10", interval="1m", source="VCI"
    )
    if df is not None and len(df):
        print(f"1m: {len(df)} rows, {df['time'].min()} -> {df['time'].max()}")
    else:
        print("1m: no data")
except Exception as exc:
    safe = str(exc).encode('ascii', errors='replace').decode('ascii')
    print(f"1m: ERROR - {safe[:200]}")
