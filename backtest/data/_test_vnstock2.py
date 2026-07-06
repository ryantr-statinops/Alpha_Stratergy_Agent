"""Test vnstock chunked fetching approach."""
from vnstock import Market
from datetime import datetime, timedelta

m = Market()

# Try fetching daily data in chunks to get more history
print("=== Daily chunked fetch ===")
all_data = []
start = datetime(2022, 1, 1)
while start < datetime(2026, 7, 3):
    end = min(start + timedelta(days=60), datetime(2026, 7, 3))
    try:
        df = m.futures("VN30F1M").ohlcv(
            start=start.strftime("%Y-%m-%d"),
            end=end.strftime("%Y-%m-%d"),
            interval="1D",
            source="VCI"
        )
        if len(df):
            all_data.append(df)
            print(f"  {start.date()} -> {end.date()}: {len(df)} rows")
    except Exception as e:
        print(f"  {start.date()} -> {end.date()}: error - {str(e)[:100]}")
    start = end

if all_data:
    import pandas as pd
    full = pd.concat(all_data, ignore_index=True)
    full = full.drop_duplicates(subset=["time"])
    full = full.sort_values("time")
    print(f"\nTotal: {len(full)} rows")
    print(f"Range: {full['time'].min()} -> {full['time'].max()}")

print()
print("=== Try 5m chunked for 1 month ===")
import time as ttime
all_5m = []
start = datetime(2026, 6, 1)
end = datetime(2026, 7, 3)
current = start
while current < end:
    chunk_end = min(current + timedelta(days=5), end)
    try:
        df = m.futures("VN30F1M").ohlcv(
            start=current.strftime("%Y-%m-%d"),
            end=chunk_end.strftime("%Y-%m-%d"),
            interval="5m",
            source="VCI"
        )
        if len(df):
            all_5m.append(df)
            print(f"  {current.date()} -> {chunk_end.date()}: {len(df)} rows")
    except Exception as e:
        print(f"  {current.date()} -> {chunk_end.date()}: error - {str(e)[:100]}")
    current = chunk_end
    ttime.sleep(0.5)

if all_5m:
    full_5m = pd.concat(all_5m, ignore_index=True)
    full_5m = full_5m.drop_duplicates(subset=["time"])
    full_5m = full_5m.sort_values("time")
    print(f"\nTotal 5m: {len(full_5m)} rows")
    print(f"Range: {full_5m['time'].min()} -> {full_5m['time'].max()}")
