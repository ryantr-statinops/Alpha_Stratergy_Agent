"""Quick test of vnstock futures data availability."""
from vnstock import Market

m = Market()

# Test VN30F2506 (June 2025 contract)
print("=== VN30F2506 (June 2025) ===")
df = m.futures("VN30F2506").ohlcv(start="2025-01-01", end="2025-06-30", interval="5m", source="VCI")
print(f"Shape: {df.shape}")
if len(df):
    print(f"Range: {df['time'].min()} -> {df['time'].max()}")
    print(f"Unique days: {df['time'].dt.date.nunique()}")

print()
print("=== VN30F2503 (March 2025) ===")
df = m.futures("VN30F2503").ohlcv(start="2024-12-01", end="2025-03-31", interval="5m", source="VCI")
print(f"Shape: {df.shape}")
if len(df):
    print(f"Range: {df['time'].min()} -> {df['time'].max()}")
    print(f"Unique days: {df['time'].dt.date.nunique()}")

print()
print("=== VN30F1M (generic current month) recent ===")
df = m.futures("VN30F1M").ohlcv(start="2026-06-01", end="2026-07-03", interval="5m", source="VCI")
print(f"Shape: {df.shape}")
if len(df):
    print(f"Range: {df['time'].min()} -> {df['time'].max()}")
    print(f"Unique days: {df['time'].dt.date.nunique()}")

print()
print("=== VN30F1M daily ===")
df = m.futures("VN30F1M").ohlcv(start="2022-01-01", end="2026-07-03", interval="1D", source="VCI")
print(f"Shape: {df.shape}")
if len(df):
    print(f"Range: {df['time'].min()} -> {df['time'].max()}")
    print(f"Unique days: {df['time'].dt.date.nunique()}")
