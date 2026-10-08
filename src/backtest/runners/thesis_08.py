"""Thesis 08: Order Book Shadowing — OHLCV Absorption templates."""
import numpy as np
import pandas as pd
from backtest.features import ma, momentum, volatility, operators as op
from backtest.runners.base import compute_positions


def T08_A(df, level_window=14, vol_window=14, adx_window=7, adx_exit=15, adx_entry_weak=18, return_window=5, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    res_level = op.rolling_max(close, level_window)
    sup_level = op.rolling_min(close, level_window)
    midpoint = (high + low) * 0.5
    vol_sma = ma.sma(volume, vol_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    return_1 = op.fillna(op.pct_change(close, periods=1), value=0)
    return_roll = ma.rolling_mean(pd.Series(return_1), return_window)
    at_resistance = close >= res_level * 0.995
    at_support = close <= sup_level * 1.005
    close_lower_half = close < midpoint
    close_upper_half = close > midpoint
    rejected_resistance = at_resistance & close_lower_half
    rejected_support = at_support & close_upper_half
    long_setup = rejected_support & (volume > vol_sma) & (adx_val > adx_entry_weak) & (return_roll > 0)
    short_setup = rejected_resistance & (volume > vol_sma) & (adx_val > adx_entry_weak) & (return_roll < 0)
    exit_setup = (adx_val < adx_exit) | (return_roll < -0.001) | (return_roll > 0.001)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T08_B(df, level_window=14, vol_window=14, adx_window=7, adx_exit=15, adx_entry_weak=18, return_window=5, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    res_level = op.rolling_max(close, level_window)
    sup_level = op.rolling_min(close, level_window)
    midpoint = (high + low) * 0.5
    vol_sma = ma.sma(volume, vol_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    natr_val = volatility.natr(high, low, close, 14)
    natr_ma = ma.sma(natr_val, 14)
    return_1 = op.fillna(op.pct_change(close, periods=1), value=0)
    return_roll = ma.rolling_mean(pd.Series(return_1), return_window)
    at_resistance = close >= res_level * 0.995
    at_support = close <= sup_level * 1.005
    close_lower_half = close < midpoint
    close_upper_half = close > midpoint
    vol_spike = volume > vol_sma * 1.5
    tight_range = (high - low) < natr_val * 0.8
    short_setup = at_resistance & vol_spike & tight_range & close_lower_half & (adx_val > adx_entry_weak) & (return_roll < 0)
    long_setup = at_support & vol_spike & tight_range & close_upper_half & (adx_val > adx_entry_weak) & (return_roll > 0)
    exit_setup = (adx_val < adx_exit) | (return_roll < -0.001) | (return_roll > 0.001) | (natr_val > natr_ma * 2.0)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T08_C(df, natr_window=10, level_window=14, vol_window=14, adx_window=7, adx_exit=15, adx_entry_weak=18, return_window=5, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    res_level = op.rolling_max(close, level_window)
    sup_level = op.rolling_min(close, level_window)
    natr_val = volatility.natr(high, low, close, natr_window)
    natr_sma = ma.sma(natr_val, natr_window)
    vol_sma = ma.sma(volume, vol_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    return_1 = op.fillna(op.pct_change(close, periods=1), value=0)
    return_roll = ma.rolling_mean(pd.Series(return_1), return_window)
    at_resistance = close >= res_level * 0.995
    at_support = close <= sup_level * 1.005
    tight_range = natr_val < natr_sma * 0.8
    short_setup = at_resistance & tight_range & (volume > vol_sma) & (adx_val > adx_entry_weak) & (return_roll < 0)
    long_setup = at_support & tight_range & (volume > vol_sma) & (adx_val > adx_entry_weak) & (return_roll > 0)
    exit_setup = (adx_val < adx_exit) | (return_roll < -0.001) | (return_roll > 0.001) | (natr_val > natr_sma * 2.0)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T08_D(df, level_window=14, vwap_window=14, vwap_mult=1.0, vol_window=14, adx_window=7, adx_exit=15, adx_entry_weak=18, return_window=5, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    res_level = op.rolling_max(close, level_window)
    sup_level = op.rolling_min(close, level_window)
    vwap_val = ma.vwap(high, low, close, volume, window=vwap_window)
    vol_sma = ma.sma(volume, vol_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    return_1 = op.fillna(op.pct_change(close, periods=1), value=0)
    return_roll = ma.rolling_mean(pd.Series(return_1), return_window)
    at_resistance = close >= res_level * 0.995
    at_support = close <= sup_level * 1.005
    over_extended_short = at_resistance & (close > vwap_val * (1 + vwap_mult / 100))
    over_extended_long = at_support & (close < vwap_val * (1 - vwap_mult / 100))
    short_setup = over_extended_short & (volume > vol_sma) & (adx_val > adx_entry_weak) & (return_roll < 0)
    long_setup = over_extended_long & (volume > vol_sma) & (adx_val > adx_entry_weak) & (return_roll > 0)
    exit_setup = (op.between(close, vwap_val * 0.999, vwap_val * 1.001)) | (adx_val < adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T08_E(df, composite_window=14, composite_entry=2.0, roc_window=5, vol_window=14, adx_window=7, adx_entry=22, adx_exit=15, return_window=5, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    price_z = ma.rolling_zscore(close, composite_window)
    vol_z = volatility.volume_z(volume, composite_window)
    natr_val = volatility.natr(high, low, close, 14)
    range_z = ma.rolling_zscore(natr_val, composite_window)
    mom = momentum.roc(close, roc_window)
    mom_z = ma.rolling_zscore(mom, composite_window)
    composite = price_z + vol_z + (-range_z) + mom_z
    vol_sma = ma.sma(volume, vol_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    return_1 = op.fillna(op.pct_change(close, periods=1), value=0)
    return_roll = ma.rolling_mean(pd.Series(return_1), return_window)
    long_setup = (composite > composite_entry) & (volume > vol_sma) & (adx_val > adx_entry) & (return_roll > 0)
    short_setup = (composite < -composite_entry) & (volume > vol_sma) & (adx_val > adx_entry) & (return_roll < 0)
    exit_setup = (np.abs(composite) < 0.5) | (adx_val < adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)
