"""Core vectorized backtest runner."""
import numpy as np
import pandas as pd


def compute_returns(df, position_col="position"):
    df = df.copy()
    df["returns"] = df["close"].pct_change().fillna(0)
    df["strategy_returns"] = df[position_col].shift(1).fillna(0) * df["returns"]
    df["equity"] = (1 + df["strategy_returns"]).cumprod()
    return df


def compute_positions(df, long_setup, short_setup, exit_setup):
    """Apply Exit→Long→Short priority ordering."""
    df = df.copy()
    df["position"] = 0
    df.loc[exit_setup, "position"] = 0
    df.loc[long_setup, "position"] = 1
    df.loc[short_setup, "position"] = -1
    return df["position"].to_numpy()


def compute_positions_tiered(df, strong_long, weak_long, strong_short, weak_short, exit_setup):
    """Like compute_positions but with 0.5/-0.5 partial sizing."""
    df = df.copy()
    df["position"] = 0
    df.loc[exit_setup, "position"] = 0
    df.loc[weak_long, "position"] = 0.5
    df.loc[strong_long, "position"] = 1
    df.loc[weak_short, "position"] = -0.5
    df.loc[strong_short, "position"] = -1
    return df["position"].to_numpy()


def run_strategy(df, template_func, params=None):
    """Generic strategy runner.
    
    df: DataFrame with OHLCV data
    template_func: callable(df, **params) -> position array
    params: dict of parameters
    """
    params = params or {}
    pos = template_func(df, **params)
    df = df.copy()
    df["position"] = pos
    return compute_returns(df)
