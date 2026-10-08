# Thesis 27: Log-Return Volatility Filter

## Core Idea
Use rolling standard deviation of log-returns to measure market activity. When vol is too low, market is flat and prone to whipsaw — skip trading. Only trade when vol is above a threshold (e.g., 30th percentile of its 100-bar history).

## Templates

### T27-A — Vol Gate Filter
Use log-ret vol as a market filter. Entry uses BB position.
- `vol = rolling_std(log_returns(close, 1), 20)`
- `vol_threshold = rolling_quantile(vol, 100, q=0.3)`
- Only trade when vol > vol_threshold (enough market activity)
- **Long**: vol > threshold AND close < bb_lower (at lower band)
- **Short**: vol > threshold AND close > bb_upper (at upper band)
- **Exit**: ATR stop + trailing stop

### T27-B — Vol Gate + Volume
Same vol gate + volume > SMA(20) confirmation.

## Parameters
| Param | T27-A | T27-B |
|-------|-------|-------|
| vol_window | 20 | 20 |
| vol_q | 0.3 | 0.3 |
| quantile_window | 100 | 100 |
| bb_window | 20 | 20 |
| atr_mult | 2.0 | 2.0 |

## Timeframes
15min, 30min
