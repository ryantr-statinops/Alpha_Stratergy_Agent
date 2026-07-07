"""
Alpha Bot — Framework Compliance Validator
Checks generated strategies for framework compliance per strategy_framework.md
"""

import os
import re
import sys

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
INDEX_PATH = os.path.join(OUTPUT_DIR, "index.csv")

FORBIDDEN_PATTERNS = [
    (r'\bimport pandas\b',                    "import pandas is forbidden"),
    (r'\bSeriesT\b',                           "SeriesT type hint is forbidden"),
    (r'(?<!= )open\s*=',                       "'open =' as variable name is forbidden (use open_price)"),
    (r'\b__init__\s*\(',                       "__init__ is forbidden"),
    (r'[^.]np\.',                              "numpy import is forbidden"),
]

REQUIRED_STRUCTURE = [
    (r'class CustomStrategy\(SimpleAlgorithm\):', "Must extend SimpleAlgorithm"),
    (r'def __algorithm__\(self\):',                "Must have __algorithm__ method"),
    (r'self\.set_positions\(',                     "Must use self.set_positions()"),
]

SETPOSITION_ORDER = ["exit", "long", "short"]
SETPOSITION_PATTERN = re.compile(r'self\.set_positions\((\w+[^,]*),\s*position=([^)]+)\)')
VALID_POSITIONS = {0, 0.5, 1.0, -0.5, -1.0}

EXIT_KEYWORDS = re.compile(r'(exit|close_out)', re.IGNORECASE)
LONG_KEYWORDS = re.compile(r'(long_setup|long)', re.IGNORECASE)
SHORT_KEYWORDS = re.compile(r'(short_setup|short)', re.IGNORECASE)


def classify_var(name):
    """Guess whether a variable name is exit/long/short."""
    if EXIT_KEYWORDS.search(name):
        return "exit"
    if LONG_KEYWORDS.search(name):
        return "long"
    if SHORT_KEYWORDS.search(name):
        return "short"
    return None


def _try_float(val):
    try:
        return float(val)
    except ValueError:
        return None


def check_order(code: str, filepath: str) -> list:
    """Check that set_positions calls are in either
       Exit → Long → Short  (old convention) or
       Long → Short → Exit  (new convention, XNOQuant: exit must beat entries)."""
    lines = code.splitlines()
    findings = []
    calls = []
    for i, line in enumerate(lines, 1):
        m = SETPOSITION_PATTERN.search(line)
        if m:
            var_name = m.group(1).strip()
            raw_pos = m.group(2).strip()
            pos_val = _try_float(raw_pos)
            role = classify_var(var_name)
            calls.append((i, role, pos_val, var_name, raw_pos))

    if not calls:
        return findings

    first = calls[0]
    last = calls[-1]
    first_is_exit = first[1] == "exit" or (first[2] is not None and first[2] == 0)
    last_is_exit = last[1] == "exit" or (last[2] is not None and last[2] == 0)
    last_is_short = last[1] == "short" or (last[2] is not None and last[2] < 0)

    # New convention: Exit is last (beats long/short)
    if last_is_exit:
        # Validate new convention: first must be long, second must be short
        if len(calls) >= 2:
            second = calls[1]
            second_is_short = second[1] == "short" or (second[2] is not None and second[2] < 0)
            if not second_is_short:
                findings.append((
                    filepath, second[0],
                    f"Second set_positions (before exit) should be Short (position<0), got '{second[3]}' pos={second[4]}"
                ))
    # Old convention: Exit is first
    else:
        if not first_is_exit:
            findings.append((
                filepath, first[0],
                f"First set_positions should be Exit (position=0), got '{first[3]}' pos={first[4]}"
            ))
        if not last_is_short:
            findings.append((
                filepath, last[0],
                f"Last set_positions should be Short (position<0), got '{last[3]}' pos={last[4]}"
            ))

    # Check numeric positions are valid
    for line_no, role, pos_val, var_name, raw_pos in calls:
        if pos_val is not None and pos_val not in VALID_POSITIONS:
            findings.append((
                filepath, line_no,
                f"Invalid position {pos_val} in '{var_name}'"
            ))

    return findings


def validate_file(filepath: str) -> list:
    """Validate a single strategy file. Returns list of (file, line, issue)."""
    findings = []
    abspath = os.path.join(OUTPUT_DIR, filepath)
    if not os.path.exists(abspath):
        return [(filepath, 0, "File missing")]

    with open(abspath, "r", encoding="utf-8") as f:
        code = f.read()

    lines = code.splitlines()

    # Check required structure
    for pattern, msg in REQUIRED_STRUCTURE:
        if not re.search(pattern, code):
            findings.append((filepath, 1, f"Missing: {msg}"))

    # Check forbidden patterns
    for pattern, msg in FORBIDDEN_PATTERNS:
        m = re.search(pattern, code)
        if m:
            line_no = 1 + code[:m.start()].count("\n")
            findings.append((filepath, line_no, f"Forbidden: {msg}"))

    # Check set_positions order
    findings.extend(check_order(code, filepath))

    # Check open variable naming
    for i, line in enumerate(lines, 1):
        # Check for bare 'open =' assignment
        if re.match(r'^\s*open\s*=\s', line) and 'open_price' not in line and 'open_' not in line:
            findings.append((filepath, i, "Uses 'open' as variable name"))

    return findings


def validate_index():
    """Check index.csv matches files on disk."""
    findings = []
    if not os.path.exists(INDEX_PATH):
        return [("index.csv", 0, "Index file missing")]

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if len(lines) < 2:
        return [("index.csv", 1, "Index has no data rows")]

    header = lines[0].strip().split(",")
    if header != ["filepath", "thesis_group", "template", "timeframe", "description", "params"]:
        return [("index.csv", 1, f"Unexpected header: {header}")]

    indexed_files = set()
    for i, line in enumerate(lines[1:], 2):
        parts = line.strip().split(",")
        if not parts:
            continue
        fname = parts[0]
        indexed_files.add(fname)
        abspath = os.path.join(OUTPUT_DIR, fname)
        if not os.path.exists(abspath):
            findings.append(("index.csv", i, f"Index references missing file: {fname}"))

    # Check for files not in index
    actual_files = {f for f in os.listdir(OUTPUT_DIR) if f.endswith(".py")}
    orphaned = actual_files - indexed_files
    for f in sorted(orphaned):
        findings.append(("index.csv", 0, f"File not in index: {f}"))

    return findings


def main():
    if not os.path.exists(OUTPUT_DIR):
        print(f"Error: Output directory not found: {OUTPUT_DIR}")
        print("Run tools/generate_strategies.py first.")
        sys.exit(1)

    all_findings = []

    # 1. Validate index
    print("Checking index.csv...")
    all_findings.extend(validate_index())

    # 2. Validate each .py file (search recursively)
    print("Checking strategy files...")
    py_files = []
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for f in files:
            if f.endswith(".py"):
                rel = os.path.relpath(os.path.join(root, f), OUTPUT_DIR)
                py_files.append(rel)
    py_files = sorted(py_files)
    for fname in py_files:
        findings = validate_file(fname)
        all_findings.extend(findings)

    # 3. Report
    errors = [f for f in all_findings if any(
        kw in f[2] for kw in ["Error", "Missing", "Forbidden", "Invalid", "Uses"]
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
