"""Reimplementation of XNOQuant self.op.* operators using pandas."""
import pandas as pd
import numpy as np


def crossed_above(series1, series2):
    series1 = pd.Series(series1)
    series2 = pd.Series(series2) if isinstance(series2, (pd.Series, np.ndarray)) else series1.shift(1) * 0 + series2
    return (series1.shift(1) <= series2.shift(1)) & (series1 > series2)


def crossed_below(series1, series2):
    series1 = pd.Series(series1)
    series2 = pd.Series(series2) if isinstance(series2, (pd.Series, np.ndarray)) else series1.shift(1) * 0 + series2
    return (series1.shift(1) >= series2.shift(1)) & (series1 < series2)


def between(series, lower, upper):
    return (series >= lower) & (series <= upper)


def fillna(series, value=0):
    return pd.Series(series).fillna(value)


def pct_change(series, periods=1):
    return pd.Series(series).pct_change(periods=periods)


def previous(series):
    return pd.Series(series).shift(1)


def abs_op(series):
    return np.abs(series)


def clip(series, lo, hi):
    return np.clip(pd.Series(series), lo, hi)


def rolling_min(series, window):
    return pd.Series(series).rolling(window).min()


def rolling_max(series, window):
    return pd.Series(series).rolling(window).max()
