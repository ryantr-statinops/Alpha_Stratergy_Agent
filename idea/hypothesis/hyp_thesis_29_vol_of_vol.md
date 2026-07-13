# Thesis 29: Vol-of-Vol (ATR Variance)

## Core Idea
Rolling standard deviation of ATR (vol-of-vol) measures the stability of market volatility. Low vol-of-vol = stable regime suitable for mean reversion. High vol-of-vol = chaotic regime — trade with trend or skip.

## Templates

### T29-A — Low Vol Regime
Trade BB reversal only when vol-of-vol is below its 50-bar mean (stable regime).
- `vov = rolling_std(atr(14), 20)`, `vov_ma = rolling_mean(vov, 50)`
- Only trade when vov < vov_ma (low vol-of-vol = stable)
- **Long**: stable AND close < bb_lower
- **Short**: stable AND close > bb_upper
- **Exit**: ATR stop + trailing stop

### T29-B — Stable + Volume
Same stable regime filter + volume > SMA(20) confirmation.

## Parameters
| Param | T29-A | T29-B |
|-------|-------|-------|
| atr_window | 14 | 14 |
| vov_window | 20 | 20 |
| vov_ma_window | 50 | 50 |
| vol_window | — | 20 |
| atr_mult | 2.0 | 2.0 |

## Timeframes
15min, 30min
