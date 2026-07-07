import numpy as np
import pandas as pd
from backtest.features.momentum import adx, roc
from backtest.features.volatility import natr, atr
from backtest.features.ma import sma, linearreg_slope


def detect_regime(df: pd.DataFrame, tf: str = "1D") -> dict:
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values

    n = len(close)
    if n < 50:
        return {
            "adx_regime": "ranging",
            "vol_regime": "normal",
            "return_regime": "sideways",
            "vola_direction": "stable",
            "regime_score": 0.0,
        }

    adx_val = adx(high, low, close, timeperiod=14)
    adx_slice = adx_val[~np.isnan(adx_val)]
    adx_mean = np.mean(adx_slice[-20:]) if len(adx_slice) >= 20 else np.mean(adx_slice)

    natr_val = natr(high, low, close, timeperiod=14)
    natr_slice = natr_val[~np.isnan(natr_val)]
    if len(natr_slice) >= 20:
        natr_ma = np.mean(natr_slice[-20:])
        natr_current = natr_slice[-1]
        natr_ratio = natr_current / natr_ma if natr_ma > 0 else 1.0
    else:
        natr_ratio = 1.0

    roc_val = roc(close, timeperiod=20)
    roc_slice = roc_val[~np.isnan(roc_val)]
    roc_mean = np.mean(roc_slice[-20:]) if len(roc_slice) >= 20 else 0.0

    atr_val = atr(high, low, close, timeperiod=14)
    atr_slice = atr_val[~np.isnan(atr_val)]
    if len(atr_slice) >= 14:
        slope_arr = linearreg_slope(atr_slice[-10:], timeperiod=10)
        if isinstance(slope_arr, np.ndarray):
            atr_slope = float(slope_arr[~np.isnan(slope_arr)][-1]) if np.any(~np.isnan(slope_arr)) else 0.0
        else:
            atr_slope = float(slope_arr)
    else:
        atr_slope = 0.0

    if adx_mean > 25:
        adx_regime = "trending"
        adx_score = min((adx_mean - 25) / 15, 1.0)
    elif adx_mean >= 20:
        adx_regime = "weak"
        adx_score = (adx_mean - 20) / 5
    else:
        adx_regime = "ranging"
        adx_score = max(1 - (20 - adx_mean) / 20, 0.0)

    if natr_ratio > 1.3:
        vol_regime = "high"
        vol_score = min((natr_ratio - 1.3) / 0.7, 1.0)
    elif natr_ratio < 0.7:
        vol_regime = "low"
        vol_score = max(1 - natr_ratio / 0.7, 0.0)
    else:
        vol_regime = "normal"
        vol_score = 1.0 - abs(natr_ratio - 1.0) / 0.3

    if roc_mean > 0.02:
        return_regime = "uptrend"
        ret_score = min(roc_mean / 0.05, 1.0)
    elif roc_mean < -0.02:
        return_regime = "downtrend"
        ret_score = min(abs(roc_mean) / 0.05, 1.0)
    else:
        return_regime = "sideways"
        ret_score = max(1 - abs(roc_mean) / 0.02, 0.0)

    if atr_slope > 0.001:
        vola_direction = "expanding"
    elif atr_slope < -0.001:
        vola_direction = "compressing"
    else:
        vola_direction = "stable"

    regime_score = 0.35 * adx_score + 0.25 * vol_score + 0.25 * ret_score + 0.15 * min(abs(atr_slope) * 100, 1.0)

    return {
        "adx_regime": adx_regime,
        "vol_regime": vol_regime,
        "return_regime": return_regime,
        "vola_direction": vola_direction,
        "regime_score": round(regime_score, 3),
        "adx_mean": round(adx_mean, 2),
        "natr_ratio": round(natr_ratio, 3),
        "roc_mean": round(roc_mean, 4),
        "atr_slope": round(atr_slope, 6),
    }


def regime_label(regime: dict) -> str:
    parts = [
        regime["adx_regime"],
        regime["vol_regime"],
        regime["vola_direction"],
    ]
    return "_".join(parts)


