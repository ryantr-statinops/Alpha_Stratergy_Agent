"""Thesis 05: Cross-Market Correlation — template implementations."""
import numpy as np
import pandas as pd
from backtest.features import ma, momentum, volatility, operators as op
from backtest.runners.base import compute_positions


def T05_A(df, beta_window=20, z_entry=2.0, adx_window=10, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    vn30_close = df.get("vn30_close", close)
    beta_val = ma.beta(close, vn30_close, beta_window)
    spread = close - beta_val * vn30_close
    spread_z = ma.rolling_zscore(spread, beta_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    long_setup = (spread_z < -z_entry) & (adx_val > adx_entry)
    short_setup = (spread_z > z_entry) & (adx_val > adx_entry)
    exit_setup = op.between(spread_z, -1, 1) | op.crossed_below(adx_val, adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T05_B(df, roc_window=5, **kwargs):
    close = df["close"].values
    vn30_close = df.get("vn30_close", close)
    fut_roc = momentum.roc(close, roc_window)
    vn30_roc = momentum.roc(vn30_close, roc_window)
    long_setup = (fut_roc > 0) & (vn30_roc > 0)
    short_setup = (fut_roc < 0) & (vn30_roc < 0)
    exit_setup = op.crossed_below(fut_roc, 0) | op.crossed_above(fut_roc, 0)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T05_C(df, basis_window=20, basis_entry=2.0, adx_window=10, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    vn30_close = df.get("vn30_close", close)
    basis = close - vn30_close
    basis_z = ma.rolling_zscore(basis, basis_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    matched_vol = df.get("fut_matched_volume", np.full(len(df), np.nan))
    if not np.isnan(matched_vol).all():
        vol_sma = ma.sma(matched_vol, basis_window)
        vol_filter = matched_vol < vol_sma
    else:
        vol_filter = np.ones(len(df), dtype=bool)
    long_setup = (basis_z < -basis_entry) & vol_filter & (adx_val > adx_entry)
    short_setup = (basis_z > basis_entry) & vol_filter & (adx_val > adx_entry)
    exit_setup = op.between(basis_z, -1, 1) | (adx_val < adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T05_D(df, roc_window=5, **kwargs):
    close = df["close"].values
    vn30_close = df.get("vn30_close", close)
    dji_close = df.get("dji_close", close)
    dji_roc = momentum.roc(dji_close, roc_window)
    fut_roc = momentum.roc(close, roc_window)
    vn30_roc = momentum.roc(vn30_close, roc_window)
    bullish = (fut_roc > 0) & (vn30_roc > 0) & (dji_roc > 0)
    bearish = (fut_roc < 0) & (vn30_roc < 0) & (dji_roc < 0)
    long_setup = bullish
    short_setup = bearish
    exit_setup = (~bullish) & (~bearish)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T05_E(df, correl_window=20, adx_window=10, roc_window=5, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    vn30_close = df.get("vn30_close", close)
    dji_close = df.get("dji_close", close)
    fut_vn30_correl = ma.rolling_correlation(close, vn30_close, correl_window)
    fut_dji_correl = ma.rolling_correlation(close, dji_close, correl_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    roc_val = momentum.roc(close, roc_window)
    correl_aligned = (fut_vn30_correl > 0.5) & (fut_dji_correl > 0)
    correl_negative = (fut_vn30_correl < -0.3) | (fut_dji_correl < -0.3)
    long_setup = correl_aligned & (roc_val > 0) & (adx_val > adx_entry)
    short_setup = correl_aligned & (roc_val < 0) & (adx_val > adx_entry)
    exit_setup = correl_negative | op.crossed_below(adx_val, adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T05_F(df, rs_window=20, **kwargs):
    close = df["close"].values
    vn30_close = df.get("vn30_close", close)
    ratio = close / np.maximum(vn30_close, 1e-10)
    ratio_sma = ma.sma(ratio, rs_window)
    ratio_roc = momentum.roc(ratio, rs_window)
    ratio_slope = ma.linearreg_slope(ratio, rs_window)
    long_setup = (ratio > ratio_sma) & (ratio_roc > 0) & (ratio_slope > 0)
    short_setup = (ratio < ratio_sma) & (ratio_roc < 0) & (ratio_slope < 0)
    exit_setup = op.crossed_below(ratio, ratio_sma) | op.crossed_above(ratio, ratio_sma)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T05_G(df, correl_window=20, adx_window=10, vol_window=14, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    vn30_close = df.get("vn30_close", close)
    correl = ma.rolling_correlation(close, vn30_close, correl_window)
    correl_sma = ma.sma(correl, correl_window)
    correl_std = ma.rolling_std(correl, correl_window)
    breakdown = correl < (correl_sma - 2 * correl_std)
    rebuilding = op.crossed_above(correl, correl_sma)
    adx_val = momentum.adx(high, low, close, adx_window)
    vol_sma = ma.sma(volume, vol_window)
    long_setup = breakdown & (volume > vol_sma * 1.5) & (adx_val > adx_entry)
    short_setup = breakdown & (volume > vol_sma * 1.5) & (adx_val > adx_entry)
    exit_setup = rebuilding | op.crossed_below(adx_val, adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)
