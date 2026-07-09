"""Core vectorized backtest runner."""
import numpy as np
import pandas as pd


def ensure_float(df):
    """Cast all numeric columns to float64 to prevent TA-Lib dtype errors."""
    for col in df.columns:
        if np.issubdtype(df[col].dtype, np.number) and df[col].dtype != np.float64:
            df[col] = df[col].astype(np.float64)
    return df


def compute_returns(df, position_col="position"):
    df = df.copy()
    df["returns"] = df["close"].pct_change().fillna(0)
    df["strategy_returns"] = df[position_col].shift(1).fillna(0) * df["returns"]
    df["equity"] = (1 + df["strategy_returns"]).cumprod()
    return df


def compute_positions(df, long_setup, short_setup, exit_setup):
    """Exit→Long→Short priority ordering with position carry-forward.

    Mimics XNOQuant's persistent set_positions(): a position entered on bar i
    is held until a subsequent exit/short/long signal changes it.
    """
    exit_setup = np.asarray(exit_setup, dtype=bool)
    long_setup = np.asarray(long_setup, dtype=bool)
    short_setup = np.asarray(short_setup, dtype=bool)
    n = len(df)
    flip = np.full(n, np.nan)
    flip[exit_setup] = 0.0
    flip[long_setup] = 1.0
    flip[short_setup] = -1.0
    pos = np.zeros(n, dtype=float)
    last = 0.0
    for i in range(n):
        if not np.isnan(flip[i]):
            last = flip[i]
        pos[i] = last
    return pos


def compute_positions_tiered(df, strong_long, weak_long, strong_short, weak_short, exit_setup):
    """Like compute_positions but with 0.5/-0.5 partial sizing (carry-forward)."""
    exit_setup = np.asarray(exit_setup, dtype=bool)
    strong_long = np.asarray(strong_long, dtype=bool)
    weak_long = np.asarray(weak_long, dtype=bool)
    strong_short = np.asarray(strong_short, dtype=bool)
    weak_short = np.asarray(weak_short, dtype=bool)
    n = len(df)
    flip = np.full(n, np.nan)
    flip[exit_setup] = 0.0
    flip[weak_long] = 0.5
    flip[strong_long] = 1.0
    flip[weak_short] = -0.5
    flip[strong_short] = -1.0
    pos = np.zeros(n, dtype=float)
    last = 0.0
    for i in range(n):
        if not np.isnan(flip[i]):
            last = flip[i]
        pos[i] = last
    return pos


def run_strategy(df, template_func, params=None):
    """Generic strategy runner.
    
    df: DataFrame with OHLCV data
    template_func: callable(df, **params) -> position array
    params: dict of parameters
    """
    df = ensure_float(df)
    params = params or {}
    pos = template_func(df, **params)
    df = df.copy()
    df["position"] = pos
    return compute_returns(df)
