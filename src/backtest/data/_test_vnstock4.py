"""Try to get more data via different approaches."""
from vnstock import Market, Listing
import pandas as pd

m = Market()
listing = Listing(source="KBS")

# 1. List all available future indices
print("=== All future indices ===")
try:
    fut_list = listing.all_future_indices()
    print(fut_list.head(20))
    print(f"Total: {len(fut_list)}")
except Exception as e:
    print(f"Error: {e}")

print()
print("=== Try VN30 index data ===")
try:
    df = m.stock("VN30").ohlcv(start="2022-01-01", end="2022-12-31", interval="1D", source="VCI")
    print(f"VN30 daily: {len(df)} rows, {df['time'].min()} -> {df['time'].max()}")
except Exception as e:
    print(f"Error: {e}")

print()
print("=== Try TCBS source for futures ===")
try:
    df = m.futures("VN30F1M").ohlcv(start="2022-01-01", end="2022-12-31", interval="1D", source="TCBS")
    print(f"TCBS futures: {len(df)} rows")
    if len(df):
        print(f"  {df['time'].min()} -> {df['time'].max()}")
except Exception as e:
    print(f"Error: {e}")

print()
print("=== Try MSN source for futures ===")
try:
    df = m.futures("VN30F1M").ohlcv(start="2022-01-01", end="2022-12-31", interval="1D", source="MSN")
    print(f"MSN futures: {len(df)} rows")
    if len(df):
        print(f"  {df['time'].min()} -> {df['time'].max()}")
except Exception as e:
    print(f"Error: {e}")

print()
print("=== Chunked daily via VCI ===")
import time as ttime
all_daily = []
cur = pd.Timestamp("2022-01-01")
end = pd.Timestamp("2026-07-03")
while cur < end:
    chunk = min(cur + pd.Timedelta(days=60), end)
    try:
        df = m.futures("VN30F1M").ohlcv(
            start=cur.strftime("%Y-%m-%d"),
            end=chunk.strftime("%Y-%m-%d"),
            interval="1D", source="VCI"
        )
        if len(df):
            all_daily.append(df)
            print(f"  {cur.date()} -> {chunk.date()}: {len(df)} rows")
    except:
        pass  # skip encoding errors
    cur = chunk
    ttime.sleep(0.3)

if all_daily:
    full = pd.concat(all_daily, ignore_index=True)
    full = full.drop_duplicates(subset=["time"]).sort_values("time")
    print(f"\nTotal daily: {len(full)} rows")
    print(f"Range: {full['time'].min()} -> {full['time'].max()}")
    # Save to CSV
    full.to_parquet("backtest/data/cache/vn30f1m_daily.parquet", index=False)
    print("Saved to backtest/data/cache/vn30f1m_daily.parquet")
