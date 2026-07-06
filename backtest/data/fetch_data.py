"""Data pipeline: fetch, cache, and serve VN30F futures data from vnstock."""
import os
import time
import pandas as pd
from vnstock import Market

CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

DAILY_PATH = os.path.join(CACHE_DIR, "vn30f_daily.parquet")
INTRADAY_PATH = os.path.join(CACHE_DIR, "vn30f_5m.parquet")


def _contract_codes(start_year=2022, end_year=2026):
    codes = []
    for y in range(start_year, end_year + 1):
        for m in ["03", "06", "09", "12"]:
            codes.append(f"VN30F{y}{m}")
    return codes


def fetch_daily(start="2022-01-01", end="2026-07-03", force=False):
    if os.path.exists(DAILY_PATH) and not force:
        df = pd.read_parquet(DAILY_PATH)
        print(f"[data] Loaded {len(df)} daily rows from cache")
        return df
    m = Market()
    all_data = []
    cur = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)
    while cur < end_ts:
        chunk = min(cur + pd.Timedelta(days=60), end_ts)
        try:
            df = m.futures("VN30F1M").ohlcv(
                start=cur.strftime("%Y-%m-%d"),
                end=chunk.strftime("%Y-%m-%d"),
                interval="1D", source="VCI"
            )
            if df is not None and len(df):
                all_data.append(df)
                print(f"  daily {cur.date()} -> {chunk.date()}: {len(df)} rows")
        except Exception:
            pass
        cur = chunk
        time.sleep(0.3)
    if not all_data:
        print("[data] No daily data fetched")
        return pd.DataFrame()
    full = pd.concat(all_data, ignore_index=True)
    full = full.drop_duplicates(subset=["time"]).sort_values("time").reset_index(drop=True)
    full.to_parquet(DAILY_PATH, index=False)
    print(f"[data] Daily: {len(full)} rows, {full['time'].min()} -> {full['time'].max()}")
    return full


def _contract_active_range(contract_code):
    """Estimate when a quarterly contract was actively traded."""
    yy = int(contract_code[-4:-2]) + 2000
    mm = int(contract_code[-2:])
    # Approximate active window: 3 months before expiry → ~20th of expiry month
    if mm == 3:
        return pd.Timestamp(f"{yy-1}-11-20"), pd.Timestamp(f"{yy}-03-21")
    elif mm == 6:
        return pd.Timestamp(f"{yy}-02-20"), pd.Timestamp(f"{yy}-06-21")
    elif mm == 9:
        return pd.Timestamp(f"{yy}-05-20"), pd.Timestamp(f"{yy}-09-21")
    else:  # 12
        return pd.Timestamp(f"{yy}-08-20"), pd.Timestamp(f"{yy}-12-21")


def fetch_5m(start="2022-01-01", end="2026-07-03", force=False):
    if os.path.exists(INTRADAY_PATH) and not force:
        df = pd.read_parquet(INTRADAY_PATH)
        print(f"[data] Loaded {len(df)} 5m rows from cache")
        return df

    contracts = _contract_codes()
    m = Market()
    all_data = []
    chunk_days = 5

    for sym in contracts:
        c_start, c_end = _contract_active_range(sym)
        c_start = max(c_start, pd.Timestamp(start))
        c_end = min(c_end, pd.Timestamp(end))
        if c_start >= c_end:
            continue

        cur = c_start
        sym_rows = 0
        while cur < c_end:
            chunk = min(cur + pd.Timedelta(days=chunk_days), c_end)
            try:
                df = m.futures(sym).ohlcv(
                    start=cur.strftime("%Y-%m-%d"),
                    end=chunk.strftime("%Y-%m-%d"),
                    interval="5m", source="VCI"
                )
                if df is not None and len(df):
                    all_data.append(df)
                    sym_rows += len(df)
            except Exception:
                pass
            cur = chunk
            time.sleep(3.5)  # rate limit: max 20 req/min for guest tier
        if sym_rows > 0:
            print(f"  {sym}: {sym_rows:5d} rows", flush=True)

    if not all_data:
        print("[data] No 5m data fetched")
        return pd.DataFrame()

    full = pd.concat(all_data, ignore_index=True)
    full = full.drop_duplicates(subset=["time"]).sort_values("time").reset_index(drop=True)
    full.to_parquet(INTRADAY_PATH, index=False)
    print(f"[data] 5m: {len(full)} rows, {full['time'].min()} -> {full['time'].max()}")
    print(f"[data]   Unique days: {full['time'].dt.date.nunique()}")
    return full


def load_5m():
    return pd.read_parquet(INTRADAY_PATH)


def load_daily():
    return pd.read_parquet(DAILY_PATH)


def resample(df_5m, rule):
    """Resample 5m data to higher timeframe. rule: '15min', '30min', '60min'."""
    if df_5m.empty:
        return df_5m
    df = df_5m.copy().set_index("time")
    ohlc = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
    rs = df.resample(rule, label="right", closed="right").agg(ohlc)
    rs = rs.dropna(subset=["open"]).reset_index()
    return rs


if __name__ == "__main__":
    print("Fetching daily data...")
    d = fetch_daily(force=True)
    print(f"  Got {len(d)} daily rows")

    print("\nFetching 5m data (this may take several minutes)...")
    i = fetch_5m(force=True)
    print(f"  Got {len(i)} 5m rows")
