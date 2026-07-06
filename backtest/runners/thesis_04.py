"""Thesis 04: Microstructure Flow — template implementations."""
import numpy as np
import pandas as pd
from backtest.features import ma, momentum, volatility, volume as vol, operators as op
from backtest.runners.base import compute_positions


def T04_A(df, cmf_window=20, adx_window=7, vol_window=14, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    open_price = df["open"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    bop_val = vol.bop(open_price, high, low, close)
    cmf_val = vol.cmf(high, low, close, pd.Series(volume), cmf_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    vol_sma = ma.sma(volume, vol_window)
    buying_pressure = (bop_val > 0) & (cmf_val > 0)
    selling_pressure = (bop_val < 0) & (cmf_val < 0)
    long_setup = buying_pressure & (adx_val > adx_entry) & (volume > vol_sma)
    short_setup = selling_pressure & (adx_val > adx_entry) & (volume > vol_sma)
    exit_setup = op.crossed_below(cmf_val, 0) | op.crossed_above(cmf_val, 0) | (adx_val < adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T04_B(df, mfi_window=14, adx_window=7, vol_window=14, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    mfi_val = vol.mfi(high, low, close, volume, mfi_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    vol_sma = ma.sma(volume, vol_window)
    long_setup = (mfi_val < 30) & (adx_val > adx_entry) & (volume > vol_sma * 0.5)
    short_setup = (mfi_val > 70) & (adx_val > adx_entry) & (volume > vol_sma * 0.5)
    exit_setup = op.crossed_above(mfi_val, 50) | op.crossed_below(mfi_val, 50) | (adx_val < adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T04_C(df, oi_window=10, vol_window_val=10, oi_drop_threshold=0.01, vol_spike_mult=2.0, price_fall_threshold=0.005, **kwargs):
    """OI Cascade — requires OI and matched_vol columns."""
    close = df["close"].values
    oi = df.get("fut_open_interest", np.full(len(df), np.nan))
    matched_vol = df.get("fut_matched_volume", np.full(len(df), np.nan))
    if np.isnan(oi).all() or np.isnan(matched_vol).all():
        return np.zeros(len(df))
    oi_sma = ma.sma(oi, oi_window)
    vol_sma = ma.sma(matched_vol, vol_window_val)
    oi_change = op.fillna(op.pct_change(oi, 1), 0)
    oi_drop = oi_change < -oi_drop_threshold
    vol_spike = matched_vol > vol_sma * vol_spike_mult
    price_fall = op.pct_change(close, 1) < -price_fall_threshold
    cascade = oi_drop & vol_spike & price_fall
    vol_collapse = matched_vol < vol_sma * 0.5
    price_stable = np.abs(op.pct_change(close, 1)) < price_fall_threshold * 0.2
    exhaustion = oi_drop & vol_collapse & price_stable
    long_setup = exhaustion
    short_setup = cascade
    exit_setup = op.crossed_below(close, oi_sma) | op.crossed_above(close, oi_sma)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T04_D(df, whale_window=20, whale_sigma=2.0, adx_window=7, adx_entry=22, adx_exit=15, **kwargs):
    """Whale Footprint — requires matched_val and matched_vol columns."""
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    matched_val = df.get("fut_matched_value", np.full(len(df), np.nan))
    matched_vol = df.get("fut_matched_volume", np.full(len(df), np.nan))
    if np.isnan(matched_val).all() or np.isnan(matched_vol).all():
        return np.zeros(len(df))
    avg_trade = matched_val / np.maximum(matched_vol, 1)
    avg_trade_sma = ma.sma(avg_trade, whale_window)
    avg_trade_std = ma.rolling_std(avg_trade, whale_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    whale = avg_trade > avg_trade_sma + whale_sigma * avg_trade_std
    vol_sma = ma.sma(matched_vol, whale_window)
    price_range = (ma.rolling_max(close, 10) - ma.rolling_min(close, 10)) / np.maximum(ma.rolling_min(close, 10), 1e-10)
    price_compression = price_range < 0.01
    long_setup = whale & price_compression & (matched_vol > vol_sma * 1.5) & (adx_val > adx_entry)
    short_setup = whale & price_compression & (matched_vol > vol_sma * 1.5) & (adx_val > adx_entry)
    exit_setup = op.crossed_below(close, ma.sma(close, 20)) | op.crossed_above(close, ma.sma(close, 20)) | (adx_val < adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T04_E(df, adosc_fast=3, adosc_slow=10, rsi_window=14, adx_window=7, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    adosc_val = vol.adosc(high, low, close, volume, adosc_fast, adosc_slow)
    rsi_val = momentum.rsi(close, rsi_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    price_rising = close > op.previous(close)
    price_falling = close < op.previous(close)
    bullish_div = price_falling & (adosc_val > op.previous(adosc_val)) & (rsi_val < 40)
    bearish_div = price_rising & (adosc_val < op.previous(adosc_val)) & (rsi_val > 60)
    long_setup = bullish_div & (adx_val > adx_entry)
    short_setup = bearish_div & (adx_val > adx_entry)
    exit_setup = op.crossed_below(close, ma.sma(close, 14)) | op.crossed_above(close, ma.sma(close, 14)) | (adx_val < adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T04_F(df, obv_window=20, adx_window=7, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    obv_val = vol.obv(close, volume)
    obv_sma = ma.sma(obv_val, obv_window)
    close_sma = ma.sma(close, obv_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    long_setup = (close > close_sma) & (obv_val > obv_sma) & (adx_val > adx_entry)
    short_setup = (close < close_sma) & (obv_val < obv_sma) & (adx_val > adx_entry)
    exit_setup = op.crossed_below(obv_val, obv_sma) | op.crossed_above(obv_val, obv_sma) | (adx_val < adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T04_G(df, imbalance_window=20, adx_window=7, adx_entry=22, adx_exit=15, **kwargs):
    """Volume Flow Imbalance — requires matched_val, matched_vol, oi columns."""
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    matched_val = df.get("fut_matched_value", np.full(len(df), np.nan))
    matched_vol = df.get("fut_matched_volume", np.full(len(df), np.nan))
    oi = df.get("fut_open_interest", np.full(len(df), np.nan))
    if np.isnan(matched_val).all() or np.isnan(matched_vol).all():
        return np.zeros(len(df))
    avg_trade = matched_val / np.maximum(matched_vol, 1)
    close_sma = ma.sma(close, imbalance_window)
    oi_change = op.fillna(op.pct_change(oi, 1), 0)
    adx_val = momentum.adx(high, low, close, adx_window)
    smart_money_long = (oi_change > 0) & (avg_trade > ma.sma(avg_trade, imbalance_window))
    smart_money_short = (oi_change < -0.005) & (matched_vol > ma.sma(matched_vol, imbalance_window) * 1.5)
    long_setup = smart_money_long & (close > close_sma) & (adx_val > adx_entry)
    short_setup = smart_money_short & (close < close_sma) & (adx_val > adx_entry)
    exit_setup = op.crossed_below(close, close_sma) | op.crossed_above(close, close_sma) | (adx_val < adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)
