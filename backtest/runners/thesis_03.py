"""Thesis 03: Time-Series Decomposition — template implementations."""
import numpy as np
import pandas as pd
from backtest.features import ma, momentum, cycle, operators as op
from backtest.runners.base import compute_positions


def T03_A(df, adx_window=10, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    trend = cycle.ht_trendline(close)
    sine_val, leadsine = cycle.sine(close)
    cycle_mode = cycle.trendmode(close) == 0
    trend_mode = cycle.trendmode(close) == 1
    adx_val = momentum.adx(high, low, close, adx_window)

    cycle_long = (sine_val > leadsine) & cycle_mode & (close > trend)
    cycle_short = (sine_val < leadsine) & cycle_mode & (close < trend)
    trend_long = (close > trend) & trend_mode & (adx_val > adx_entry)
    trend_short = (close < trend) & trend_mode & (adx_val > adx_entry)

    long_setup = cycle_long | trend_long
    short_setup = cycle_short | trend_short
    exit_setup = op.crossed_below(close, trend) | op.crossed_above(close, trend) | (adx_val < adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T03_B(df, base_window=14, max_cycle_period=30, adx_window=10, roc_window=5, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    cycle_period = cycle.dcperiod(close)
    trend = cycle.ht_trendline(close)
    adx_val = momentum.adx(high, low, close, base_window)
    roc_val = momentum.roc(close, roc_window)
    long_setup = (close > trend) & (roc_val > 0) & (adx_val > adx_entry)
    short_setup = (close < trend) & (roc_val < 0) & (adx_val > adx_entry)
    exit_setup = op.crossed_below(close, trend) | op.crossed_above(close, trend) | (adx_val < adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T03_C(df, lr_window=14, adx_window=10, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    slope = ma.linearreg_slope(close, lr_window)
    angle = ma.linearreg_angle(close, lr_window)
    forecast = ma.tsf(close, lr_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    long_setup = (slope > 0) & (angle > 5) & (close < forecast) & (adx_val > adx_entry)
    short_setup = (slope < 0) & (angle < -5) & (close > forecast) & (adx_val > adx_entry)
    exit_setup = op.crossed_below(slope, 0) | op.crossed_above(slope, 0) | (adx_val < adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T03_D(df, rsi_window=14, adx_window=10, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    sine_val, leadsine = cycle.sine(close)
    rsi_val = momentum.rsi(close, rsi_window)
    trend = cycle.ht_trendline(close)
    adx_val = momentum.adx(high, low, close, adx_window)
    cycle_up = op.crossed_above(sine_val, leadsine)
    cycle_down = op.crossed_below(sine_val, leadsine)
    long_setup = cycle_up & (rsi_val > 30) & (adx_val > adx_entry)
    short_setup = cycle_down & (rsi_val < 70) & (adx_val > adx_entry)
    exit_setup = op.crossed_below(close, trend) | op.crossed_above(close, trend) | (adx_val < adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)


def T03_E(df, mad_window=14, ema_window=13, adx_window=10, adx_entry=22, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    mad = ma.rolling_mad(close, mad_window)
    std = ma.rolling_std(close, mad_window)
    mad_ratio = mad / np.maximum(std, 1e-10)
    mad_ratio_sma = ma.sma(mad_ratio, mad_window)
    structured = mad_ratio < mad_ratio_sma * 0.8
    chaotic = mad_ratio > mad_ratio_sma * 1.2
    ema_val = ma.ema(close, ema_window)
    adx_val = momentum.adx(high, low, close, adx_window)
    long_setup = (close > ema_val) & structured & (adx_val > adx_entry)
    short_setup = (close < ema_val) & structured & (adx_val > adx_entry)
    exit_setup = op.crossed_below(close, ema_val) | op.crossed_above(close, ema_val) | chaotic | (adx_val < adx_exit)
    return compute_positions(df, long_setup, short_setup, exit_setup)
