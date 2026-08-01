"""
Alpha Bot — Framework Compliance Validator V2 (Round 2: Fundamental Alpha Arena)
Checks generated strategies in output/stage_2/ for round-2 framework compliance
per agent/stage_2_guideline.md + template_example/strategy_framework.md.

V2 additions:
- Quét output/stage_2/ (không phải toàn bộ output) + manifest output/index.csv (round 2).
- Detect mode tự động: cross_sectional (set_portfolio_positions) vs time_series (set_positions).
- Bounds theo mode: time_series long-only [0, +1]; cross_sectional market-neutral.
- Field suffix theo mode: time_series không _panel, cross_sectional phải _panel.
- Point-in-time: cấm global aggregations (mean/rank/quantile/sort_values), loops/lambdas.

V3 additions:
- Manifest parse bằng csv.DictReader (description chứa dấu phẩy).
- Validate filepath format <cap>/<mode>/<file>.py + cap->universe + mode consistency
  (path vs manifest vs code entry point).
- Reject invalid universe/mode/duplicate filepath; empty manifest dùng os.walk.
- Forbidden: shift âm, backfill, centered windows, print/eval/exec, import bất kỳ.
- Fundamental guard: ratio/divide fundamental không có .notna() + denominator > 0 (error trong strict).
- time_series position: chấp nhận mọi numeric trong [0,1]; dynamic -> warning.
- cross_sectional: bắt buộc portfolio_weights_panel + mask + method hợp lệ.
- --strict: warnings trở thành errors (exit 1).
"""

import argparse
import csv
import os
import re
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(ROOT_DIR, "output", "stage_2")
INDEX_PATH = os.path.join(ROOT_DIR, "output", "index.csv")

CAP_TO_UNIVERSE = {
    "vn_small_cap": "VN-SMALL-CAP",
    "vn_mid_cap": "VN-MID-CAP",
    "vn_large_cap": "VN-LARGE-CAP",
}
UNIVERSE_TO_CAP = {v: k for k, v in CAP_TO_UNIVERSE.items()}
VALID_MODES = {"time_series", "cross_sectional"}
VALID_UNIVERSES = set(CAP_TO_UNIVERSE.values())

