#!/usr/bin/env python3
"""Pre-submit gate pipeline (Pha E).

Chains the offline gates before an alpha may be submitted:

  1. validate_framework.py --strict   (syntax compliance)
  2. factor_diagnostics.py            (Layer 3 -- factor quality / field validity)
  3. economic_validation.py           (Layer 4 -- data truth / freq consistency)

Emits PASS/BLOCK and alerts risky idioms, notably the financial-gate pattern
`(x >= 0) | (x < 0)` which is True on missing-filled-0 panels and empties the
eligible universe -> the root cause of 16 zero files.

Read-only: parses .py + CSVs; never calls the submit API.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
UNIVERSES = ("vn_large_cap", "vn_mid_cap", "vn_small_cap")


def iter_alpha_files(universe=None):
    us = [universe] if universe else list(UNIVERSES)
    for u in us:
        base = os.path.join(ROOT, "output", "stage_2", u, "cross_sectional")
        if not os.path.isdir(base):
            continue
        for fn in sorted(os.listdir(base)):
            if fn.endswith(".py"):
                yield u, fn, os.path.join(base, fn)


def check_bad_gates(src: str) -> list[str]:
    """Detect `is_financial` bound built from (>= 0)/(< 0) comparisons."""
    hits = []
    for m in re.finditer(r"is_financial\s*=\s*([^\n]+)", src):
        block = m.group(1)
        if re.search(r">=\s*0\s*\)\s*\|", block) or re.search(r"<\s*0\s*\)", block):
            hits.append("is_financial built from (>=0)|(<0) -> True on fill-0 panels")
    return hits


def run_python(name, args=()):
    try:
        p = subprocess.run([sys.executable, os.path.join(TOOLS, name), *args],
                           cwd=ROOT, capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr
    except Exception as e:  # noqa: BLE001
        return 1, "error running %s: %s" % (name, e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pattern", default=r"Vn[A-Za-z0-9]+\.py",
                    help="filename regex to select which alphas to audit")
    ap.add_argument("--universe", choices=UNIVERSES, default=None)
    ap.add_argument("--skip-validate", action="store_true")
    ap.add_argument("--skip-d3", action="store_true")
    ap.add_argument("--skip-d4", action="store_true")
    args = ap.parse_args()

    print("=" * 70)
    print("Layer-Q gate (validate_framework + L3 diagnostics + L4 validation)")
    print("=" * 70)

    verdict_ok = True

    if not args.skip_validate:
        rc, out = run_python("validate_framework.py", ["--strict"])
        print("\n[1/3] validate_framework --strict:", "PASS" if rc == 0 else "FAIL")
        if rc != 0:
            print(out[-2000:])
            verdict_ok = False

    if not args.skip_d3:
        rc, _ = run_python("factor_diagnostics.py")
        print("[2/3] Layer 3 factor_diagnostics:", "PASS" if rc == 0 else "FAIL")

    if not args.skip_d4:
        rc, _ = run_python("economic_validation.py")
        print("[3/3] Layer 4 economic_validation:", "PASS" if rc == 0 else "FAIL")

    pat = re.compile(args.pattern)
    risky = []
    for _u, fn, path in iter_alpha_files(args.universe):
        if not pat.search(fn) or not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as fh:
            bad = check_bad_gates(fh.read())
        if bad:
            risky.append((fn, bad))

    if risky:
        verdict_ok = False
        print("\n[ALERT] %d file(s) with zero-universe financial-gate idiom:"
              % len(risky))
        for fn, bad in risky:
            print("  - %s :: %s" % (fn, "; ".join(bad)))

    print("\n" + "=" * 70)
    print("VERDICT:", "PASS (eligible to submit)" if verdict_ok
          else "BLOCK (fix before submit)")
    sys.exit(0 if verdict_ok else 1)


if __name__ == "__main__":
    main()