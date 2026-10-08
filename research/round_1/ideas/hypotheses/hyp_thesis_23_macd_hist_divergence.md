# Thesis 23: MACD Histogram Divergence

## Core Idea
The MACD histogram slope (`linearreg_slope(macd_hist, 5)`) is a leading indicator of momentum shifts. When the histogram slope crosses zero, it signals a change in momentum direction before price confirms.

## Templates

### T23-A — Hist Slope
Entry when MACD histogram slope changes direction.
- `macd, signal, hist = macd(close, 12, 26, 9)`
- `hist_slope = linearreg_slope(hist, 5)`
- **Long**: crossed_above(hist_slope, 0) — histogram turning up, momentum building
- **Short**: crossed_below(hist_slope, 0) — histogram turning down, momentum fading
- **Exit**: ATR stop + trailing stop

### T23-B — Hist + Price Cross
Same + price relative to BB mid-band.
- **Long**: hist_slope cross above 0 AND close > bb_mid (price above mid-band)
- **Short**: hist_slope cross below 0 AND close < bb_mid (price below mid-band)

## Parameters
| Param | T23-A | T23-B |
|-------|-------|-------|
| macd_fast | 12 | 12 |
| macd_slow | 26 | 26 |
| macd_signal | 9 | 9 |
| slope_window | 5 | 5 |
| bb_window | — | 20 |
| atr_mult | 2.0 | 2.0 |

## Timeframes
15min, 30min, 60min
