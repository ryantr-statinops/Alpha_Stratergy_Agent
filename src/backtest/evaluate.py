"""Performance evaluation metrics."""
import numpy as np
import pandas as pd


N_BARS_PER_YEAR = {
    "5m":   78 * 252,    # 78 bars/session × 252 days
    "15m":  26 * 252,
    "30m":  13 * 252,
    "60m":  7  * 252,
    "1D":   252,
}


def evaluate(df, timeframe="1D", position_col="position"):
    """Compute full scorecard from strategy results DataFrame."""
    df = df.copy()
    if "strategy_returns" not in df.columns:
        df["returns"] = df["close"].pct_change().fillna(0)
        df["strategy_returns"] = df[position_col].shift(1).fillna(0) * df["returns"]
        df["equity"] = (1 + df["strategy_returns"]).cumprod()

    sr = df["strategy_returns"].values
    eq = df["equity"].values
    n = len(sr)
    npy = N_BARS_PER_YEAR.get(timeframe, 252)

    # --- Core metrics ---
    total_return = eq[-1] - 1 if n > 0 else 0
    years = max(n / npy, 1 / npy)
    cagr = (eq[-1] ** (1 / years) - 1) if eq[-1] > 0 else 0

    # Annualized metrics
    ann_mean = np.mean(sr) * npy
    ann_std = np.std(sr, ddof=1) * np.sqrt(npy)
    sharpe = ann_mean / ann_std if ann_std > 0 else 0

    # Sortino (downside deviation only)
    downside = sr[sr < 0]
    dd_std = np.std(downside, ddof=1) * np.sqrt(npy) if len(downside) > 1 else 1e-6
    sortino = ann_mean / dd_std if dd_std > 0 else 0

    # Max drawdown
    cummax = np.maximum.accumulate(eq)
    drawdown = (eq - cummax) / cummax
    max_dd = np.min(drawdown) if n > 0 else 0

    # Calmar
    calmar = cagr / abs(max_dd) if max_dd < 0 else 0

    # Profit Factor
    gains = sr[sr > 0].sum()
    losses = abs(sr[sr < 0].sum())
    profit_factor = gains / losses if losses > 0 else float("inf")

    # Win rate
    n_wins = np.sum(sr > 0)
    win_rate = n_wins / np.sum(sr != 0) if np.sum(sr != 0) > 0 else 0

    # Average trade return
    avg_trade = np.mean(sr[sr != 0]) if np.sum(sr != 0) > 0 else 0

    # Ulcer Index
    ulcer = np.sqrt(np.mean(drawdown ** 2)) if n > 0 else 0

    # VaR / CVaR (95%)
    var_95 = np.percentile(sr, 5) if n > 0 else 0
    cvar_95 = np.mean(sr[sr <= var_95]) if np.sum(sr <= var_95) > 0 else 0

    # Number of trades (position changes)
    pos_changes = np.sum(np.abs(np.diff(np.sign(df[position_col].values)))) if n > 1 else 0

    return {
        "total_return": total_return,
        "cagr": cagr,
        "sharpe": sharpe,
        "sortino": sortino,
        "max_dd": max_dd,
        "calmar": calmar,
        "profit_factor": profit_factor,
        "win_rate": win_rate,
        "avg_trade": avg_trade,
        "ulcer_index": ulcer,
        "var_95": var_95,
        "cvar_95": cvar_95,
        "n_trades": pos_changes,
        "n_bars": n,
    }
