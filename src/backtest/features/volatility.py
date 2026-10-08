"""Volatility indicators — ATR, BBands, NATR using TA-Lib."""
import talib
import numpy as np
import pandas as pd


def atr(high, low, close, timeperiod=14):
    return talib.ATR(np.asarray(high), np.asarray(low), np.asarray(close), timeperiod=timeperiod)


def natr(high, low, close, timeperiod=14):
    return talib.NATR(np.asarray(high), np.asarray(low), np.asarray(close), timeperiod=timeperiod)


def bbands(series, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0):
    upper, mid, lower = talib.BBANDS(
        np.asarray(series), timeperiod=timeperiod,
        nbdevup=nbdevup, nbdevdn=nbdevdn, matype=matype
    )
    return upper, mid, lower


def price_z(series, timeperiod=20):
    mean = pd.Series(series).rolling(timeperiod).mean()
    std = pd.Series(series).rolling(timeperiod).std()
    return ((pd.Series(series) - mean) / std.replace(0, np.nan)).to_numpy()


def volume_z(volume, timeperiod=20):
    mean = pd.Series(volume).rolling(timeperiod).mean()
    std = pd.Series(volume).rolling(timeperiod).std()
    return ((pd.Series(volume) - mean) / std.replace(0, np.nan)).to_numpy()
