# Thesis 22: Return Mean Drift

## Core Idea
Use `rolling_mean(returns(close), 20)` to measure the average return drift. When drift crosses a positive threshold, upward momentum is building (long). When drift crosses below a negative threshold, downward momentum is building (short).

## Templates

### T22-A — RetMean Cross
Entry when average return drift shifts direction.
- `ret_mean = rolling_mean(returns(close), 20)`
- **Long**: crossed_above_value(ret_mean, 0.001) — positive drift starting
- **Short**: crossed_below_value(ret_mean, -0.001) — negative drift starting
- **Exit**: ATR stop + trailing stop

### T22-B — RetMean + ADX
Same + ADX trend confirmation.
- Adds: adx_val > adx_entry

## Parameters
| Param | T22-A | T22-B |
|-------|-------|-------|
| ret_window | 20 | 20 |
| entry_threshold | 0.001 | 0.001 |
| adx_entry | — | 22 |
| atr_mult | 2.0 | 2.0 |

## Timeframes
15min, 30min
