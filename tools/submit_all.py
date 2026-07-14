#!/usr/bin/env python3
"""
Batch submit all strategy variants to alpha.xnoquant.io via XNOQuant API.

Usage:
    1. Open https://alpha.xnoquant.io/build in Chrome
    2. Open DevTools → Network tab → filter Fetch/XHR
    3. Paste any code into editor, look for request named "update" or "editor"
    4. Right-click → Copy → Copy as cURL (bash)
    5. Extract EDITOR_ID (UUID after /editors/) and TOKEN (Bearer ...)
    6. Update the two constants below
    7. Run: python tools/submit_all.py

    Optionally pass --test to submit only 1 variant:
        python tools/submit_all.py --test
"""

import requests
import glob
import json
import time
import os
import sys
from datetime import datetime

# ── CONFIG ── UPDATE THESE BEFORE RUNNING ──
EDITOR_ID = "a1619c25-f370-4461-9d47-ddfd2deb66dc"
TOKEN = "xq_pnLDPtb8VvmwVYPMnVDZehjSqsx1K8hr2vU"
# NOTE: Copy từ DevTools Network tab mỗi session — UUID và token có thể thay đổi
# ──────────────────────────────────────────

BASE = f"https://api.xnoquant.io/xalpha-api/v2/editors/{EDITOR_ID}"
HEADERS = {
    "accept": "application/json",
    "authorization": f"Bearer {TOKEN}",
    "content-type": "application/json",
    "origin": "https://alpha.xnoquant.io",
    "referer": "https://alpha.xnoquant.io/",
}
DELAY = 10

session = requests.Session()
session.headers.update(HEADERS)


def submit_one(fpath: str, index: int, total: int) -> str:
    with open(fpath, encoding="utf-8") as f:
        code = f.read()

    name = os.path.basename(fpath)
    payload = {"code": code}

    r1 = session.put(f"{BASE}/update", json=payload)
    r2 = session.post(f"{BASE}/verify")
    r3 = session.post(f"{BASE}/simulate")

    status = f"{r1.status_code}/{r2.status_code}/{r3.status_code}"
    ok = all(s == 200 or s == 201 or s == 204 for s in (r1.status_code, r2.status_code, r3.status_code))
    marker = "OK" if ok else "FAIL"
    print(f"[{index}/{total}] {marker} {status}  {name}")
    return marker


def main():
    files = sorted(glob.glob("output/thesis_*/**/*.py", recursive=True))
    total = len(files)
    print(f"Found {total} variants to submit")

    if not files:
        print("No .py files found in output/thesis_*/")
        return

    is_test = "--test" in sys.argv
    if is_test:
        files = files[:1]
        total = len(files)
        print("--- TEST MODE: submitting 1 variant only ---")

    results = {"OK": 0, "FAIL": 0}
    start = time.time()

    for i, fpath in enumerate(files, 1):
        try:
            marker = submit_one(fpath, i, total)
            results[marker] += 1
        except requests.exceptions.RequestException as e:
            print(f"[{i}/{total}] ERROR {os.path.basename(fpath)}: {e}")
            results["FAIL"] += 1

        if i < total:
            time.sleep(DELAY)

    elapsed = time.time() - start
    print(f"\nDone in {elapsed:.0f}s")
    print(f"  OK:   {results['OK']}")
    print(f"  FAIL: {results['FAIL']}")


if __name__ == "__main__":
    main()
