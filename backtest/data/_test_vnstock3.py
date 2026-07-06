"""Test vnstock 5m data by contract code."""
import sys
from vnstock import Market

m = Market()

# Try known specific contract codes
contracts = [
    ("VN30F2403", "2024-01-01", "2024-03-31"),
    ("VN30F2406", "2024-04-01", "2024-06-30"),
    ("VN30F2409", "2024-07-01", "2024-09-30"),
    ("VN30F2412", "2024-10-01", "2024-12-31"),
    ("VN30F2503", "2025-01-01", "2025-03-31"),
    ("VN30F2506", "2025-04-01", "2025-06-30"),
]

for sym, s, e in contracts:
    try:
        df = m.futures(sym).ohlcv(start=s, end=e, interval="5m", source="VCI")
        print(f"{sym}: {len(df)} rows", flush=True)
        if len(df) > 0:
            print(f"  {df['time'].min()} -> {df['time'].max()}", flush=True)
    except Exception as exc:
        msg = str(exc)
        # Try to print error without vietnamese chars
        safe = msg.encode('ascii', errors='replace').decode('ascii')
        print(f"{sym}: ERROR - {safe[:200]}", flush=True)

print()
print("=== Try daily for full history ===", flush=True)

# Get daily data for VN30F1M
try:
    df = m.futures("VN30F1M").ohlcv(start="2022-01-01", end="2026-07-03", interval="1D", source="VCI")
    print(f"Daily: {len(df)} rows", flush=True)
    if len(df) > 0:
        print(f"  {df['time'].min()} -> {df['time'].max()}", flush=True)
except Exception as exc:
    msg = str(exc)
    safe = msg.encode('ascii', errors='replace').decode('ascii')
    print(f"Daily ERROR: {safe[:200]}", flush=True)
