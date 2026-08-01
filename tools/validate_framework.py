"""
Alpha Bot — Framework Compliance Validator V2 (Round 2: Fundamental Alpha Arena)
Checks generated strategies in output/stage_2/ for round-2 framework compliance
per agent/framework_build_guide.md + template_example/strategy_framework.md.

V2 additions:
- Quét output/stage_2/ (không phải toàn bộ output) + manifest output/index.csv (round 2).
- Detect mode tự động: cross_sectional (set_portfolio_positions) vs time_series (set_positions).
- Bounds theo mode: time_series long-only [0, +1]; cross_sectional market-neutral.
- Field suffix theo mode: time_series không _panel, cross_sectional phải _panel.
- Point-in-time: cấm global aggregations (mean/rank/quantile/sort_values), loops/lambdas.
"""

import os
import re
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(ROOT_DIR, "output", "stage_2")
INDEX_PATH = os.path.join(ROOT_DIR, "output", "index.csv")

FORBIDDEN_PATTERNS = [
    (r'\bimport pandas\b',                    "import pandas is forbidden"),
    (r'\bSeriesT\b',                           "SeriesT type hint is forbidden"),
    (r'(?<!= )open\s*=',                       "'open =' as variable name is forbidden (use open_price)"),
    (r'\b__init__\s*\(',                       "__init__ is forbidden"),
    (r'[^.]np\.',                              "numpy import is forbidden"),
    (r'\bfor\b.*\bin\b',                       "loops are forbidden (vectorized only)"),
    (r'\blambda\b',                            "lambda is forbidden"),
    (r'\.apply\(',                             ".apply() is forbidden (vectorized only)"),
]

# Global aggregations break point-in-time / cross-sectional neutrality
FORBIDDEN_AGGREGATIONS = [
    (r'\.mean\(\)',                            "global .mean() is forbidden (point-in-time)"),
    (r'\.median\(\)',                          "global .median() is forbidden (point-in-time)"),
    (r'\.rank\(\)',                            "global .rank() is forbidden (use feat/op panel ops)"),
    (r'\.quantile\(',                          "global .quantile() is forbidden (point-in-time)"),
    (r'\.sort_values\(',                       "global .sort_values() is forbidden"),
    (r'\.max\(\)',                             "global .max() is forbidden (use rolling/panel ops)"),
    (r'\.min\(\)',                             "global .min() is forbidden (use rolling/panel ops)"),
]

# Round-2 entry points
SET_POSITIONS = re.compile(r'self\.set_positions\(')
SET_PORTFOLIO_POSITIONS = re.compile(r'self\.set_portfolio_positions\(')

REQUIRED_STRUCTURE = [
    (r'class CustomStrategy\(SimpleAlgorithm\):', "Must extend SimpleAlgorithm"),
    (r'def __algorithm__\(self\):',                "Must have __algorithm__ method"),
]

VALID_TS_POSITIONS = {0, 0.5, 1.0}
POSITION_VALUE = re.compile(r'self\.set_positions\([^,]+,\s*position=([^)]+)\)')

# Field access patterns: self.data.<field>, self.feat.<field>
DATA_FIELD = re.compile(r'self\.data\.([A-Za-z0-9_]+)')
FEAT_FIELD = re.compile(r'self\.feat\.([A-Za-z0-9_]+)')
PANEL_OP = re.compile(r'self\.(?:op|feat)\.[A-Za-z0-9_]*panel')

INDEX_HEADER = ["filepath", "thesis_group", "template", "mode", "universe", "description", "params"]


def detect_mode(code: str):
    """Return 'cross_sectional', 'time_series', or None."""
    if SET_PORTFOLIO_POSITIONS.search(code):
        return "cross_sectional"
    if SET_POSITIONS.search(code):
        return "time_series"
    return None


def _line_of(code: str, match) -> int:
    return 1 + code[:match.start()].count("\n")


def check_field_suffix(code: str, filepath: str, mode: str) -> list:
    """Round-2 mode contract: field suffix must match mode."""
    findings = []
    fields = []
    fields += DATA_FIELD.findall(code)
    fields += FEAT_FIELD.findall(code)

    for f in sorted(set(fields)):
        if f.endswith("_panel"):
            if mode == "time_series":
                findings.append((filepath, 0, f"Mode contract: time_series must NOT use _panel field '{f}'"))
        else:
            if mode == "cross_sectional":
                findings.append((filepath, 0, f"Mode contract: cross_sectional must use _panel field '{f}'"))
    return findings


def check_positions(code: str, filepath: str, mode: str) -> list:
    """Check entry point + position bounds per mode."""
    findings = []

    if mode == "cross_sectional":
        if SET_POSITIONS.search(code):
            findings.append((filepath, 0, "Mode contract: cross_sectional must use set_portfolio_positions, not set_positions"))
    elif mode == "time_series":
        if SET_PORTFOLIO_POSITIONS.search(code):
            findings.append((filepath, 0, "Mode contract: time_series must use set_positions, not set_portfolio_positions"))
        # Long-only bounds [0, +1]
        for m in POSITION_VALUE.finditer(code):
            raw = m.group(1).strip()
            try:
                val = float(raw)
            except ValueError:
                continue
            if val not in VALID_TS_POSITIONS:
                msg = f"Invalid time_series position {val} (allowed: 0 / 0.5 / 1.0)"
                if val < 0:
                    msg = f"time_series is long-only, found negative position {val}"
                findings.append((filepath, _line_of(code, m), msg))
    else:
        findings.append((filepath, 0, "Missing entry point: need set_positions (time_series) or set_portfolio_positions (cross_sectional)"))

    return findings


