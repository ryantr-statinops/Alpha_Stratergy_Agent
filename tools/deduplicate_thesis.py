import csv
import os
from collections import defaultdict

CSV_PATH = os.path.join("output", "index.csv")

rows = []
with open(CSV_PATH, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

groups = defaultdict(list)
for row in rows:
    groups[row["template"]].append(row)

total_kept = 0
total_deleted = 0

for template, files in sorted(groups.items()):
    fifteen_min = [f for f in files if f["timeframe"] == "15min"]
    others = [f for f in files if f["timeframe"] != "15min"]

    if fifteen_min:
        keep = [fifteen_min[0]]
        if len(fifteen_min) > 2:
            mid_idx = len(fifteen_min) // 2
            keep.append(fifteen_min[mid_idx])
        elif len(fifteen_min) > 1:
            keep.append(fifteen_min[1])
        delete = fifteen_min[len(keep):] + others
    else:
        keep = [files[0]]
        delete = files[1:]

    for row in delete:
        fpath = os.path.join("output", row["filepath"])
        if os.path.isfile(fpath):
            os.remove(fpath)
            total_deleted += 1
    total_kept += len(keep)

print(f"Kept: {total_kept}, Deleted: {total_deleted}")
