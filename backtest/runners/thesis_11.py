"""Thesis 11: VWAP Basis Reversion — template implementations."""
import numpy as np
from backtest.features import ma, momentum, volatility, operators as op
from backtest.runners.base import compute_positions


def T11_A(df, vwap_window=20, z_entry=2.0, z_exit=1.0, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    vn30_close = df.get("vn30_close", close)

    vwap_val = np.asarray(ma.vwap(high, low, close, volume, vwap_window))
    vwap_dist = close - vwap_val
    vwap_dist_z = np.asarray(ma.rolling_zscore(vwap_dist, vwap_window))

    basis = close - vn30_close
    basis_z = np.asarray(ma.rolling_zscore(basis, vwap_window))

    long_setup = (vwap_dist_z < -z_entry) & (basis_z < -z_entry)
    short_setup = (vwap_dist_z > z_entry) & (basis_z > z_entry)
    exit_setup = (np.abs(vwap_dist_z) < z_exit) | (np.abs(basis_z) < z_exit)

    return compute_positions(df, long_setup, short_setup, exit_setup)


def T11_B(df, vwap_window=20, z_entry=2.0, z_exit=1.0,
          adx_window=14, adx_max=20, adx_exit=15, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    vn30_close = df.get("vn30_close", close)

    vwap_val = np.asarray(ma.vwap(high, low, close, volume, vwap_window))
    vwap_dist = close - vwap_val
    vwap_dist_z = np.asarray(ma.rolling_zscore(vwap_dist, vwap_window))

    basis = close - vn30_close
    basis_z = np.asarray(ma.rolling_zscore(basis, vwap_window))

    adx_val = momentum.adx(high, low, close, adx_window)
    trend_ok = adx_val < adx_max

    long_setup = (vwap_dist_z < -z_entry) & (basis_z < -z_entry) & trend_ok
    short_setup = (vwap_dist_z > z_entry) & (basis_z > z_entry) & trend_ok
    exit_setup = (
        (np.abs(vwap_dist_z) < z_exit) | (np.abs(basis_z) < z_exit) |
        (adx_val > adx_exit)
    )

    return compute_positions(df, long_setup, short_setup, exit_setup)


def T11_C(df, vwap_window=20, z_entry=2.0, z_exit=1.0,
          atr_stop_mult=2.5, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    vn30_close = df.get("vn30_close", close)

    vwap_val = np.asarray(ma.vwap(high, low, close, volume, vwap_window))
    vwap_dist = close - vwap_val
    vwap_dist_z = np.asarray(ma.rolling_zscore(vwap_dist, vwap_window))

    basis = close - vn30_close
    basis_z = np.asarray(ma.rolling_zscore(basis, vwap_window))

    atr_val = volatility.atr(high, low, close, 14)
    ma20 = ma.sma(close, 20)
    atr_stop = (
        (close < ma20 - atr_stop_mult * atr_val) |
        (close > ma20 + atr_stop_mult * atr_val)
    )

    long_setup = (vwap_dist_z < -z_entry) & (basis_z < -z_entry)
    short_setup = (vwap_dist_z > z_entry) & (basis_z > z_entry)
    exit_setup = (
        (np.abs(vwap_dist_z) < z_exit) | (np.abs(basis_z) < z_exit) |
        atr_stop
    )

    return compute_positions(df, long_setup, short_setup, exit_setup)


def T11_D(df, vwap_window=20, z_entry=2.0, z_exit=1.0,
          adx_window=14, adx_entry=22, adx_exit=15,
          return_window=5, atr_stop_mult=2.5, **kwargs):
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    vn30_close = df.get("vn30_close", close)

    vwap_val = np.asarray(ma.vwap(high, low, close, volume, vwap_window))
    vwap_dist = close - vwap_val
    vwap_dist_z = np.asarray(ma.rolling_zscore(vwap_dist, vwap_window))

    basis = close - vn30_close
    basis_z = np.asarray(ma.rolling_zscore(basis, vwap_window))

    adx_val = momentum.adx(high, low, close, adx_window)
    ranging = adx_val < adx_exit
    trending = adx_val > adx_entry

    atr_val = volatility.atr(high, low, close, 14)
    ma20 = ma.sma(close, 20)
    atr_stop = (
        (close < ma20 - atr_stop_mult * atr_val) |
        (close > ma20 + atr_stop_mult * atr_val)
    )

    return_1 = op.fillna(op.pct_change(close, 1), 0)
    return_roll = np.asarray(ma.rolling_mean(return_1, return_window))

    range_to_trend = np.asarray(op.crossed_above(adx_val, adx_entry))
    trend_to_range = np.asarray(op.crossed_below(adx_val, adx_exit))

    mr_long = ranging & (vwap_dist_z < -z_entry) & (basis_z < -z_entry)
    mr_short = ranging & (vwap_dist_z > z_entry) & (basis_z > z_entry)

    tf_long = trending & (close > vwap_val) & (basis > 0) & (return_roll > 0)
    tf_short = trending & (close < vwap_val) & (basis < 0) & (return_roll < 0)

    exit_setup = (
        (np.abs(vwap_dist_z) < z_exit) |
        (np.abs(basis_z) < z_exit) |
        range_to_trend | trend_to_range |
        atr_stop
    )

    long_signal = (tf_long | (mr_long & ~trending)) & (~exit_setup)
    short_signal = (tf_short | (mr_short & ~trending)) & (~exit_setup)

    return compute_positions(df, long_signal, short_signal, exit_setup)