def validate_file(filepath: str) -> list:
    """Validate a single strategy file. Returns list of (file, line, issue)."""
    findings = []
    abspath = os.path.join(OUTPUT_DIR, *filepath.split("/"))
    if not os.path.exists(abspath):
        return [(filepath, 0, "File missing")]

    with open(abspath, "r", encoding="utf-8") as f:
        code = f.read()

    # Required structure
    for pattern, msg in REQUIRED_STRUCTURE:
        if not re.search(pattern, code):
            findings.append((filepath, 1, f"Missing: {msg}"))

    # Forbidden patterns
    for pattern, msg in FORBIDDEN_PATTERNS:
        m = re.search(pattern, code)
        if m:
            findings.append((filepath, _line_of(code, m), f"Forbidden: {msg}"))

    # Forbidden global aggregations (point-in-time)
    for pattern, msg in FORBIDDEN_AGGREGATIONS:
        m = re.search(pattern, code)
        if m:
            findings.append((filepath, _line_of(code, m), f"Point-in-time: {msg}"))

    # Mode contract
    mode = detect_mode(code)
    if mode is None:
        findings.append((filepath, 0, "Cannot detect mode: no entry point found"))
    else:
        findings.extend(check_field_suffix(code, filepath, mode))
        findings.extend(check_positions(code, filepath, mode))

    return findings


def validate_index() -> list:
    """Check output/index.csv (round-2 manifest) matches files on disk."""
    findings = []
    if not os.path.exists(INDEX_PATH):
        # Index will be created as strategies are written — not an error yet
        return [("index.csv", 0, "Index file missing (will be created when strategies are written)")]

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if len(lines) < 2:
        # Empty index is fine only if there are no strategy files yet
        has_py = any(f.endswith(".py") for f in os.listdir(OUTPUT_DIR))
        if has_py:
            return [("index.csv", 1, "Index has no data rows but strategy files exist")]
        return []

    header = lines[0].strip().split(",")
    if header != INDEX_HEADER:
        return [("index.csv", 1, f"Unexpected header {header} (expected {INDEX_HEADER})")]

    indexed_files = set()
    for i, line in enumerate(lines[1:], 2):
        parts = line.strip().split(",")
        if not parts:
            continue
        fname = parts[0]
        indexed_files.add(fname)
        abspath = os.path.join(OUTPUT_DIR, *fname.split("/"))
        if not os.path.exists(abspath):
            findings.append(("index.csv", i, f"Index references missing file: {fname}"))

    actual_files = set()
    for root, _dirs, files in os.walk(OUTPUT_DIR):
        for f in files:
            if f.endswith(".py"):
                rel = os.path.relpath(os.path.join(root, f), OUTPUT_DIR).replace("\\", "/")
                actual_files.add(rel)
    orphaned = actual_files - indexed_files
    for f in sorted(orphaned):
        findings.append(("index.csv", 0, f"File not in index: {f}"))

    return findings


def main():
    if not os.path.exists(OUTPUT_DIR):
        print(f"Error: Output directory not found: {OUTPUT_DIR}")
        print("Round-2 strategies live in output/stage_2/.")
        sys.exit(1)

    all_findings = []

    print("Checking output/index.csv (round-2 manifest)...")
    all_findings.extend(validate_index())

    print("Checking strategy files in output/stage_2/...")
    py_files = []
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for f in files:
            if f.endswith(".py"):
                rel = os.path.relpath(os.path.join(root, f), OUTPUT_DIR)
                py_files.append(rel)
    py_files = sorted(py_files)
    for fname in py_files:
        all_findings.extend(validate_file(fname))

    errors = [f for f in all_findings if any(
        kw in f[2] for kw in ["Error", "Missing", "Forbidden", "Invalid", "Uses", "Mode contract", "Point-in-time", "Cannot detect", "long-only"]
    )]
    warnings = [f for f in all_findings if f not in errors]

    print(f"\nResults:")
    print(f"  Files checked: {len(py_files)}")
    print(f"  Issues found: {len(all_findings)}")

    if errors:
        print(f"\n  ERRORS ({len(errors)}):")
        for fname, line, msg in sorted(errors):
            print(f"    {fname}:{line} — {msg}")

    if warnings:
        print(f"\n  WARNINGS ({len(warnings)}):")
        for fname, line, msg in sorted(warnings):
            print(f"    {fname}:{line} — {msg}")

    if not errors and not warnings:
        print("\n  All checks passed!")
        return 0
    elif not errors:
        print("\n  No errors (warnings only).")
        return 0
    else:
        print(f"\n  {len(errors)} error(s) found.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
