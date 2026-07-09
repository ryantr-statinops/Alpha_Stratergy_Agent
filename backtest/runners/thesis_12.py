"""Thesis 12: Kalman Filter Regime Switching — aligned with XNOQuant templates."""
import warnings
import numpy as np
from backtest.features import ma, momentum, volatility, operators as op
from backtest.features.kalman import kalman_1d, kalman_2d, kalman_proxy

warnings.filterwarnings("ignore", "Mean of empty slice")


def T12_A(df, kf_window=10, sideways_buffer=0.02,
          kf_z_entry=1.5, kf_z_mr_entry=2.0,
          adx_window=14, adx_entry=20, adx_exit=15, atr_stop_mult=2.5, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values

    kalman_state = ma.sma(close, kf_window)
    kf_dev = close / np.maximum(kalman_state, 1e-10) - 1
    kf_residual = close - kalman_state
    residual_std = np.asarray(ma.rolling_std(kf_residual, 20))
    kf_z = kf_residual / np.maximum(residual_std, 1e-10)

    adx_val = momentum.adx(high, low, close, adx_window)
    atr_val = volatility.atr(high, low, close, 14)

    kf_trend_up = kf_dev > sideways_buffer
    kf_trend_down = kf_dev < -sideways_buffer
    kf_sideways = ~kf_trend_up & ~kf_trend_down

    atr_stop_long = close < kalman_state - atr_stop_mult * atr_val
    atr_stop_short = close > kalman_state + atr_stop_mult * atr_val

    dip_long = kf_trend_up & (kf_z < -kf_z_entry) & (adx_val > adx_entry)
    rally_short = kf_trend_down & (kf_z > kf_z_entry) & (adx_val > adx_entry)
    mr_long = kf_sideways & (kf_z < -kf_z_mr_entry)
    mr_short = kf_sideways & (kf_z > kf_z_mr_entry)

    long_setup = np.asarray(dip_long | mr_long)
    short_setup = np.asarray(rally_short | mr_short)
    exit_long = np.asarray(
        op.crossed_below(kf_z, -0.2) | (adx_val < adx_exit) | atr_stop_long
    )
    exit_short = np.asarray(
        op.crossed_above(kf_z, 0.2) | (adx_val < adx_exit) | atr_stop_short
    )

    long_signal = long_setup
    short_signal = short_setup

    n = len(df)
    pos = np.zeros(n, dtype=float)
    last = 0.0
    for i in range(n):
        if last > 0:
            if exit_long[i]:
                last = 0.0
            elif short_signal[i]:
                last = -1.0
        elif last < 0:
            if exit_short[i]:
                last = 0.0
            elif long_signal[i]:
                last = 1.0
        else:
            if long_signal[i]:
                last = 1.0
            elif short_signal[i]:
                last = -1.0
        pos[i] = last
    return pos


def T12_B(df, kf_window=10, sideways_buffer=0.02,
          kf_z_mr_entry=2.0,
          adx_window=14, adx_entry=20, adx_exit=15, atr_stop_mult=2.5, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values

    kalman_state = ma.sma(close, kf_window)
    kf_residual = close - kalman_state
    residual_std = np.asarray(ma.rolling_std(kf_residual, 20))
    kf_z = kf_residual / np.maximum(residual_std, 1e-10)
    kf_dev = close / np.maximum(kalman_state, 1e-10) - 1

    adx_val = momentum.adx(high, low, close, adx_window)
    atr_val = volatility.atr(high, low, close, 14)

    kf_trend_up = kf_dev > sideways_buffer
    kf_trend_down = kf_dev < -sideways_buffer
    kf_sideways = ~kf_trend_up & ~kf_trend_down

    atr_stop_long = close < kalman_state - atr_stop_mult * atr_val
    atr_stop_short = close > kalman_state + atr_stop_mult * atr_val

    dip_long = kf_trend_up & (kf_z < -1.0) & (adx_val > adx_entry)
    rally_short = kf_trend_down & (kf_z > 1.0) & (adx_val > adx_entry)
    mr_long = kf_sideways & (kf_z < -kf_z_mr_entry)
    mr_short = kf_sideways & (kf_z > kf_z_mr_entry)

    long_setup = np.asarray(dip_long | mr_long)
    short_setup = np.asarray(rally_short | mr_short)
    exit_long = np.asarray(
        op.crossed_below(kf_z, -0.2) | (adx_val < adx_exit) | atr_stop_long
    )
    exit_short = np.asarray(
        op.crossed_above(kf_z, 0.2) | (adx_val < adx_exit) | atr_stop_short
    )

    long_signal = long_setup
    short_signal = short_setup

    n = len(df)
    pos = np.zeros(n, dtype=float)
    last = 0.0
    for i in range(n):
        if last > 0:
            if exit_long[i]:
                last = 0.0
            elif short_signal[i]:
                last = -1.0
        elif last < 0:
            if exit_short[i]:
                last = 0.0
            elif long_signal[i]:
                last = 1.0
        else:
            if long_signal[i]:
                last = 1.0
            elif short_signal[i]:
                last = -1.0
        pos[i] = last
    return pos


def T12_C(df, kf_window=10, sideways_buffer=0.02,
          kf_z_entry=1.5, kf_z_mr_entry=2.0,
          adx_window=14, adx_entry=20, adx_exit=15, atr_stop_mult=2.5, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values

    kalman_state = ma.sma(close, kf_window)
    kf_residual = close - kalman_state
    residual_std = np.asarray(ma.rolling_std(kf_residual, 20))
    kf_z = kf_residual / np.maximum(residual_std, 1e-10)
    kf_dev = close / np.maximum(kalman_state, 1e-10) - 1

    adx_val = momentum.adx(high, low, close, adx_window)
    atr_val = volatility.atr(high, low, close, 14)

    kf_trend_up = kf_dev > sideways_buffer
    kf_trend_down = kf_dev < -sideways_buffer
    kf_sideways = ~kf_trend_up & ~kf_trend_down

    atr_stop_long = close < kalman_state - atr_stop_mult * atr_val
    atr_stop_short = close > kalman_state + atr_stop_mult * atr_val

    dip_long = kf_trend_up & (kf_z < -kf_z_entry) & (adx_val > adx_entry)
    rally_short = kf_trend_down & (kf_z > kf_z_entry) & (adx_val > adx_entry)
    mr_long = kf_sideways & (kf_z < -kf_z_mr_entry) & (adx_val < adx_entry)
    mr_short = kf_sideways & (kf_z > kf_z_mr_entry) & (adx_val < adx_entry)

    long_setup = np.asarray(dip_long | mr_long)
    short_setup = np.asarray(rally_short | mr_short)
    exit_long = np.asarray(
        op.crossed_below(kf_z, -0.2) | (adx_val < adx_exit) | atr_stop_long
    )
    exit_short = np.asarray(
        op.crossed_above(kf_z, 0.2) | (adx_val < adx_exit) | atr_stop_short
    )

    long_signal = long_setup
    short_signal = short_setup

    n = len(df)
    pos = np.zeros(n, dtype=float)
    last = 0.0
    for i in range(n):
        if last > 0:
            if exit_long[i]:
                last = 0.0
            elif short_signal[i]:
                last = -1.0
        elif last < 0:
            if exit_short[i]:
                last = 0.0
            elif long_signal[i]:
                last = 1.0
        else:
            if long_signal[i]:
                last = 1.0
            elif short_signal[i]:
                last = -1.0
        pos[i] = last
    return pos


def T12_D(df, kf_window=10, sideways_buffer=0.02,
          kf_z_entry=1.5, kf_z_mr_entry=2.0,
          adx_window=14, adx_entry=20, adx_exit=15, atr_stop_mult=2.5, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values

    kalman_state, kf_residual = kalman_proxy(close, kf_window)
    kf_residual = np.asarray(kf_residual)
    residual_std = np.asarray(ma.rolling_std(kf_residual, 20))
    kf_z = kf_residual / np.maximum(residual_std, 1e-10)
    kf_dev = close / np.maximum(kalman_state, 1e-10) - 1

    adx_val = momentum.adx(high, low, close, adx_window)
    atr_val = volatility.atr(high, low, close, 14)

    kf_trend_up = kf_dev > sideways_buffer
    kf_trend_down = kf_dev < -sideways_buffer
    kf_sideways = ~kf_trend_up & ~kf_trend_down

    atr_stop_long = close < kalman_state - atr_stop_mult * atr_val
    atr_stop_short = close > kalman_state + atr_stop_mult * atr_val

    residual_z = np.asarray(ma.rolling_zscore(kf_residual, 20))

    dip_long = kf_trend_up & (kf_z < -kf_z_entry) & (residual_z < -1.0) & (adx_val > adx_entry)
    rally_short = kf_trend_down & (kf_z > kf_z_entry) & (residual_z > 1.0) & (adx_val > adx_entry)
    mr_long = kf_sideways & (kf_z < -kf_z_mr_entry) & (residual_z < -1.5)
    mr_short = kf_sideways & (kf_z > kf_z_mr_entry) & (residual_z > 1.5)

    long_setup = np.asarray(dip_long | mr_long)
    short_setup = np.asarray(rally_short | mr_short)
    exit_long = np.asarray(
        op.crossed_below(kf_z, -0.2) | (adx_val < adx_exit) | atr_stop_long
    )
    exit_short = np.asarray(
        op.crossed_above(kf_z, 0.2) | (adx_val < adx_exit) | atr_stop_short
    )

    long_signal = long_setup
    short_signal = short_setup

    n = len(df)
    pos = np.zeros(n, dtype=float)
    last = 0.0
    for i in range(n):
        if last > 0:
            if exit_long[i]:
                last = 0.0
            elif short_signal[i]:
                last = -1.0
        elif last < 0:
            if exit_short[i]:
                last = 0.0
            elif long_signal[i]:
                last = 1.0
        else:
            if long_signal[i]:
                last = 1.0
            elif short_signal[i]:
                last = -1.0
        pos[i] = last
    return pos