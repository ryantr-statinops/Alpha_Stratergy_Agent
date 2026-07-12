# Thesis 18: Range Rank Breakout

## Core Idea
Use `rolling_rank(close, 100)` to measure where current close sits in its 100-bar history (0–1 scale). Extreme rank values (< 0.05 or > 0.95) signal overextended prices — mean reversion or breakout continuation.

## Templates

### T18-A — Rank Only
Entry when price rank hits extreme quantile.
- **Long**: `rolling_rank(close, 100) < 0.05`
- **Short**: `rolling_rank(close, 100) > 0.95`
- **Exit**: ATR stop + trailing stop

### T18-B — Rank + Volume
Same + volume confirmation.
- **Long**: rank < 0.05 AND volume > vol_sma(20)
- **Short**: rank > 0.95 AND volume > vol_sma(20)

## Parameters
| Param | T18-A | T18-B |
|-------|-------|-------|
| rank_window | 100 | 100 |
| rank_entry | 0.05 | 0.05 |
| vol_window | — | 20 |
| atr_mult | 2.0 | 2.0 |

## Timeframes
15min, 30min
