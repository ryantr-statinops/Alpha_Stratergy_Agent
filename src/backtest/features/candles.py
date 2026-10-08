"""Candlestick pattern detection using TA-Lib."""
import talib
import numpy as np


def hammer(open_price, high, low, close):
    return talib.CDLHAMMER(np.asarray(open_price), np.asarray(high), np.asarray(low), np.asarray(close))


def engulfing_pattern(open_price, high, low, close):
    return talib.CDLENGULFING(np.asarray(open_price), np.asarray(high), np.asarray(low), np.asarray(close))


def morning_star(open_price, high, low, close, penetration=0.3):
    return talib.CDLMORNINGSTAR(np.asarray(open_price), np.asarray(high), np.asarray(low), np.asarray(close), penetration=penetration)


def evening_star(open_price, high, low, close, penetration=0.3):
    return talib.CDLEVENINGSTAR(np.asarray(open_price), np.asarray(high), np.asarray(low), np.asarray(close), penetration=penetration)


def doji(open_price, high, low, close):
    return talib.CDLDOJI(np.asarray(open_price), np.asarray(high), np.asarray(low), np.asarray(close))


def marubozu(open_price, high, low, close):
    return talib.CDLMARUBOZU(np.asarray(open_price), np.asarray(high), np.asarray(low), np.asarray(close))
