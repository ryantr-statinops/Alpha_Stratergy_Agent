"""Volume indicators — OBV, MFI, CMF, BOP, ADOSC using TA-Lib."""
import talib
import numpy as np
import pandas as pd


def obv(close, volume):
    return talib.OBV(np.asarray(close), np.asarray(volume))


def mfi(high, low, close, volume, timeperiod=14):
    return talib.MFI(np.asarray(high), np.asarray(low), np.asarray(close), np.asarray(volume), timeperiod=timeperiod)


def ad(high, low, close, volume):
    return talib.AD(np.asarray(high), np.asarray(low), np.asarray(close), np.asarray(volume))


def adosc(high, low, close, volume, fastperiod=3, slowperiod=10):
    return talib.ADOSC(np.asarray(high), np.asarray(low), np.asarray(close), np.asarray(volume),
                       fastperiod=fastperiod, slowperiod=slowperiod)


def bop(open_price, high, low, close):
    return talib.BOP(np.asarray(open_price), np.asarray(high), np.asarray(low), np.asarray(close))


def cmf(high, low, close, volume, timeperiod=20):
    money_flow_vol = ((close * 2 - high - low) / (high - low).replace(0, np.nan) * close * volume).to_numpy()
    vol = np.asarray(volume)
    mf = pd.Series(money_flow_vol).rolling(timeperiod).sum()
    v = pd.Series(vol).rolling(timeperiod).sum()
    return (mf / v).to_numpy()
