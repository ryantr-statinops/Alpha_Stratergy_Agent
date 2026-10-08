"""Thesis 01: Rolling Mean + Quantile — template implementations."""
import numpy as np
import pandas as pd
from backtest.features import ma, momentum, volatility, operators as op
from backtest.runners.base import compute_positions


def T01_A(df, mean_window=20, price_source="close", **kwargs):
    close = df["close"].values
    src = close
    mean = ma.rolling_mean(src, mean_window)
    long_setup = src > mean
    short_setup = src < mean
    exit_setup = op.crossed_below(src, mean) | op.crossed_above(src, mean)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T01_B(df, fast_window=13, slow_window=34, **kwargs):
    close = df["close"].values
    fast_ma = ma.sma(close, fast_window)
    slow_ma = ma.sma(close, slow_window)
    long_setup = op.crossed_above(fast_ma, slow_ma)
    short_setup = op.crossed_below(fast_ma, slow_ma)
    exit_setup = op.crossed_below(fast_ma, slow_ma) | op.crossed_above(fast_ma, slow_ma)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T01_C(df, mean_window=20, rsi_window=7, vol_window=14, adx_window=7, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    volume = df["volume"].values
    high = df["high"].values
    low = df["low"].values
    mean = ma.rolling_mean(close, mean_window)
    rsi_val = momentum.rsi(close, rsi_window)
    vol_sma = ma.sma(volume, vol_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    long_setup = (close > mean) & (rsi_val > 50) & (volume > vol_sma) & (adx_val > adx_entry)
    short_setup = (close < mean) & (rsi_val < 50) & (volume > vol_sma) & (adx_val > adx_entry)
    exit_setup = op.crossed_below(close, mean) | op.crossed_above(close, mean) | (adx_val < adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T01_D(df, q_window=20, q_high=0.8, q_low=0.2, **kwargs):
    close = df["close"].values
    upper = ma.rolling_quantile(close, q_window, q_high)
    lower = ma.rolling_quantile(close, q_window, q_low)
    long_setup = close > upper
    short_setup = close < lower
    exit_setup = op.crossed_below(close, upper) | op.crossed_above(close, lower)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T01_E(df, mean_window=20, q_window=20, **kwargs):
    close = df["close"].values
    mean = ma.rolling_mean(close, mean_window)
    upper = ma.rolling_quantile(close, q_window, 0.8)
    lower = ma.rolling_quantile(close, q_window, 0.2)
    long_setup = (close > upper) & (close > mean)
    short_setup = (close < lower) & (close < mean)
    exit_setup = op.crossed_below(close, mean) | op.crossed_above(close, mean)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T01_F(df, z_window=20, z_entry=2.0, **kwargs):
    close = df["close"].values
    price_z = ma.rolling_zscore(close, z_window)
    long_setup = price_z < -z_entry
    short_setup = price_z > z_entry
    exit_setup = op.between(price_z, -1, 1)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T01_G(df, kama_window=20, adx_window=7, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    mama_val, fama = ma.mama(close)
    kama_val = ma.kama(close, kama_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    long_setup = (close > kama_val) & (mama_val > fama)
    short_setup = (close < kama_val) & (mama_val < fama)
    exit_setup = op.crossed_below(close, kama_val) | op.crossed_above(close, kama_val)
    return compute_positions(df, long_setup, short_setup, exit_setup)
