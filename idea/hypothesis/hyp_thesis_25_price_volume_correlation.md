# Thesis 25: Price-Volume Correlation

## Core Idea
Rolling correlation between price and volume measures whether they move together or diverge. Strong negative correlation (< -0.5) signals accumulation (price down, volume up) or distribution (price up, volume down). Trade the implied reversal.

## Templates

### T25-A — Correlation Filter
Entry when price-volume correlation crosses extreme negative threshold.
- **Long**: rolling_correlation(close, volume, 20) < -0.5 AND close < bb_mid (accumulation at low price)
- **Short**: rolling_correlation(close, volume, 20) < -0.5 AND close > bb_mid (distribution at high price)
- **Exit**: ATR stop + trailing stop

### T25-B — Correlation + Regime
Same + ADX regime filter (only trade when ADX > threshold to avoid whipsaw).

## Parameters
| Param | T25-A | T25-B |
|-------|-------|-------|
| corr_window | 20 | 20 |
| corr_entry | -0.5 | -0.5 |
| adx_entry | — | 18 |
| atr_mult | 2.0 | 2.0 |

## Timeframes
15min, 30min, 60min
