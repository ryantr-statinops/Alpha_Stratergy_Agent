"""Quick 5m data fetch: test 1 contract first."""
import os, sys, time, pandas as pd
from vnstock import Market

CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)
INTRADAY_PATH = os.path.join(CACHE_DIR, "vn30f_5m.parquet")

# First test with just 2 contracts
test_contracts = ["VN30F2503", "VN30F2506"]

m = Market()
all_data = []

for sym in test_contracts:
    print(f"Fetching {sym}...", flush=True)
    cur = pd.Timestamp("2025-01-01")
    end = pd.Timestamp("2025-06-30")
    sym_rows = 0
    while cur < end:
        chunk = min(cur + pd.Timedelta(days=5), end)
        try:
            df = m.futures(sym).ohlcv(
                start=cur.strftime("%Y-%m-%d"),
                end=chunk.strftime("%Y-%m-%d"),
                interval="5m", source="VCI"
            )
            if df is not None and len(df):
                all_data.append(df)
                sym_rows += len(df)
        except Exception as exc:
            safe = str(exc).encode("ascii", errors="replace").decode("ascii")
            print(f"  {cur.date()}: {safe[:100]}")
        cur = chunk
        time.sleep(0.3)
    print(f"  {sym}: {sym_rows} rows")

if all_data:
    full = pd.concat(all_data, ignore_index=True)
    full = full.drop_duplicates(subset=["time"]).sort_values("time").reset_index(drop=True)
    print(f"\nTotal: {len(full)} rows")
    print(f"Range: {full['time'].min()} -> {full['time'].max()}")
    print(f"Unique days: {full['time'].dt.date.nunique()}")
else:
    print("No data fetched")
