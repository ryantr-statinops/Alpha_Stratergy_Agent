"""Thesis 11: VWAP Basis Reversion — template implementations.

All variants use regime-switching architecture:
  - Mean reversion (MR)     : dual z-score extremes when no strong trend
  - Trend following (TF)    : ATR band breakout or ADX trending
  - Exit only on z-score neutral, blocked by opposing trend direction
"""
import numpy as np
from backtest.features import ma, momentum, volatility, operators as op
from backtest.runners.base import compute_positions


def _vwap_basis_core(df, vwap_window):
    """Shared VWAP + basis z-score computation."""
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

    return close, high, low, vwap_val, vwap_dist_z, basis_z, basis


def _atr_band(close, high, low, mult):
    """ATR band around 20-period MA."""
    atr_val = volatility.atr(high, low, close, 14)
    ma20 = ma.sma(close, 20)
    trend_up = close > ma20 + mult * atr_val
    trend_down = close < ma20 - mult * atr_val
    return trend_up, trend_down


def _regime_entry(vwap_dist_z, basis_z, z_entry, trend_up, trend_down):
    """MR gated by trend direction + exclusive TF."""
    mr_long = (vwap_dist_z < -z_entry) & (basis_z < -z_entry) & (~trend_down)
    mr_short = (vwap_dist_z > z_entry) & (basis_z > z_entry) & (~trend_up)
    tf_long = trend_up
    tf_short = trend_down

    long_setup = mr_long | tf_long
    short_setup = mr_short | tf_short
    return long_setup, short_setup


def _zscore_exit(vwap_dist_z, basis_z, z_exit, trend_up, trend_down):
    """Exit on z-score neutral, blocked when trend is active."""
    exit_reversion = (np.abs(vwap_dist_z) < z_exit) | (np.abs(basis_z) < z_exit)
    final_exit = exit_reversion & (~trend_up) & (~trend_down)
    return final_exit


def T11_A(df, vwap_window=20, z_entry=2.0, z_exit=1.0, **kwargs):
    close, high, low, vwap_val, vwap_dist_z, basis_z, basis = \
        _vwap_basis_core(df, vwap_window)
    trend_up, trend_down = _atr_band(close, high, low, 2.5)

    long_setup, short_setup = _regime_entry(
        vwap_dist_z, basis_z, z_entry, trend_up, trend_down)
    exit_setup = _zscore_exit(
        vwap_dist_z, basis_z, z_exit, trend_up, trend_down)

    long_signal = long_setup & (~exit_setup)
    short_signal = short_setup & (~exit_setup)

    pos = compute_positions(df, long_signal, short_signal, exit_setup)
    return pos


def T11_B(df, vwap_window=20, z_entry=2.0, z_exit=1.0,
          adx_window=14, adx_max=20, adx_exit=15, **kwargs):
    close, high, low, vwap_val, vwap_dist_z, basis_z, basis = \
        _vwap_basis_core(df, vwap_window)

    adx_val = momentum.adx(high, low, close, adx_window)

    atr_val = volatility.atr(high, low, close, 14)
    ma20 = ma.sma(close, 20)
    trend_up = (close > ma20 + 2.5 * atr_val) & (adx_val < adx_max)
    trend_down = (close < ma20 - 2.5 * atr_val) & (adx_val < adx_max)

    # MR only when ADX < adx_max (no strong trend), gated by ATR band
    mr_long = (vwap_dist_z < -z_entry) & (basis_z < -z_entry) \
              & (adx_val < adx_max) & (~trend_down)
    mr_short = (vwap_dist_z > z_entry) & (basis_z > z_entry) \
               & (adx_val < adx_max) & (~trend_up)
    tf_long = trend_up
    tf_short = trend_down

    long_setup = mr_long | tf_long
    short_setup = mr_short | tf_short

    exit_reversion = (np.abs(vwap_dist_z) < z_exit) | (np.abs(basis_z) < z_exit)
    exit_adx = adx_val > adx_exit
    exit_setup = (exit_reversion | exit_adx) & (~trend_up) & (~trend_down)

    long_signal = long_setup & (~exit_setup)
    short_signal = short_setup & (~exit_setup)

    pos = compute_positions(df, long_signal, short_signal, exit_setup)
    return pos


def T11_C(df, vwap_window=20, z_entry=2.0, z_exit=1.0,
          atr_stop_mult=2.5, **kwargs):
    close, high, low, vwap_val, vwap_dist_z, basis_z, basis = \
        _vwap_basis_core(df, vwap_window)
    trend_up, trend_down = _atr_band(close, high, low, atr_stop_mult)

    long_setup, short_setup = _regime_entry(
        vwap_dist_z, basis_z, z_entry, trend_up, trend_down)
    exit_setup = _zscore_exit(
        vwap_dist_z, basis_z, z_exit, trend_up, trend_down)

    long_signal = long_setup & (~exit_setup)
    short_signal = short_setup & (~exit_setup)

    pos = compute_positions(df, long_signal, short_signal, exit_setup)
    return pos


def T11_D(df, vwap_window=20, z_entry=2.0, z_exit=1.0,
          adx_window=14, adx_entry=22, adx_exit=15,
          return_window=5, atr_stop_mult=2.5, **kwargs):
    close, high, low, vwap_val, vwap_dist_z, basis_z, basis = \
        _vwap_basis_core(df, vwap_window)

    adx_val = momentum.adx(high, low, close, adx_window)
    ranging = adx_val < adx_exit
    trending = adx_val > adx_entry

    atr_val = volatility.atr(high, low, close, 14)
    ma20 = ma.sma(close, 20)
    trend_up = close > ma20 + atr_stop_mult * atr_val
    trend_down = close < ma20 - atr_stop_mult * atr_val

    return_1 = op.fillna(op.pct_change(close, 1), 0)
    return_roll = np.asarray(ma.rolling_mean(return_1, return_window))

    # Exit events
    range_to_trend = np.asarray(op.crossed_above(adx_val, adx_entry))
    trend_to_range = np.asarray(op.crossed_below(adx_val, adx_exit))

    # MR — only in ranging + no opposing ATR trend
    mr_long = ranging & (vwap_dist_z < -z_entry) & (basis_z < -z_entry) \
              & (~trend_down)
    mr_short = ranging & (vwap_dist_z > z_entry) & (basis_z > z_entry) \
               & (~trend_up)

    # TF — only in trending + ATR trend alignment
    tf_long = trending & (close > vwap_val) & (basis > 0) & (return_roll > 0) \
              & trend_up
    tf_short = trending & (close < vwap_val) & (basis < 0) & (return_roll < 0) \
               & trend_down

    long_setup = mr_long | tf_long
    short_setup = mr_short | tf_short

    exit_reversion = (np.abs(vwap_dist_z) < z_exit) | (np.abs(basis_z) < z_exit)
    exit_regime = range_to_trend | trend_to_range
    exit_setup = (exit_reversion | exit_regime) & (~trend_up) & (~trend_down)

    long_signal = long_setup & (~exit_setup)
    short_signal = short_setup & (~exit_setup)

    pos = compute_positions(df, long_signal, short_signal, exit_setup)
    return pos
