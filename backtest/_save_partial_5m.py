"""Save the 5m data we already fetched via _test_contract_chunks.py."""
import pandas as pd
import os

# The earlier test saved to this path
src = "backtest/data/cache/vn30f2506_5m_test.parquet"
dst = "backtest/data/cache/vn30f_5m.parquet"

if os.path.exists(src):
    df = pd.read_parquet(src)
    print(f"Found partial 5m data: {len(df)} rows")
    print(f"  Range: {df['time'].min()} -> {df['time'].max()}")
    print(f"  Unique days: {df['time'].dt.date.nunique()}")
    df.to_parquet(dst, index=False)
    print(f"Saved to {dst}")
else:
    print("No partial 5m data found")
