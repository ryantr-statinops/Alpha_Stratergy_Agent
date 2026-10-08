# Thesis 28: BB Width Squeeze

## Core Idea
BB Width = (upper - lower) / mid. When BB width contracts to its 10th percentile (quantile 0.1) over 100 bars, the market is in a squeeze phase — low volatility before an explosive move. Trade the breakout direction.

## Templates

### T28-A — Squeeze Detection
Detect squeeze via historical quantile then trade breakout.
- `bb_width = (bb_upper - bb_lower) / bb_mid`
- `squeeze = bb_width < rolling_quantile(bb_width, 100, 0.1)`
- **Long**: squeeze AND crossed_above(close, bb_upper)
- **Short**: squeeze AND crossed_below(close, bb_lower)
- **Exit**: ATR stop + trailing stop

### T28-B — Squeeze + Volume
Same + volume > SMA(20) confirmation on breakout.

## Parameters
| Param | T28-A | T28-B |
|-------|-------|-------|
| bb_window | 20 | 20 |
| squeeze_q | 0.1 | 0.1 |
| quantile_window | 100 | 100 |
| vol_window | — | 20 |
| atr_mult | 2.0 | 2.0 |

## Timeframes
15min, 30min, 60min
