"""Thesis 07: Intraday Session — template implementations."""
import numpy as np
import pandas as pd
from backtest.features import ma, momentum, volatility, operators as op
from backtest.runners.base import compute_positions


def T07_A(df, fast_window=8, vol_window=14, return_window=5, **kwargs):
    close = df["close"].values
    volume = df["volume"].values
    vol_sma = ma.sma(volume, vol_window)
    mean_val = ma.sma(close, fast_window)
    return_1 = op.fillna(op.pct_change(close, periods=1), value=0)
    return_roll = ma.rolling_mean(pd.Series(return_1), return_window)
    long_setup = (close > mean_val) & (volume > vol_sma) & (return_roll > 0)
    short_setup = (close < mean_val) & (volume > vol_sma) & (return_roll < 0)
    exit_setup = (return_roll < 0) | (return_roll > 0)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T07_B(df, rsi_window=7, vol_window=14, adx_window=7, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    rsi_val = momentum.rsi(close, rsi_window)
    vol_sma = ma.sma(volume, vol_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    long_setup = (rsi_val < 30) & (volume > vol_sma * 0.7) & (adx_val < 20)
    short_setup = (rsi_val > 70) & (volume > vol_sma * 0.7) & (adx_val < 20)
    exit_setup = op.crossed_above(rsi_val, 50) | op.crossed_below(rsi_val, 50) | (adx_val > 25)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T07_C(df, roc_window=3, vol_window=14, vol_mult=1.5, adx_window=7, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    roc_val = momentum.roc(close, roc_window)
    vol_sma = ma.sma(volume, vol_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    long_setup = (roc_val > 0) & (volume > vol_sma * vol_mult) & (adx_val > adx_entry)
    short_setup = (roc_val < 0) & (volume > vol_sma * vol_mult) & (adx_val > adx_entry)
    exit_setup = (roc_val < 0) | (roc_val > 0) | (adx_val < adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T07_D(df, bb_window=14, bb_mult=2.0, vol_window=14, ema_window=20, adx_window=7, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    upper, mid, lower = volatility.bbands(close, bb_window, bb_mult, bb_mult)
    vol_sma = ma.sma(volume, vol_window)
    mean_val = ma.sma(close, ema_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    long_setup = (close < lower) & (volume > vol_sma) & (adx_val < 20)
    short_setup = (close > upper) & (volume > vol_sma) & (adx_val < 20)
    exit_setup = op.crossed_above(close, mean_val) | op.crossed_below(close, mean_val) | (adx_val > 25)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T07_E(df, vwap_window=14, z_entry=1.0, vol_window=14, return_window=5, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    vwap_val = ma.vwap(high, low, close, volume, window=vwap_window)
    vol_sma = ma.sma(volume, vol_window)
    return_1 = op.fillna(op.pct_change(close, periods=1), value=0)
    return_roll = ma.rolling_mean(pd.Series(return_1), return_window)
    upper_band = vwap_val * (1 + z_entry / 100)
    lower_band = vwap_val * (1 - z_entry / 100)
    long_setup = (close < lower_band) & (return_roll > 0) & (volume > vol_sma * 0.7)
    short_setup = (close > upper_band) & (return_roll < 0) & (volume > vol_sma * 0.7)
    exit_setup = op.crossed_above(close, vwap_val) | op.crossed_below(close, vwap_val)
    return compute_positions(df, long_setup, short_setup, exit_setup)
