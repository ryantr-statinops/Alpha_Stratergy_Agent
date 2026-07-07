"""Thesis 10: Regime-based Mean Reversion — template implementations."""
import warnings
import numpy as np
from backtest.features import ma, momentum, volatility, operators as op
from backtest.runners.base import compute_positions

warnings.filterwarnings("ignore", "Mean of empty slice")


def T10_A(df, ma200_window=200, ma20_window=20, sideways_buffer=0.02,
          adx_window=14, adx_exit=12, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values

    ma200 = ma.sma(close, ma200_window)
    ma20 = ma.sma(close, ma20_window)
    ratio = close / np.maximum(ma200, 1e-10)
    valid = ratio < 10

    bull = valid & (ratio > 1 + sideways_buffer)
    bear = valid & (ratio < 1 - sideways_buffer)
    sideways = valid & ~bull & ~bear

    lower_q = np.asarray(ma.rolling_quantile(close, 20, 0.2))
    upper_q = np.asarray(ma.rolling_quantile(close, 20, 0.8))

    dip_long = bull & (close < ma20)
    rally_short = bear & (close > ma20)
    mr_long = sideways & (close < lower_q)
    mr_short = sideways & (close > upper_q)

    adx_val = momentum.adx(high, low, close, adx_window)

    long_setup = np.asarray(dip_long | mr_long)
    short_setup = np.asarray(rally_short | mr_short)
    exit_setup = np.asarray(op.between(close, ma20 * 0.998, ma20 * 1.002) | (adx_val < adx_exit))

    return compute_positions(df, long_setup, short_setup, exit_setup)


def T10_B(df, ma200_window=200, ma20_window=20, sideways_buffer=0.02,
          adx_window=14, adx_entry=22, adx_exit=15, vol_window=14, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values

    ma200 = ma.sma(close, ma200_window)
    ma20 = ma.sma(close, ma20_window)
    ratio = close / np.maximum(ma200, 1e-10)
    valid = ratio < 10

    bull = valid & (ratio > 1 + sideways_buffer)
    bear = valid & (ratio < 1 - sideways_buffer)
    sideways = valid & ~bull & ~bear

    adx_val = momentum.adx(high, low, close, adx_window)
    vol_sma = ma.sma(volume, vol_window)
    volume_ok = volume > vol_sma
    rsi_val = momentum.rsi(close, 14)

    dip_long = bull & (close < ma20) & (adx_val > adx_entry) & volume_ok
    rally_short = bear & (close > ma20) & (adx_val > adx_entry) & volume_ok
    mr_long = sideways & (rsi_val < 30) & (volume < vol_sma)
    mr_short = sideways & (rsi_val > 70) & (volume < vol_sma)

    long_setup = np.asarray(dip_long | mr_long)
    short_setup = np.asarray(rally_short | mr_short)
    exit_setup = np.asarray(op.between(close, ma20 * 0.998, ma20 * 1.002) | (adx_val < adx_exit))

    return compute_positions(df, long_setup, short_setup, exit_setup)


def T10_C(df, ma200_window=200, sideways_buffer=0.02, bb_window=20, bb_mult=2.0,
          adx_window=14, adx_exit=12, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values

    ma200 = ma.sma(close, ma200_window)
    ratio = close / np.maximum(ma200, 1e-10)
    valid = ratio < 10

    bull = valid & (ratio > 1 + sideways_buffer)
    bear = valid & (ratio < 1 - sideways_buffer)
    sideways = valid & ~bull & ~bear

    upper, mid, lower = volatility.bbands(close, bb_window, bb_mult, bb_mult)
    adx_val = momentum.adx(high, low, close, adx_window)

    lower_q = np.asarray(ma.rolling_quantile(close, 20, 0.1))
    upper_q = np.asarray(ma.rolling_quantile(close, 20, 0.9))

    dip_long = bull & (close < lower)
    rally_short = bear & (close > upper)
    mr_long = sideways & (close < lower_q)
    mr_short = sideways & (close > upper_q)

    long_setup = np.asarray(dip_long | mr_long)
    short_setup = np.asarray(rally_short | mr_short)
    exit_setup = np.asarray(op.between(close, mid * 0.998, mid * 1.002) | (adx_val < adx_exit))

    return compute_positions(df, long_setup, short_setup, exit_setup)
