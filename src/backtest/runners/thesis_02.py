"""Thesis 02: Volatility Regime — template implementations."""
import numpy as np
import pandas as pd
from backtest.features import ma, momentum, volatility, operators as op
from backtest.runners.base import compute_positions


def T02_A(df, vol_window=14, vol_entry=1.5, adx_window=7, roc_window=3, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    atr_val = volatility.atr(high, low, close, vol_window)
    atr_sma = ma.sma(atr_val, vol_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    vol_expansion = atr_val > atr_sma * vol_entry
    roc_val = momentum.roc(close, roc_window)
    long_setup = vol_expansion & (roc_val > 0) & (adx_val > adx_entry)
    short_setup = vol_expansion & (roc_val < 0) & (adx_val > adx_entry)
    exit_setup = (atr_val < atr_sma) | op.crossed_below(adx_val, adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T02_B(df, vol_window=14, vol_compress=0.7, rsi_window=14, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    atr_val = volatility.atr(high, low, close, vol_window)
    atr_sma = ma.sma(atr_val, vol_window)
    rsi_val = momentum.rsi(close, rsi_window)
    vol_compression = atr_val < atr_sma * vol_compress
    long_setup = vol_compression & (rsi_val < 30)
    short_setup = vol_compression & (rsi_val > 70)
    exit_setup = op.crossed_above(rsi_val, 50) | op.crossed_below(rsi_val, 50)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T02_C(df, adx_window=14, vol_window=14, roc_window=3, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    adx_val = momentum.adx(high, low, close, adx_window)
    atr_val = volatility.atr(high, low, close, vol_window)
    atr_sma = ma.sma(atr_val, vol_window)
    vol_sma = ma.sma(volume, vol_window)
    vol_ratio = volume / np.maximum(vol_sma, 1e-10)
    vol_regime = ma.rolling_std(atr_val, vol_window)
    vol_regime_sma = ma.sma(vol_regime, vol_window)
    roc_fast = momentum.roc(close, roc_window)
    upper_q = ma.rolling_quantile(close, 20, 0.8)
    lower_q = ma.rolling_quantile(close, 20, 0.2)

    momentum_mode = (adx_val > 25) & (vol_regime > vol_regime_sma)
    meanrev_mode = (adx_val < 22) & (vol_regime < vol_regime_sma)

    mom_long = momentum_mode & (roc_fast > 0) & (volume > vol_sma)
    mom_short = momentum_mode & (roc_fast < 0) & (volume > vol_sma)
    mr_long = meanrev_mode & (close < lower_q) & (volume < vol_sma)
    mr_short = meanrev_mode & (close > upper_q) & (volume < vol_sma)

    long_setup = mom_long | mr_long
    short_setup = mom_short | mr_short
    exit_setup = op.crossed_below(adx_val, 15) | (adx_val < 18)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T02_D(df, atr_window=14, atr_mult=2, ema_window=13, adx_window=7, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    atr_val = volatility.atr(high, low, close, atr_window)
    ema_val = ma.ema(close, ema_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    long_setup = (close > ema_val) & (adx_val > adx_entry) & (close > (close - atr_val * atr_mult))
    short_setup = (close < ema_val) & (adx_val > adx_entry) & (close < (close + atr_val * atr_mult))
    exit_setup = op.crossed_below(close, ema_val) | op.crossed_above(close, ema_val)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T02_E(df, natr_window=14, adx_window=7, roc_window=3, rsi_window=14, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    natr_val = volatility.natr(high, low, close, natr_window)
    natr_sma = ma.sma(natr_val, natr_window)
    adx_val = momentum.adx(high, low, close, adx_window)

    high_vol = natr_val > natr_sma * 1.3
    low_vol = natr_val < natr_sma * 0.7

    roc_val = momentum.roc(close, roc_window)
    rsi_val = momentum.rsi(close, rsi_window)

    long_trend = high_vol & (roc_val > 0) & (adx_val > adx_entry)
    short_trend = high_vol & (roc_val < 0) & (adx_val > adx_entry)
    long_rev = low_vol & (rsi_val < 30) & (adx_val < 20)
    short_rev = low_vol & (rsi_val > 70) & (adx_val < 20)

    long_setup = long_trend | long_rev
    short_setup = short_trend | short_rev
    exit_setup = op.crossed_below(adx_val, 15) | (natr_val < natr_sma * 0.5)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T02_F(df, kama_window=20, adx_window=7, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    kama_val = ma.kama(close, kama_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    long_setup = (close > kama_val) & (adx_val > adx_entry)
    short_setup = (close < kama_val) & (adx_val > adx_entry)
    exit_setup = op.crossed_below(close, kama_val) | op.crossed_above(close, kama_val) | (adx_val < adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)
