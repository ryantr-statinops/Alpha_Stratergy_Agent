# Thesis 26: CMF Quantile Threshold

## Core Idea
Chaikin Money Flow (CMF) measures buying/selling pressure. Instead of using a fixed threshold (CMF > 0), use rolling_rank to identify historically extreme CMF values. CMF rank > 0.9 = exceptional buying pressure. CMF rank < 0.1 = exceptional selling pressure.

## Templates

### T26-A — CMF Rank
Entry when CMF rank reaches extreme levels.
- `cmf_rank = rolling_rank(cmf(high, low, close, volume, 20), 100)`
- **Long**: cmf_rank > 0.9 (historically strong buying)
- **Short**: cmf_rank < 0.1 (historically strong selling)
- **Exit**: ATR stop + trailing stop

### T26-B — CMF + RSI
Same + RSI directional filter.
- **Long**: cmf_rank > 0.9 AND rsi > 50
- **Short**: cmf_rank < 0.1 AND rsi < 50

## Parameters
| Param | T26-A | T26-B |
|-------|-------|-------|
| cmf_window | 20 | 20 |
| rank_window | 100 | 100 |
| entry_q | 0.9 | 0.9 |
| atr_mult | 2.0 | 2.0 |

## Timeframes
15min, 30min