FORBIDDEN_PATTERNS = [
    (r'^\s*(import|from)\s',               "import statements are forbidden in strategy files"),
    (r'\bimport pandas\b',                 "import pandas is forbidden"),
    (r'\bSeriesT\b',                       "SeriesT type hint is forbidden"),
    (r'(?<!= )open\s*=',                   "'open =' as variable name is forbidden (use open_price)"),
    (r'\b__init__\s*\(',                   "__init__ is forbidden"),
    (r'[^.]np\.',                          "numpy import is forbidden"),
    (r'\bfor\b.*\bin\b',                   "loops are forbidden (vectorized only)"),
    (r'\[[^\]]*\bfor\b[^\]]*\bin\b',       "list/dict comprehensions are forbidden"),
    (r'\blambda\b',                        "lambda is forbidden"),
    (r'\.apply\(',                         ".apply() is forbidden (vectorized only)"),
    (r'\bprint\s*\(',                      "print() is forbidden (hidden runtime access)"),
    (r'\beval\s*\(',                       "eval() is forbidden (hidden runtime access)"),
    (r'\bexec\s*\(',                       "exec() is forbidden (hidden runtime access)"),
    (r'\bopen\s*\(',                       "open() file access is forbidden"),
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

# Point-in-time: look-ahead constructs
FORBIDDEN_TIMING = [
    (r'\.shift\s*\(\s*-',                  "negative shift is forbidden (future observation)"),
    (r'\.bfill\s*\(',                       "backfill is forbidden (future observation)"),
    (r'\bbackfill\b',                       "backfill is forbidden (future observation)"),
    (r'center\s*=\s*True',                  "centered rolling window is forbidden (future observation)"),
]

# Round-2 entry points
SET_POSITIONS = re.compile(r'self\.set_positions\(')
SET_PORTFOLIO_POSITIONS = re.compile(r'self\.set_portfolio_positions\(')
PORTFOLIO_WEIGHTS = re.compile(r'self\.op\.portfolio_weights_panel\(')

REQUIRED_STRUCTURE = [
    (r'class CustomStrategy\(SimpleAlgorithm\):', "Must extend SimpleAlgorithm"),
    (r'def __algorithm__\(self\):',                "Must have __algorithm__ method"),
]

POSITION_VALUE = re.compile(r'self\.set_positions\([^,]+,\s*position=([^)]+)\)')
DATA_FIELD = re.compile(r'self\.data\.([A-Za-z0-9_]+)')
FEAT_FIELD = re.compile(r'self\.feat\.([A-Za-z0-9_]+)')

# Approved cross-sectional weighting methods (stage_2_guideline.md §5)
APPROVED_CS_METHODS = {"rank_demean_l1", "demean_l1"}

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


def parse_filepath(filepath: str):
    """Return (cap, mode, fname) or (None, None, None) if the layout is wrong."""
    parts = filepath.replace("\\", "/").split("/")
    if len(parts) != 3:
        return None, None, None
    cap, mode, fname = parts
    if cap not in CAP_TO_UNIVERSE:
        return None, None, None
    if mode not in VALID_MODES:
        return None, None, None
    if not fname.endswith(".py"):
        return None, None, None
    return cap, mode, fname


def check_field_suffix(code: str, filepath: str, mode: str) -> list:
    """Round-2 mode contract: DATA field suffix must match mode."""
    findings = []
    fields = DATA_FIELD.findall(code)
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
        if not PORTFOLIO_WEIGHTS.search(code):
            findings.append((filepath, 0, "cross_sectional: missing self.op.portfolio_weights_panel(...)"))
        # method=... must be approved
        m = re.search(r'method\s*=\s*[\'"]([A-Za-z0-9_]+)[\'"]', code)
        if m and m.group(1) not in APPROVED_CS_METHODS:
            findings.append((filepath, _line_of(code, m), f"cross_sectional: unsupported weighting method '{m.group(1)}'"))
        # mask= must be provided
        if not re.search(r'mask\s*=', code):
            findings.append((filepath, 0, "cross_sectional: portfolio_weights_panel requires a mask="))
    elif mode == "time_series":
        if SET_PORTFOLIO_POSITIONS.search(code):
            findings.append((filepath, 0, "Mode contract: time_series must use set_positions, not set_portfolio_positions"))
        # Long-only bounds [0, +1] — accept any numeric in range; dynamic -> warning
        for match in POSITION_VALUE.finditer(code):
            raw = match.group(1).strip()
            try:
                val = float(raw)
            except ValueError:
                findings.append((filepath, _line_of(code, match),
                                 "Dynamic position value cannot be verified statically (must stay within [0, +1])"))
                continue
            if val < 0:
                findings.append((filepath, _line_of(code, match), f"time_series is long-only, found negative position {val}"))
            elif val > 1:
                findings.append((filepath, _line_of(code, match), f"time_series position {val} exceeds max +1"))
    else:
        findings.append((filepath, 0, "Missing entry point: need set_positions (time_series) or set_portfolio_positions (cross_sectional)"))

    return findings


def check_fundamental_guards(code: str, filepath: str) -> list:
    """Warn when a ratio/divide is built from fundamentals without .notna() and a positive denominator."""
    findings = []
    fundamental = re.compile(r'self\.data\.fun_[A-Za-z0-9_]+(?:_panel)?')
    has_fundamental = bool(fundamental.search(code))
    if not has_fundamental:
        return findings

    has_notna = bool(re.search(r'\.notna\s*\(', code))
    has_pos_guard = bool(re.search(r'([A-Za-z0-9_]+)\s*>\s*0', code))

    # safe_divide / pct_change on fundamentals require explicit guards
    risky_ratio = re.compile(r'(?:safe_divide|pct_change)\s*\(')
    if risky_ratio.search(code):
        if not has_notna:
            findings.append((filepath, 0, "Fundamental ratio used without .notna() guard — treat missing as unavailable"))
        if not has_pos_guard:
            findings.append((filepath, 0, "Fundamental ratio used without positive-denominator guard (> 0)"))
    return findings


def validate_file(filepath: str, manifest_universe: str = "", manifest_mode: str = "") -> list:
    """Validate a single strategy file. Returns list of (file, line, issue)."""
    findings = []
    abspath = os.path.join(OUTPUT_DIR, *filepath.split("/"))
    if not os.path.exists(abspath):
        return [(filepath, 0, "File missing")]

    with open(abspath, "r", encoding="utf-8") as f:
        code = f.read()

    # Layout: <cap>/<mode>/<file>.py
    cap, path_mode, fname = parse_filepath(filepath)
    if cap is None:
        findings.append((filepath, 0,
                         f"Invalid filepath layout '{filepath}' — expected <vn_small_cap|vn_mid_cap|vn_large_cap>/<mode>/<file>.py"))
        return findings

    expected_universe = CAP_TO_UNIVERSE[cap]

    # Manifest consistency (when manifest rows exist)
    if manifest_mode and manifest_mode != path_mode:
        findings.append((filepath, 0, f"Manifest mode '{manifest_mode}' does not match path mode '{path_mode}'"))
    if manifest_universe and manifest_universe != expected_universe:
        findings.append((filepath, 0, f"Manifest universe '{manifest_universe}' does not match cap '{cap}' ({expected_universe})"))

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

    # Forbidden timing / look-ahead
    for pattern, msg in FORBIDDEN_TIMING:
        m = re.search(pattern, code)
        if m:
            findings.append((filepath, _line_of(code, m), f"Look-ahead: {msg}"))

    # Mode contract
    mode = detect_mode(code)
    if mode is None:
        findings.append((filepath, 0, "Cannot detect mode: no entry point found"))
    else:
        if path_mode and mode != path_mode:
            findings.append((filepath, 0, f"Detected mode '{mode}' does not match path mode '{path_mode}'"))
        findings.extend(check_field_suffix(code, filepath, mode))
        findings.extend(check_positions(code, filepath, mode))
        findings.extend(check_fundamental_guards(code, filepath))

    return findings


def validate_index() -> list:
    """Check output/index.csv (round-2 manifest) matches files on disk."""
    findings = []
    if not os.path.exists(INDEX_PATH):
        return [("index.csv", 0, "Index file missing (will be created when strategies are written)")]

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != INDEX_HEADER:
            return [("index.csv", 1, f"Unexpected header {reader.fieldnames} (expected {INDEX_HEADER})")]
        rows = list(reader)

    def walk_py(relpath):
        """Recursively collect .py rel paths under OUTPUT_DIR."""
        found = []
        for root, _dirs, files in os.walk(OUTPUT_DIR):
            for fn in files:
                if fn.endswith(".py"):
                    found.append(os.path.relpath(os.path.join(root, fn), OUTPUT_DIR).replace("\\", "/"))
        return set(found)

    actual_files = walk_py(OUTPUT_DIR)

    if not rows:
        # Empty index is fine only if there are no strategy files (nested included)
        if actual_files:
            return [("index.csv", 1, f"Index has no data rows but {len(actual_files)} strategy file(s) exist")]
        return []

    indexed_files = set()
    seen = set()
    for row in rows:
        fname = (row.get("filepath") or "").strip()
        if not fname:
            findings.append(("index.csv", 0, "Index row missing filepath"))
            continue
        if fname in seen:
            findings.append(("index.csv", 0, f"Duplicate filepath in index: {fname}"))
        seen.add(fname)

        cap, mode, _ = parse_filepath(fname)
        if cap is None:
            findings.append(("index.csv", 0,
                             f"Index filepath '{fname}' invalid — expected <cap>/<mode>/<file>.py"))
            continue
        indexed_files.add(fname)

        universe = (row.get("universe") or "").strip()
        if universe not in VALID_UNIVERSES:
            findings.append(("index.csv", 0, f"Index universe '{universe}' invalid for {fname}"))
        elif universe != CAP_TO_UNIVERSE[cap]:
            findings.append(("index.csv", 0,
                             f"Index universe '{universe}' does not match cap '{cap}' for {fname}"))

        manifest_mode = (row.get("mode") or "").strip()
        if manifest_mode not in VALID_MODES:
            findings.append(("index.csv", 0, f"Index mode '{manifest_mode}' invalid for {fname}"))
        elif manifest_mode != mode:
            findings.append(("index.csv", 0,
                             f"Index mode '{manifest_mode}' does not match path mode '{mode}' for {fname}"))

        abspath = os.path.join(OUTPUT_DIR, *fname.split("/"))
        if not os.path.exists(abspath):
            findings.append(("index.csv", 0, f"Index references missing file: {fname}"))

    orphaned = actual_files - indexed_files
    for f in sorted(orphaned):
        findings.append(("index.csv", 0, f"File not in index: {f}"))

    return findings


def classify(findings, strict: bool):
    """Split findings into errors and warnings. --strict promotes warnings to errors."""
    error_kw = ["Error", "Missing", "Forbidden", "Invalid", "Mode contract", "Point-in-time",
                "Cannot detect", "long-only", "exceeds max", "Look-ahead", "Duplicate", "import"]
    errors = []
    warnings = []
    for finding in findings:
        msg = finding[2]
        is_error = any(kw in msg for kw in error_kw)
        if strict:
            is_error = is_error or ("unsupported weighting" in msg or "Dynamic position" in msg
                                    or "without .notna" in msg or "positive-denominator" in msg
                                    or "does not match" in msg or "requires a mask" in msg)
        (errors if is_error else warnings).append(finding)
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Validate Round-2 strategies against framework compliance")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as errors (exit code 1). Use before submission.")
    args = parser.parse_args()

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
                rel = os.path.relpath(os.path.join(root, f), OUTPUT_DIR).replace("\\", "/")
                py_files.append(rel)
    py_files = sorted(py_files)

    # Load manifest for per-file universe/mode consistency
    manifest_lookup = {}
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                fp = (row.get("filepath") or "").strip()
                if fp:
                    manifest_lookup[fp] = (row.get("universe", "").strip(), row.get("mode", "").strip())

    for fname in py_files:
        universe, mode = manifest_lookup.get(fname, ("", ""))
        all_findings.extend(validate_file(fname, universe, mode))

    errors, warnings = classify(all_findings, args.strict)

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
        print(f"\n  No errors (warnings only). Strict mode: {args.strict}")
        return 0 if not args.strict else 1
    else:
        print(f"\n  {len(errors)} error(s) found.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
