# Thesis 21: Momentum Decay

## Core Idea
Track the slope of the 20-bar rolling mean using `linearreg_slope`. When the slope starts decreasing (uptrend losing steam) or increasing (downtrend losing steam), it signals trend exhaustion and an impending reversal.

## Templates

### T21-A — Slope Decay
Entry when momentum slope crosses its own average — indicating deceleration.
- `mom_slope = linearreg_slope(rolling_mean(close, 20), 5)`
- `mom_slope_avg = rolling_mean(mom_slope, 5)`
- **Long**: mom_slope < 0 AND crossed_above(mom_slope, mom_slope_avg) — downtrend decaying
- **Short**: mom_slope > 0 AND crossed_below(mom_slope, mom_slope_avg) — uptrend decaying
- **Exit**: ATR stop + trailing stop

### T21-B — Decay + Volume
Same + volume confirmation.
- Adds: volume > vol_sma(20)

## Parameters
| Param | T21-A | T21-B |
|-------|-------|-------|
| ma_window | 20 | 20 |
| slope_window | 5 | 5 |
| smooth_window | 5 | 5 |
| vol_window | — | 20 |
| atr_mult | 2.0 | 2.0 |

## Timeframes
15min, 30min
