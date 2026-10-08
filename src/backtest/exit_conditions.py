import numpy as np
import pandas as pd
from backtest.features.momentum import adx
from backtest.features.volatility import natr
from backtest.features.ma import sma, rolling_mean, rolling_std
from backtest.features.operators import fillna, pct_change


def compute_exit(df: pd.DataFrame,
                 position: np.ndarray,
                 adx_window: int = 14,
                 adx_exit: float = 15,
                 return_window: int = 5,
                 return_exit_threshold: float = 0.0,
                 natr_window: int = 14,
                 vol_exit_mult: float = 2.0) -> np.ndarray:
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values

    n = len(close)
    exit_signal = np.zeros(n, dtype=bool)

    # Layer 1: Trend exit (ADX threshold)
    adx_val = adx(high, low, close, timeperiod=adx_window)
    trend_exit = adx_val < adx_exit
    exit_signal = exit_signal | trend_exit

    # Layer 2: Momentum reversal exit (dynamic threshold based on vol)
    return_1 = fillna(pct_change(pd.Series(close), periods=1), value=0)
    return_roll = rolling_mean(return_1, window=return_window)
    return_std = rolling_std(return_1.values, window=20)
    effective_threshold = return_exit_threshold if return_exit_threshold > 0 else 0.5
    mom_exit = np.zeros(n, dtype=bool)
    for i in range(1, n):
        thresh = effective_threshold * return_std[i] if return_std[i] > 0 else 0.0001
        if position[i] > 0 and return_roll[i] < -thresh:
            mom_exit[i] = True
        elif position[i] < 0 and return_roll[i] > thresh:
            mom_exit[i] = True
    exit_signal = exit_signal | mom_exit

    # Layer 3: Volatility explosion exit
    natr_val = natr(high, low, close, timeperiod=natr_window)
    natr_ma = sma(natr_val, timeperiod=natr_window)
    vol_exit = natr_val > natr_ma * vol_exit_mult
    exit_signal = exit_signal | vol_exit

    return exit_signal


def apply_freeze_protection(equity_curve: np.ndarray,
                            max_dd_allowed: float = -0.10,
                            lookback: int = 20) -> np.ndarray:
    n = len(equity_curve)
    frozen = np.zeros(n, dtype=bool)
    if n < lookback:
        return frozen

    peak = np.maximum.accumulate(equity_curve)
    dd = (equity_curve - peak) / (peak + 1e-10)
    in_drawdown = False
    recovery_threshold = 1 - abs(max_dd_allowed) / 2

    for i in range(lookback, n):
        if not in_drawdown:
            if dd[i] < max_dd_allowed:
                in_drawdown = True
                frozen[i] = True
        else:
            frozen[i] = True
            if equity_curve[i] >= peak[i] * recovery_threshold:
                in_drawdown = False
                frozen[i] = False

    return frozen
