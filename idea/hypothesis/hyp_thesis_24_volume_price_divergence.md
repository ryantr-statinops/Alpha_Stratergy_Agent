# Thesis 24: Volume-Price Divergence

## Core Idea
On-Balance Volume (OBV) leads price. When OBV and price move in opposite directions, it signals an impending reversal. Bullish divergence = price down but OBV up (accumulation). Bearish divergence = price up but OBV down (distribution).

## Templates

### T24-A — OBV Divergence
Compare OBV slope vs price slope to detect divergence.
- `obv = obv(close, volume)`, `price_slope = linearreg_slope(close, 5)`, `obv_slope = linearreg_slope(obv, 5)`
- **Long**: price_slope < 0 AND obv_slope crossed above 0 (price falling but OBV turning up)
- **Short**: price_slope > 0 AND obv_slope crossed below 0 (price rising but OBV turning down)
- **Exit**: ATR stop + trailing stop

### T24-B — VPD + Volume
Same + volume > SMA(20) confirmation.

## Parameters
| Param | T24-A | T24-B |
|-------|-------|-------|
| slope_window | 5 | 5 |
| vol_window | — | 20 |
| atr_mult | 2.0 | 2.0 |

## Timeframes
15min, 30min
