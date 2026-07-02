"""
Move output files into thesis group subfolders.
"""
import os
import csv

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
INDEX_PATH = os.path.join(OUTPUT_DIR, "index.csv")

THESIS_FOLDERS = {
    "01": "thesis_01_rolling_mean_quantile",
    "02": "thesis_02_volatility_regime",
    "03": "thesis_03_time_series_decomp",
    "04": "thesis_04_microstructure_flow",
    "05": "thesis_05_cross_market_correlation",
    "06": "thesis_06_multifactor_composite",
}

# Read index
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Create dirs
for folder in THESIS_FOLDERS.values():
    os.makedirs(os.path.join(OUTPUT_DIR, folder), exist_ok=True)

# Move files & update index
updated_rows = []
for r in rows:
    fname = r["filepath"]
    thesis = r["thesis_group"]
    folder = THESIS_FOLDERS.get(thesis, "other")
    src = os.path.join(OUTPUT_DIR, fname)
    dst = os.path.join(OUTPUT_DIR, folder, fname)
    if os.path.exists(src):
        os.rename(src, dst)
    r["filepath"] = f"{folder}/{fname}"
    updated_rows.append(r)

# Write updated index
with open(INDEX_PATH, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["filepath","thesis_group","template","timeframe","description","params"])
    writer.writeheader()
    writer.writerows(updated_rows)

print(f"OK Moved {len(updated_rows)} files into thesis folders")
for g, folder in sorted(THESIS_FOLDERS.items()):
    count = sum(1 for r in updated_rows if r["thesis_group"] == g)
    print(f"  thesis_{g}: {folder}/ -> {count} files")
print(f"\nIndex updated: {INDEX_PATH}")
