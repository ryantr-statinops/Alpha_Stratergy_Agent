"""Thesis 09: Institutional Flow Arbitrage — template implementations."""
import warnings
import numpy as np
import pandas as pd
from backtest.features import ma, momentum, volatility, operators as op
from backtest.runners.base import compute_positions

warnings.filterwarnings("ignore", "Mean of empty slice")


def _fillna_pct(arr):
    return pd.Series(arr).pct_change().fillna(0).to_numpy()


def T09_A(df, adx_entry=18, adx_exit=12, adx_window=7, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    fut_oi = df.get("fut_open_interest", np.full(len(df), np.nan))

    oi_change = _fillna_pct(fut_oi)
    fut_ret = _fillna_pct(close)

    fut_bull = fut_ret > 0
    fut_bear = fut_ret < 0
    oi_up = oi_change > 0
    oi_down = oi_change < 0

    adx_val = momentum.adx(high, low, close, adx_window)

    genuine_long = fut_bull & oi_up & (adx_val > adx_entry)
    genuine_short = fut_bear & oi_up & (adx_val > adx_entry)

    fade_long = fut_bear & oi_down & (adx_val > 18)
    fade_short = fut_bull & oi_down & (adx_val > 18)

    long_setup = genuine_long | fade_long
    short_setup = genuine_short | fade_short
    exit_setup = adx_val < adx_exit

    return compute_positions(df, long_setup, short_setup, exit_setup)


def T09_B(df, adx_entry=18, adx_exit=12, vol_window=14, adx_window=7, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values

    fut_matched = df.get("fut_matched_value", np.full(len(df), np.nan))
    fut_total = df.get("fut_total_value", np.full(len(df), np.nan))
    vn30_close = df.get("vn30_close", close)

    matched_change = _fillna_pct(fut_matched)
    fut_ret = _fillna_pct(close)
    vn30_ret = _fillna_pct(vn30_close)

    flow_up = matched_change > 0
    flow_down = matched_change < 0
    fut_bull = fut_ret > 0
    fut_bear = fut_ret < 0
    vn30_align = (fut_ret > 0) == (vn30_ret > 0)

    adx_val = momentum.adx(high, low, close, adx_window)
    vol_sma = ma.sma(volume, vol_window)
    volume_ok = volume > vol_sma

    strong_long = fut_bull & flow_up & vn30_align & (adx_val > adx_entry) & volume_ok
    strong_short = fut_bear & flow_up & vn30_align & (adx_val > adx_entry) & volume_ok

    fade_long = fut_bear & flow_down & (adx_val > 18)
    fade_short = fut_bull & flow_down & (adx_val > 18)

    long_setup = strong_long | fade_long
    short_setup = strong_short | fade_short
    exit_setup = adx_val < adx_exit

    return compute_positions(df, long_setup, short_setup, exit_setup)


def T09_C(df, window=20, entry=2.0, adx_entry=18, adx_exit=12, adx_window=7, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values

    fut_oi = df.get("fut_open_interest", np.full(len(df), np.nan))
    fut_matched = df.get("fut_matched_volume", np.full(len(df), np.nan))
    vn30_close = df.get("vn30_close", close)

    price_z = np.asarray(ma.rolling_zscore(close, window))
    vn30_z = np.asarray(ma.rolling_zscore(vn30_close, window))
    vol_z = np.asarray(ma.rolling_zscore(volume, window))

    oi_change = _fillna_pct(fut_oi)
    matched_change = _fillna_pct(fut_matched)

    adx_val = momentum.adx(high, low, close, adx_window)

    oi_flow_up = oi_change > 0
    matched_flow_up = matched_change > 0
    flow_align = oi_flow_up == matched_flow_up

    composite = price_z + vn30_z + vol_z

    long_setup = (composite > entry) & flow_align & (adx_val > adx_entry)
    short_setup = (composite < -entry) & flow_align & (adx_val > adx_entry)
    exit_setup = (np.abs(composite) < 0.5) | (adx_val < adx_exit)

    return compute_positions(df, long_setup, short_setup, exit_setup)
