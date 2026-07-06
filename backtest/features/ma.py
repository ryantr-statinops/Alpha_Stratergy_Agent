"""Moving average indicators — reimplementing self.feat.* using TA-Lib + pandas."""
import talib
import pandas as pd
import numpy as np


def sma(series, timeperiod=30):
    return talib.SMA(np.asarray(series), timeperiod=timeperiod)


def ema(series, timeperiod=30):
    return talib.EMA(np.asarray(series), timeperiod=timeperiod)


def wma(series, timeperiod=30):
    return talib.WMA(np.asarray(series), timeperiod=timeperiod)


def dema(series, timeperiod=30):
    return talib.DEMA(np.asarray(series), timeperiod=timeperiod)


def tema(series, timeperiod=30):
    return talib.TEMA(np.asarray(series), timeperiod=timeperiod)


def trima(series, timeperiod=30):
    return talib.TRIMA(np.asarray(series), timeperiod=timeperiod)


def kama(series, timeperiod=30):
    return talib.KAMA(np.asarray(series), timeperiod=timeperiod)


def mama(series):
    mama_out, fama_out = talib.MAMA(np.asarray(series))
    return mama_out, fama_out


def rolling_mean(series, window=20):
    return pd.Series(series).rolling(window).mean()


def rolling_std(series, window=20):
    return pd.Series(series).rolling(window).std()


def rolling_mad(series, window=20):
    return pd.Series(series).rolling(window).apply(lambda x: np.mean(np.abs(x - np.mean(x))), raw=True)


def rolling_quantile(series, window=20, q=0.5):
    return pd.Series(series).rolling(window).quantile(q)


def rolling_zscore(series, window=20):
    mean = rolling_mean(series, window)
    std = rolling_std(series, window)
    return (pd.Series(series) - mean) / std.replace(0, np.nan)


def rolling_correlation(series1, series2, window=20):
    return pd.Series(series1).rolling(window).corr(pd.Series(series2))


def linearreg_slope(series, timeperiod=14):
    return talib.LINEARREG_SLOPE(np.asarray(series), timeperiod=timeperiod)


def linearreg_angle(series, timeperiod=14):
    return talib.LINEARREG_ANGLE(np.asarray(series), timeperiod=timeperiod)


def tsf(series, timeperiod=14):
    return talib.TSF(np.asarray(series), timeperiod=timeperiod)


def beta(series1, series2, timeperiod=5):
    return talib.BETA(np.asarray(series1), np.asarray(series2), timeperiod=timeperiod)


def typprice(high, low, close):
    return (high + low + close) / 3.0


def wclprice(high, low, close):
    return (high * 2 + low * 2 + close) / 5.0


def medprice(high, low):
    return (high + low) / 2.0


def ohlc4(open_price, high, low, close):
    return (open_price + high + low + close) / 4.0


def vwap(high, low, close, volume, window=20):
    tp = typprice(high, low, close)
    tp = pd.Series(tp) if not isinstance(tp, pd.Series) else tp
    vol = pd.Series(volume) if not isinstance(volume, pd.Series) else volume
    return (tp * vol).rolling(window).sum() / vol.rolling(window).sum()
