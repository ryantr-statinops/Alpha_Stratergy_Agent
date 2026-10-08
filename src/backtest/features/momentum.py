"""Momentum indicators — reimplementing self.feat.* using TA-Lib."""
import talib
import numpy as np


def rsi(series, timeperiod=14):
    return talib.RSI(np.asarray(series), timeperiod=timeperiod)


def roc(series, timeperiod=10):
    return talib.ROC(np.asarray(series), timeperiod=timeperiod)


def mom(series, timeperiod=10):
    return talib.MOM(np.asarray(series), timeperiod=timeperiod)


def cmo(series, timeperiod=14):
    return talib.CMO(np.asarray(series), timeperiod=timeperiod)


def macd(series, fastperiod=12, slowperiod=26, signalperiod=9):
    macd_val, macd_signal, macd_hist = talib.MACD(
        np.asarray(series), fastperiod=fastperiod,
        slowperiod=slowperiod, signalperiod=signalperiod
    )
    return macd_val, macd_signal, macd_hist


def adx(high, low, close, timeperiod=14):
    return talib.ADX(np.asarray(high), np.asarray(low), np.asarray(close), timeperiod=timeperiod)


def adxr(high, low, close, timeperiod=14):
    return talib.ADXR(np.asarray(high), np.asarray(low), np.asarray(close), timeperiod=timeperiod)


def aroon(high, low, timeperiod=14):
    aroon_down, aroon_up = talib.AROON(np.asarray(high), np.asarray(low), timeperiod=timeperiod)
    return aroon_up, aroon_down


def aroonosc(high, low, timeperiod=14):
    return talib.AROONOSC(np.asarray(high), np.asarray(low), timeperiod=timeperiod)


def apo(series, fastperiod=12, slowperiod=26, matype=0):
    return talib.APO(np.asarray(series), fastperiod=fastperiod, slowperiod=slowperiod, matype=matype)


def ppo(series, fastperiod=12, slowperiod=26, matype=0):
    return talib.PPO(np.asarray(series), fastperiod=fastperiod, slowperiod=slowperiod, matype=matype)


def returns(close, periods=1):
    arr = np.asarray(close, dtype=float)
    ret = np.diff(arr, prepend=np.nan) / np.nan_to_num(np.roll(arr, 1), nan=1.0)
    ret[0] = np.nan
    return ret
