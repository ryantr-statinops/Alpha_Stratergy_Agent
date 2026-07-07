"""Thesis 10: Regime-based Mean Reversion — aligned with XNOQuant templates."""
import warnings
import numpy as np
from backtest.features import ma, momentum, volatility, operators as op
from backtest.runners.base import compute_positions

warnings.filterwarnings("ignore", "Mean of empty slice")


def T10_A(df, ma200_window=200, ma20_window=20, sideways_buffer=0.02,
          adx_window=14, adx_entry=20, adx_exit=15, atr_stop_mult=2.5, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values

    ma200 = ma.sma(close, ma200_window)
    ma20 = ma.sma(close, ma20_window)
    ratio = close / np.maximum(ma200, 1e-10)
    warmup = ma200 > 0

    bull = warmup & (ratio > 1 + sideways_buffer)
    bear = warmup & (ratio < 1 - sideways_buffer)
    sideways = warmup & ~bull & ~bear

    lower_q = np.asarray(ma.rolling_quantile(close, 20, 0.2))
    upper_q = np.asarray(ma.rolling_quantile(close, 20, 0.8))

    adx_val = momentum.adx(high, low, close, adx_window)
    atr_val = volatility.atr(high, low, close, 14)

    no_long_trend = close >= ma20 - atr_stop_mult * atr_val
    no_short_trend = close <= ma20 + atr_stop_mult * atr_val
    no_long_mr = close >= lower_q - atr_stop_mult * atr_val
    no_short_mr = close <= upper_q + atr_stop_mult * atr_val
    atr_stop = (close < ma20 - atr_stop_mult * atr_val) | (close > ma20 + atr_stop_mult * atr_val)

    dip_long = bull & (close < ma20) & (adx_val > adx_entry) & no_long_trend
    rally_short = bear & (close > ma20) & (adx_val > adx_entry) & no_short_trend
    mr_long = sideways & (close < lower_q) & (adx_val < adx_entry) & no_long_mr
    mr_short = sideways & (close > upper_q) & (adx_val < adx_entry) & no_short_mr

    long_setup = np.asarray(dip_long | mr_long)
    short_setup = np.asarray(rally_short | mr_short)
    exit_setup = np.asarray(
        op.crossed_above(close, ma20) | op.crossed_below(close, ma20) |
        (adx_val < adx_exit) | (adx_val > adx_entry) | atr_stop
    )

    long_signal = long_setup & (~exit_setup)
    short_signal = short_setup & (~exit_setup)
    return compute_positions(df, long_signal, short_signal, exit_setup)


def T10_B(df, ma200_window=200, ma20_window=20, sideways_buffer=0.02,
          adx_window=14, adx_entry=22, adx_exit=15, vol_window=14,
          atr_stop_mult=2.5, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values

    ma200 = ma.sma(close, ma200_window)
    ma20 = ma.sma(close, ma20_window)
    ratio = close / np.maximum(ma200, 1e-10)
    warmup = ma200 > 0

    bull = warmup & (ratio > 1 + sideways_buffer)
    bear = warmup & (ratio < 1 - sideways_buffer)
    sideways = warmup & ~bull & ~bear

    lower_q = np.asarray(ma.rolling_quantile(close, 20, 0.2))
    upper_q = np.asarray(ma.rolling_quantile(close, 20, 0.8))

    adx_val = momentum.adx(high, low, close, adx_window)
    vol_sma = ma.sma(volume, vol_window)
    volume_ok = volume > vol_sma
    rsi_val = momentum.rsi(close, 14)
    atr_val = volatility.atr(high, low, close, 14)

    no_long_trend = close >= ma20 - atr_stop_mult * atr_val
    no_short_trend = close <= ma20 + atr_stop_mult * atr_val
    no_long_mr = close >= lower_q - atr_stop_mult * atr_val
    no_short_mr = close <= upper_q + atr_stop_mult * atr_val
    atr_stop = (close < ma20 - atr_stop_mult * atr_val) | (close > ma20 + atr_stop_mult * atr_val)

    dip_long = bull & (close < ma20) & (adx_val > adx_entry) & volume_ok & no_long_trend
    rally_short = bear & (close > ma20) & (adx_val > adx_entry) & volume_ok & no_short_trend
    mr_long = sideways & (close < lower_q) & (rsi_val < 30) & (volume < vol_sma) & (adx_val < adx_entry) & no_long_mr
    mr_short = sideways & (close > upper_q) & (rsi_val > 70) & (volume < vol_sma) & (adx_val < adx_entry) & no_short_mr

    long_setup = np.asarray(dip_long | mr_long)
    short_setup = np.asarray(rally_short | mr_short)
    exit_setup = np.asarray(
        op.crossed_above(close, ma20) | op.crossed_below(close, ma20) |
        (adx_val < adx_exit) | (adx_val > adx_entry) | atr_stop
    )

    long_signal = long_setup & (~exit_setup)
    short_signal = short_setup & (~exit_setup)
    return compute_positions(df, long_signal, short_signal, exit_setup)


def T10_C(df, ma200_window=200, sideways_buffer=0.02, bb_window=20, bb_mult=2.0,
          adx_window=14, adx_entry=20, adx_exit=15, atr_stop_mult=2.5, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values

    ma200 = ma.sma(close, ma200_window)
    ma20 = ma.sma(close, 20)
    ratio = close / np.maximum(ma200, 1e-10)
    warmup = ma200 > 0

    bull = warmup & (ratio > 1 + sideways_buffer)
    bear = warmup & (ratio < 1 - sideways_buffer)
    sideways = warmup & ~bull & ~bear

    upper, mid, lower = volatility.bbands(close, bb_window, bb_mult, bb_mult)
    adx_val = momentum.adx(high, low, close, adx_window)
    atr_val = volatility.atr(high, low, close, 14)

    lower_q = np.asarray(ma.rolling_quantile(close, 20, 0.1))
    upper_q = np.asarray(ma.rolling_quantile(close, 20, 0.9))

    no_long_trend = close >= ma20 - atr_stop_mult * atr_val
    no_short_trend = close <= ma20 + atr_stop_mult * atr_val
    no_long_mr = close >= lower_q - atr_stop_mult * atr_val
    no_short_mr = close <= upper_q + atr_stop_mult * atr_val
    atr_stop = (close < ma20 - atr_stop_mult * atr_val) | (close > ma20 + atr_stop_mult * atr_val)

    dip_long = bull & (close < lower) & (adx_val > adx_entry) & no_long_trend
    rally_short = bear & (close > upper) & (adx_val > adx_entry) & no_short_trend
    mr_long = sideways & (close < lower_q) & (adx_val < adx_entry) & no_long_mr
    mr_short = sideways & (close > upper_q) & (adx_val < adx_entry) & no_short_mr

    long_setup = np.asarray(dip_long | mr_long)
    short_setup = np.asarray(rally_short | mr_short)
    exit_setup = np.asarray(
        op.crossed_above(close, mid) | op.crossed_below(close, mid) |
        (adx_val < adx_exit) | (adx_val > adx_entry) | atr_stop
    )

    long_signal = long_setup & (~exit_setup)
    short_signal = short_setup & (~exit_setup)
    return compute_positions(df, long_signal, short_signal, exit_setup)
