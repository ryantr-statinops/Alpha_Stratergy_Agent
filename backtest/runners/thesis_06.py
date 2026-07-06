"""Thesis 06: Multi-Factor Composite — template implementations."""
import numpy as np
import pandas as pd
from backtest.features import ma, momentum, volatility, volume as vol, operators as op
from backtest.runners.base import compute_positions


def T06_A(df, z_window=20, z_threshold=2.0, rsi_window=14, adx_window=10, return_window=5,
          adx_entry=22, adx_entry_weak=18, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    price_z = volatility.price_z(close, z_window)
    vol_z = volatility.volume_z(volume, z_window)
    momentum_vals = momentum.roc(close, rsi_window)
    mom_z = ma.rolling_zscore(momentum_vals, z_window)
    composite = price_z + mom_z + vol_z
    rsi_val = momentum.rsi(close, rsi_window)
    rsi_ok = op.between(rsi_val, 30, 70)
    adx_val = momentum.adx(high, low, close, adx_window)
    return_roll = momentum.returns(close, return_window)
    core_long = (composite > z_threshold)
    core_short = (composite < -z_threshold)
    strong_long = core_long & rsi_ok & (adx_val > adx_entry) & (vol_z > 0) & (return_roll > 0)
    weak_long = core_long & rsi_ok & (adx_val > adx_entry_weak) & (return_roll > 0)
    strong_short = core_short & rsi_ok & (adx_val > adx_entry) & (vol_z < 0) & (return_roll < 0)
    weak_short = core_short & rsi_ok & (adx_val > adx_entry_weak) & (return_roll < 0)
    exit_setup = (np.abs(composite) < 0.5) | (adx_val < adx_exit)
    return compute_positions_tiered(df, strong_long, weak_long, strong_short, weak_short, exit_setup)


def T06_B(df, z_window=20, z_threshold=2.0, rsi_window=14, adx_window=10, return_window=5,
          adx_entry=22, adx_entry_weak=18, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    vn30_close = df.get("vn30_close", close)
    price_z = volatility.price_z(close, z_window)
    vol_z = volatility.volume_z(volume, z_window)
    atr_val = volatility.atr(high, low, close, 14)
    vola_z = ma.rolling_zscore(atr_val, z_window)
    ratio = close / np.maximum(vn30_close, 1e-10)
    ratio_z = ma.rolling_zscore(ratio, z_window)
    composite = price_z + vol_z + vola_z + ratio_z
    adx_val = momentum.adx(high, low, close, adx_window)
    rsi_val = momentum.rsi(close, rsi_window)
    return_roll = momentum.returns(close, return_window)
    core_long = (composite > z_threshold) & (rsi_val > 30) & (rsi_val < 70)
    core_short = (composite < -z_threshold) & (rsi_val > 30) & (rsi_val < 70)
    strong_long = core_long & (adx_val > adx_entry) & (vol_z > 0) & (return_roll > 0)
    weak_long = core_long & (adx_val > adx_entry_weak) & (return_roll > 0)
    strong_short = core_short & (adx_val > adx_entry) & (vol_z < 0) & (return_roll < 0)
    weak_short = core_short & (adx_val > adx_entry_weak) & (return_roll < 0)
    exit_setup = (np.abs(composite) < 1.0) | (adx_val < adx_exit)
    return compute_positions_tiered(df, strong_long, weak_long, strong_short, weak_short, exit_setup)


def T06_C(df, mid_window=26, vol_window=20, roc_window=5, adx_window=10, return_window=5,
          adx_entry=22, adx_entry_weak=18, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    vn30_close = df.get("vn30_close", close)
    ema_val = ma.ema(close, mid_window)
    trend_ok = close > ema_val
    roc_val = momentum.roc(close, roc_window)
    momentum_ok = roc_val > 0
    vol_sma = ma.sma(volume, vol_window)
    volume_ok = volume > vol_sma
    atr_val = volatility.atr(high, low, close, 14)
    atr_trend = atr_val > ma.sma(atr_val, vol_window)
    vn30_roc = momentum.roc(vn30_close, roc_window)
    vn30_ok = vn30_roc > 0
    adx_val = momentum.adx(high, low, close, adx_window)
    return_roll = momentum.returns(close, return_window)
    core_long = trend_ok & momentum_ok & vn30_ok
    core_short = (~trend_ok) & (~momentum_ok) & (~vn30_ok)
    strong_long = core_long & volume_ok & atr_trend & (adx_val > adx_entry) & (return_roll > 0)
    weak_long = core_long & (adx_val > adx_entry_weak) & (return_roll > 0)
    strong_short = core_short & volume_ok & atr_trend & (adx_val > adx_entry) & (return_roll < 0)
    weak_short = core_short & (adx_val > adx_entry_weak) & (return_roll < 0)
    exit_setup = op.crossed_below(close, ema_val) | (adx_val < adx_exit)
    return compute_positions_tiered(df, strong_long, weak_long, strong_short, weak_short, exit_setup)


def T06_D(df, z_window=20, adx_window=10, return_window=5, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    open_price = df["open"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    from backtest.features import candles
    price_z = volatility.price_z(close, z_window)
    vol_z = volatility.volume_z(volume, z_window)
    momentum_vals = momentum.roc(close, 14)
    mom_z = ma.rolling_zscore(momentum_vals, z_window)
    composite = price_z + mom_z + vol_z
    hammer_val = candles.hammer(open_price, high, low, close)
    engulf_val = candles.engulfing_pattern(open_price, high, low, close)
    morning_val = candles.morning_star(open_price, high, low, close)
    evening_val = candles.evening_star(open_price, high, low, close)
    adx_val = momentum.adx(high, low, close, adx_window)
    return_roll = momentum.returns(close, return_window)
    bullish_pattern = (hammer_val != 0) | (engulf_val != 0) | (morning_val != 0)
    bearish_pattern = (evening_val != 0)
    long_setup = (composite > 1.5) & bullish_pattern & (adx_val > adx_entry) & (return_roll > 0)
    short_setup = (composite < -1.5) & bearish_pattern & (adx_val > adx_entry) & (return_roll < 0)
    exit_setup = (np.abs(composite) < 0.5) | (adx_val < adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T06_E(df, z_window=20, z_entry=2.0, adx_window=10, rsi_window=14, return_window=5,
          adx_entry=22, adx_entry_weak=18, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    vn30_close = df.get("vn30_close", close)
    adx_val = momentum.adx(high, low, close, adx_window)
    atr_val = volatility.atr(high, low, close, 14)
    atr_sma = ma.sma(atr_val, 20)
    strong_trend = adx_val > 25
    weak_trend_mask = (adx_val > 20) & (adx_val <= 25)
    high_vol = atr_val > atr_sma * 1.3
    price_z = volatility.price_z(close, z_window)
    vol_z = volatility.volume_z(volume, z_window)
    momentum_vals = momentum.roc(close, 14)
    mom_z = ma.rolling_zscore(momentum_vals, z_window)
    ratio = close / np.maximum(vn30_close, 1e-10)
    ratio_z = ma.rolling_zscore(ratio, z_window)
    composite = np.where(strong_trend,
                         price_z * 1.5 + mom_z * 1.0 + vol_z * 0.5,
                         np.where(high_vol,
                                  price_z * 1.0 + vol_z * 1.5 + ratio_z * 0.5,
                                  price_z * 0.5 + ratio_z * 1.0 + mom_z * 0.5))
    rsi_val = momentum.rsi(close, rsi_window)
    return_roll = momentum.returns(close, return_window)
    strong_long = (composite > z_entry) & (adx_val > adx_entry) & (rsi_val > 40) & (return_roll > 0)
    weak_long = (composite > z_entry) & (adx_val > adx_entry_weak) & (return_roll > 0)
    strong_short = (composite < -z_entry) & (adx_val > adx_entry) & (rsi_val < 60) & (return_roll < 0)
    weak_short = (composite < -z_entry) & (adx_val > adx_entry_weak) & (return_roll < 0)
    exit_setup = (np.abs(composite) < 0.5) | (adx_val < adx_exit)
    return compute_positions_tiered(df, strong_long, weak_long, strong_short, weak_short, exit_setup)


def compute_positions_tiered(df, strong_long, weak_long, strong_short, weak_short, exit_setup):
    df = df.copy()
    df["position"] = 0
    df.loc[exit_setup, "position"] = 0
    df.loc[weak_long, "position"] = 0.5
    df.loc[strong_long, "position"] = 1
    df.loc[weak_short, "position"] = -0.5
    df.loc[strong_short, "position"] = -1
    return df["position"].to_numpy()
