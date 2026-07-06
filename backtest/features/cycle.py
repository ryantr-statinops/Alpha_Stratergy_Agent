"""Cycle indicators — Hilbert Transform, DCPeriod using TA-Lib."""
import talib
import numpy as np


def ht_trendline(close):
    return talib.HT_TRENDLINE(np.asarray(close))


def sine(close):
    sine, leadsine = talib.HT_SINE(np.asarray(close))
    return sine, leadsine


def dcperiod(close):
    return talib.HT_DCPERIOD(np.asarray(close))


def dcphase(close):
    return talib.HT_DCPHASE(np.asarray(close))


def trendmode(close):
    return talib.HT_TRENDMODE(np.asarray(close))


def phasor(close):
    inphase, quadrature = talib.HT_PHASOR(np.asarray(close))
    return inphase, quadrature
