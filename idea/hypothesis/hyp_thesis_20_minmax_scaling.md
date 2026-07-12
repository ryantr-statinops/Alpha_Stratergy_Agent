# Thesis 20: MinMax Scaling

## Core Idea
Normalize close price to [0, 1] range using `rolling_min(close, 200)` and `rolling_max(close, 200)`. Trade when price hits multi-session extremes — near 200-bar low or high.

## Templates

### T20-A — MinMax Entry
Entry at multi-session extremes.
- **Long**: `pos < 0.05` (near 200-bar low)
- **Short**: `pos > 0.95` (near 200-bar high)
- **Exit**: ATR stop + trailing stop

### T20-B — MinMax + Trend
Same + EMA trend filter.
- **Long**: pos < 0.05 AND ema_fast > ema_slow
- **Short**: pos > 0.95 AND ema_fast < ema_slow

## Parameters
| Param | T20-A | T20-B |
|-------|-------|-------|
| lookback | 200 | 200 |
| pos_entry | 0.05 | 0.05 |
| ema_fast | — | 20 |
| ema_slow | — | 50 |
| atr_mult | 2.0 | 2.0 |

## Timeframes
15min, 30min, 60min
