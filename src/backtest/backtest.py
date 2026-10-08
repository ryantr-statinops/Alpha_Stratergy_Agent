import numpy as np
import pandas as pd
from backtest.exit_conditions import compute_exit, apply_freeze_protection
from backtest.evaluate import evaluate


def run_strategy(df: pd.DataFrame,
                 position_func: callable,
                 params: dict,
                 timeframe: str = "15m",
                 enable_exit_enhance: bool = True,
                 enable_freeze: bool = True) -> dict:
    raw_pos = position_func(df, **params)
    pos = raw_pos.copy()
    n = len(pos)

    if enable_exit_enhance:
        adx_window = params.get("adx_window", 14)
        adx_exit = params.get("adx_exit", 15)
        return_window = params.get("return_window", 5)
        return_exit_threshold = params.get("return_exit_threshold", 0.0002)
        vol_exit_mult = params.get("vol_exit_mult", 2.0)

        exit_sig = compute_exit(
            df, pos,
            adx_window=adx_window,
            adx_exit=adx_exit,
            return_window=return_window,
            return_exit_threshold=return_exit_threshold,
            vol_exit_mult=vol_exit_mult,
        )
        pos[exit_sig & (pos != 0)] = 0
        n_overrides = int((exit_sig & (raw_pos != 0)).sum())
    else:
        n_overrides = 0

    result_df = df.copy()
    if "close" in result_df.columns:
        result_df["close"] = result_df["close"].astype(float)
    result_df["position"] = pos

    if enable_freeze:
        returns = result_df["close"].pct_change().fillna(0)
        strat_returns = pos * returns
        equity = (1 + strat_returns).cumprod().values
        frozen = apply_freeze_protection(equity, max_dd_allowed=-0.10)
        if frozen.any():
            pos_frozen = pos.copy()
            pos_frozen[frozen] = 0
            result_df["position"] = pos_frozen

    metrics = evaluate(result_df, timeframe=timeframe)
    metrics["n_exit_overrides"] = n_overrides

    return metrics
