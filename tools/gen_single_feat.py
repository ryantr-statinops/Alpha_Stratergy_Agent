#!/usr/bin/env python3
"""
Generate a single-feat alpha strategy file following the trend-following pattern.

Parameters are read from syntax/parameters.md for 15min VNFuture.

Usage:
    python tools/gen_single_feat.py <indicator> <feat_call> <threshold> [--data <vars>]

Examples:
    python tools/gen_single_feat.py rsi "rsi(close, timeperiod=14)" 50
    python tools/gen_single_feat.py cci "cci(high, low, close, timeperiod=20)" 0 --data "high, low"
    python tools/gen_single_feat.py cmo "cmo(close, timeperiod=14)" 0
    python tools/gen_single_feat.py willr "willr(high, low, close, timeperiod=14)" -50 --data "high, low"
"""

import os
import sys
import re

PARAMETERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "syntax", "parameters.md")


def load_parameters():
    """Parse syntax/parameters.md and return {feature: {param: value}}."""
    params = {}
    current_feature = None
    with open(PARAMETERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            m = re.match(r"^\|\s*(\S+)\s*\|\s*(\S+)\s*\|\s*(\S+)\s*\|", line)
            if m:
                feature = m.group(1).lower()
                param = m.group(2).lower()
                value = m.group(3)
                if feature in ("feature", "name", "---"):
                    continue
                if param == "(none)":
                    continue
                if feature not in params:
                    params[feature] = {}
                params[feature][param] = value
    return params


def get_param(feature: str, param: str, default: str, params_dict: dict) -> str:
    """Look up a parameter value from the parameters.md file."""
    feature_lower = feature.lower()
    if feature_lower in params_dict:
        if param.lower() in params_dict[feature_lower]:
            return params_dict[feature_lower][param.lower()]
    return default


TEMPLATE = '''class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
{data_lines}
        {feat_var} = self.feat.{feat_call}

        long_setup = {feat_var} > {threshold}
        short_setup = {feat_var} < {threshold}
        exit_setup = self.op.crossed({feat_var}, {threshold})

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
'''


def generate(indicator: str, feat_call: str, threshold: str, data_vars: list[str] | None = None):
    if data_vars is None:
        data_vars = []

    data_lines = []
    for var in data_vars:
        data_lines.append(f"        {var} = self.data.pv_{var}")
    if not data_lines:
        data_lines.append("        close = self.data.pv_close")

    feat_var = feat_call.split("(")[0]

    code = TEMPLATE.format(
        data_lines="\n".join(data_lines),
        feat_var=feat_var,
        feat_call=feat_call,
        threshold=threshold,
    )

    filename = f"SF_{indicator.upper()}_15min.py"
    filepath = os.path.join("output", "single_feat_alpha", filename)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"Generated: {filepath}")
    return filepath


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate a single-feat alpha strategy")
    parser.add_argument("indicator", help="Indicator name (e.g., rsi, cci, cmo, willr)")
    parser.add_argument("feat_call", help="Feature function call (e.g., rsi(close, timeperiod=14))")
    parser.add_argument("threshold", help="Threshold value for entry/exit (e.g., 50, 0, -50)")
    parser.add_argument("--data", nargs="*", default=[], help="Additional data vars (e.g., high low)")

    args = parser.parse_args()
    generate(args.indicator, args.feat_call, args.threshold, args.data)
