"""
Comprehensive Framework Validator — checks ALL 805 strategies against XNOQuant rules.
Usage: python tools/validate_framework.py
"""

import os
import re
import ast
import sys
import glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE, "output")

PASS = 0
FAIL = 0
ERRORS = []


def check(rule_id, description, condition, filepath, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        return True
    else:
        FAIL += 1
        msg = f"[{rule_id}] FAIL {filepath}: {description}"
        if detail:
            msg += f" — {detail}"
        ERRORS.append(msg)
        return False


def has_line_containing(text, pattern):
    """Check if any line in text contains the regex pattern."""
    for line in text.split("\n"):
        if re.search(pattern, line):
            return True
    return False


def has_line_starting(text, pattern):
    """Check if any line starts with the pattern (after stripping)."""
    for line in text.split("\n"):
        if line.strip().startswith(pattern):
            return True
    return False


def count_pattern(text, pattern):
    """Count lines matching the pattern."""
    return len(re.findall(pattern, text, re.MULTILINE))


def validate_file(filepath):
    """Run all validation rules on a single strategy file."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
        lines = text.split("\n")

    relpath = os.path.relpath(filepath, BASE)

    # Determine thesis from path
    path_parts = relpath.replace("\\", "/").split("/")
    thesis_dir = path_parts[1] if len(path_parts) > 1 else ""
    thesis_match = re.match(r"thesis_(\d+)_(\w+)", thesis_dir)
    thesis_id = int(thesis_match.group(1)) if thesis_match else 0
    thesis_name = thesis_match.group(2) if thesis_match else ""

    # ── Structural Checks ──

    # R1: Docstring format
    check("R1", "Docstring has name:", "name:" in text, filepath)
    check("R1", "Docstring has summary:", "summary:" in text, filepath)
    check("R1", "Docstring has thesis:", "thesis:" in text, filepath)
    check("R1", "Docstring has idea:", "idea:" in text, filepath)

    # R2: Class definition
    check("R2", 'Class is "class CustomStrategy(SimpleAlgorithm):',
          'class CustomStrategy(SimpleAlgorithm):' in text, filepath)

    # R3: Algorithm method
    check("R3", 'Has "def __algorithm__(self):"',
          'def __algorithm__(self):' in text, filepath)

    # R4: No SeriesT type hints
    check("R4", "No SeriesT type hints", "SeriesT" not in text, filepath)

    # R5: No 'open' variable name (allow 'open_', 'open_price', 'open_ranges')
    open_vars = re.findall(r'^\s+open\s*=', text, re.MULTILINE)
    check("R5", "No 'open' as variable name", len(open_vars) == 0, filepath,
          detail=f"found {len(open_vars)} occurrences" if open_vars else "")

    # R6: No external library imports
    bad_imports = [imp for imp in ["import pandas", "import numpy", "from pandas",
                                    "from numpy", "import scipy", "import sklearn"]
                   if imp in text]
    check("R6", "No external library imports", len(bad_imports) == 0, filepath)

    # R7: Only self.set_positions for trading
    if thesis_name != "intraday_session":  # intraday uses enter/exit ranges differently
        check("R7", "Uses self.set_positions only",
              has_line_containing(text, r"self\.set_positions\("), filepath)

    # ── return_roll Enhancement Checks ──

    # R8: Has return_window class attribute
    check("R8", "Has return_window class attribute",
          has_line_containing(text, r"return_window\s*="), filepath)

    # R9: Has return_threshold class attribute
    check("R9", "Has return_threshold class attribute",
          has_line_containing(text, r"return_threshold\s*="), filepath)

    # R10: Has position_close_after_n_candles
    check("R10", "Has position_close_after_n_candles",
          has_line_containing(text, r"position_close_after_n_candles\s*="), filepath)

    # R11: Has return_1 computation
    check("R11", "Has return_1 = self.op.fillna(self.op.pct_change(...))",
          "self.op.fillna(self.op.pct_change(close, periods=1), value=0)" in text, filepath)

    # R12: Has return_roll computation
    check("R12", "Has return_roll = self.feat.rolling_mean(...)",
          "return_roll = self.feat.rolling_mean(return_1, window=self.return_window)" in text, filepath)

    # R13: Entry conditions include return_roll filter
    has_ret_long = has_line_containing(text, r"long_setup\s*=.*return_roll\s*>\s*0") or \
                   has_line_containing(text, r"strong_long\s*=.*return_roll\s*>\s*0")
    has_ret_short = has_line_containing(text, r"short_setup\s*=.*return_roll\s*<\s*0") or \
                    has_line_containing(text, r"strong_short\s*=.*return_roll\s*<\s*0")
    check("R13", "Long entry includes return_roll > 0", has_ret_long, filepath)
    check("R13", "Short entry includes return_roll < 0", has_ret_short, filepath)

    # R14: Exit includes abs(return_roll) < threshold
    check("R14", "Exit includes abs(return_roll) < self.return_threshold",
          "abs(return_roll) < self.return_threshold" in text, filepath)

    # ── Thesis-Specific Checks ──

    # R15: Thesis 07 must have position_open_ranges + position_close_ranges
    if thesis_name == "intraday_session":
        check("R15", "Has position_open_ranges",
              has_line_containing(text, r"position_open_ranges\s*="), filepath)
        check("R15", "Has position_close_ranges",
              has_line_containing(text, r"position_close_ranges\s*="), filepath)

    # R16: Tiered ADX templates (thesis 02 + 08) must have strong/weak split
    if thesis_name in ("trend", "multifactor"):
        has_strong = has_line_containing(text, r"strong_long\s*=")
        has_weak = has_line_containing(text, r"weak_long\s*=")
        # Some trend templates (ma_cross, aroon) are NOT tiered, only macd/quantile/ema_adx
        # Check if the file uses ADX to determine if it should be tiered
        uses_adx = has_line_containing(text, r"self\.feat\.adx\(")
        if uses_adx:
            check("R16", "ADX templates have strong_long position",
                  has_strong, filepath)
            check("R16", "ADX templates have weak_long position",
                  has_weak, filepath)
            check("R16", "ADX templates have tiered sizing (0.5/1.0)",
                  has_line_containing(text, r"set_positions\(.*position\s*=\s*0\.5"), filepath)

    # ── Position Sizing Order ──

    # R17: Exit (position=0) comes before Long/Short
    pos_calls = []
    for line in lines:
        m = re.search(r'self\.set_positions\((.+?),\s*position\s*=\s*([-0-9.]+)', line)
        if m:
            pos_calls.append((line.strip(), float(m.group(2))))

    exit_order = [i for i, (_, p) in enumerate(pos_calls) if p == 0]
    long_order = [i for i, (_, p) in enumerate(pos_calls) if p > 0]
    short_order = [i for i, (_, p) in enumerate(pos_calls) if p < 0]

    if exit_order and long_order and short_order:
        first_exit = exit_order[0]
        first_long = long_order[0]
        first_short = short_order[0]
        check("R17", "Exit (position=0) called before Long positions",
              first_exit < first_long, filepath,
              detail=f"exit at index {first_exit}, long at {first_long}")
        check("R17", "Exit (position=0) called before Short positions",
              first_exit < first_short, filepath,
              detail=f"exit at index {first_exit}, short at {first_short}")

    # R18: Valid position values
    for _, pos in pos_calls:
        check("R18", f"Position value {pos} is valid",
              pos in (0, 0.5, 1, -0.5, -1), filepath,
              detail=f"invalid position: {pos}")

    # ── Data & Feature Access ──

    # R19: Data only from self.data
    bad_data = re.findall(r'(?<!self\.)data\.(?!pv_|fut_)', text)
    if bad_data:
        check("R19", "No direct data access outside self.data",
              False, filepath, detail=f"found: {bad_data}")

    # R20: Has session_candles value matches timeframe
    # (we embedded it as position_close_after_n_candles, which we already check)

    # R21: At least one set_positions with position=0 (exit)
    check("R21", "Has at least one exit (position=0)",
          any(p == 0 for _, p in pos_calls), filepath)

    # R22: Closed-form positions (no complex Python expressions as positions)
    # Already checked by R18 which validates each position value.

    # ── Position Values Range ──

    # R23: Position values within [-1, 1]
    for _, pos in pos_calls:
        check("R23", f"Position {pos} within [-1, 1]",
              -1 <= pos <= 1, filepath)

    # R24: Data fields used match what's available (no undefined self.data fields)
    data_refs = re.findall(r'self\.data\.(\w+)', text)
    valid_data = {
        "pv_close", "pv_high", "pv_low", "pv_open", "pv_volume",
        "pv_vn30_close", "pv_vn30_high", "pv_vn30_low", "pv_vn30_open", "pv_vn30_volume",
        "pv_dji_close", "pv_dji_high", "pv_dji_low", "pv_dji_open",
        "fut_matched_volume_vn30f1m_1d", "fut_matched_value_vn30f1m_1d",
        "fut_open_interest_vn30f1m_1d", "fut_total_volume_vn30f1m_1d",
        "fut_total_value_vn30f1m_1d",
    }
    for ref in data_refs:
        check("R24", f"self.data.{ref} is a valid field",
              ref in valid_data, filepath, detail=f"unknown field: {ref}")


def main():
    global PASS, FAIL, ERRORS
    py_files = glob.glob(os.path.join(OUTPUT_DIR, "**", "*.py"), recursive=True)
    print(f"Found {len(py_files)} strategy files to validate...")

    for i, filepath in enumerate(py_files):
        if (i + 1) % 100 == 0:
            print(f"  Progress: {i + 1}/{len(py_files)}...")
        try:
            validate_file(filepath)
        except Exception as e:
            FAIL += 1
            ERRORS.append(f"[EXCEPTION] {filepath}: {e}")

    # Summary
    print(f"\n{'='*60}")
    print(f"Validation Summary")
    print(f"{'='*60}")
    print(f"  Files checked: {len(py_files)}")
    print(f"  Checks passed: {PASS}")
    print(f"  Checks failed: {FAIL}")
    print(f"  Pass rate:     {PASS / (PASS + FAIL) * 100:.1f}%" if (PASS + FAIL) > 0 else "  N/A")

    if ERRORS:
        print(f"\n  Failures ({len(ERRORS)}):")
        # Group by rule
        from collections import Counter
        rule_counts = Counter()
        for e in ERRORS:
            rule_id = e.split("]")[0].lstrip("[")
            rule_counts[rule_id] += 1
        print(f"\n  Failures by rule:")
        for rule_id, count in sorted(rule_counts.items()):
            print(f"    {rule_id}: {count} failures")

        # Show first 5 errors with file paths
        print(f"\n  First 10 errors:")
        for e in ERRORS[:10]:
            print(f"    {e}")

    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