STRATEGY_REGIME_MAP = {
    # Thesis 01: Rolling Mean
    "T01-A": {"regimes": ["trending", "weak"], "vol": ["normal", "low"]},
    "T01-B": {"regimes": ["trending"], "vol": ["normal"]},
    "T01-C": {"regimes": ["trending", "weak"], "vol": ["normal", "low"]},
    "T01-D": {"regimes": ["trending", "weak"], "vol": ["normal", "high"]},
    "T01-E": {"regimes": ["trending", "weak"], "vol": ["normal", "low"]},
    "T01-F": {"regimes": ["ranging", "weak"], "vol": ["low", "normal"]},
    "T01-G": {"regimes": ["trending"], "vol": ["normal"]},
    # Thesis 02: Volatility Regime
    "T02-A": {"regimes": ["trending"], "vol": ["high", "normal"]},
    "T02-B": {"regimes": ["ranging", "weak"], "vol": ["low"]},
    "T02-C": {"regimes": ["trending", "weak", "ranging"], "vol": ["normal", "low", "high"]},
    "T02-D": {"regimes": ["trending"], "vol": ["normal", "high"]},
    "T02-E": {"regimes": ["trending", "ranging"], "vol": ["high", "low"]},
    "T02-F": {"regimes": ["trending"], "vol": ["normal"]},
    # Thesis 03: Time-Series Decomposition
    "T03-A": {"regimes": ["trending", "weak"], "vol": ["normal"]},
    "T03-B": {"regimes": ["trending"], "vol": ["normal"]},
    "T03-C": {"regimes": ["trending"], "vol": ["normal"]},
    "T03-D": {"regimes": ["ranging", "weak"], "vol": ["low", "normal"]},
    "T03-E": {"regimes": ["trending", "weak"], "vol": ["normal"]},
    # Thesis 04: Microstructure Flow
    "T04-A": {"regimes": ["trending", "weak"], "vol": ["normal"]},
    "T04-B": {"regimes": ["ranging", "weak"], "vol": ["low", "normal"]},
    "T04-C": {"regimes": ["trending"], "vol": ["high"]},
    "T04-D": {"regimes": ["ranging", "weak"], "vol": ["low", "normal"]},
    "T04-E": {"regimes": ["trending", "weak"], "vol": ["normal"]},
    "T04-F": {"regimes": ["trending"], "vol": ["normal"]},
    "T04-G": {"regimes": ["trending", "weak"], "vol": ["normal", "high"]},
    # Thesis 05: Cross-Market
    "T05-A": {"regimes": ["ranging", "weak"], "vol": ["low", "normal"]},
    "T05-B": {"regimes": ["trending", "weak"], "vol": ["normal"]},
    "T05-C": {"regimes": ["ranging", "weak"], "vol": ["low", "normal"]},
    "T05-D": {"regimes": ["trending"], "vol": ["normal"]},
    "T05-E": {"regimes": ["trending", "weak"], "vol": ["normal"]},
    "T05-F": {"regimes": ["trending"], "vol": ["normal"]},
    "T05-G": {"regimes": ["weak", "ranging"], "vol": ["high"]},
    # Thesis 06: Multi-Factor Composite
    "T06-A": {"regimes": ["trending", "weak"], "vol": ["normal"]},
    "T06-B": {"regimes": ["trending", "weak"], "vol": ["normal"]},
    "T06-C": {"regimes": ["trending", "weak", "ranging"], "vol": ["normal", "low", "high"]},
    "T06-D": {"regimes": ["weak", "ranging"], "vol": ["low", "normal"]},
    "T06-E": {"regimes": ["trending", "weak", "ranging"], "vol": ["normal", "low", "high"]},
    # Thesis 07: Intraday Session
    "T07-A": {"regimes": ["trending", "weak"], "vol": ["normal"]},
    "T07-B": {"regimes": ["ranging"], "vol": ["low", "normal"]},
    "T07-C": {"regimes": ["trending"], "vol": ["normal", "high"]},
    "T07-D": {"regimes": ["ranging", "weak"], "vol": ["low", "normal"]},
    "T07-E": {"regimes": ["weak", "ranging"], "vol": ["normal"]},
    # Thesis 08: Key Level Absorption
    "T08-A": {"regimes": ["weak", "ranging"], "vol": ["low", "normal"]},
    "T08-B": {"regimes": ["weak", "trending"], "vol": ["high", "normal"]},
    "T08-C": {"regimes": ["ranging", "weak"], "vol": ["low"]},
    "T08-D": {"regimes": ["weak", "ranging"], "vol": ["normal"]},
    "T08-E": {"regimes": ["trending", "weak"], "vol": ["normal"]},
    # Thesis 09: Institutional Flow Arbitrage
    "T09-A": {"regimes": ["weak", "ranging"], "vol": ["normal", "low"]},
    "T09-B": {"regimes": ["trending", "weak"], "vol": ["normal", "high"]},
    "T09-C": {"regimes": ["weak", "ranging"], "vol": ["normal", "low"]},
    # Thesis 10: Regime-based Mean Reversion
    "T10-A": {"regimes": ["trending", "weak"], "vol": ["normal", "low"]},
    "T10-B": {"regimes": ["trending"], "vol": ["normal", "high"]},
    "T10-C": {"regimes": ["weak", "ranging"], "vol": ["normal", "low"]},
}


def strategy_allowed(regime: dict, base_name: str) -> bool:
    sig = STRATEGY_REGIME_MAP.get(base_name)
    if sig is None:
        return True
    if regime["adx_regime"] not in sig["regimes"]:
        return False
    if regime["vol_regime"] not in sig["vol"]:
        return False
    return True
