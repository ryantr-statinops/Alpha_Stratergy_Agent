# Thesis 19: BB Relative Position

## Core Idea
Calculate price's relative position inside Bollinger Bands: `(close - bb_lower) / (bb_upper - bb_lower)`. Value 0 = lower band, 1 = upper band. Trade when price reaches band extremes.

## Templates

### T19-A — BB Distance
Entry at band extremes.
- **Long**: `bb_pos < 0.05` (price at lower band)
- **Short**: `bb_pos > 0.95` (price at upper band)
- **Exit**: ATR stop + trailing stop

### T19-B — BB + ADX
Same + ADX trend confirmation.
- **Long**: bb_pos < 0.05 AND adx_val > adx_entry
- **Short**: bb_pos > 0.95 AND adx_val > adx_entry

### T19-C — BB + Volume
Same + volume confirmation.
- **Long**: bb_pos < 0.05 AND volume > vol_sma(20)
- **Short**: bb_pos > 0.95 AND volume > vol_sma(20)

## Parameters
| Param | T19-A | T19-B | T19-C |
|-------|-------|-------|-------|
| bb_window | 20 | 20 | 20 |
| bb_nbdev | 2 | 2 | 2 |
| bb_entry | 0.05 | 0.05 | 0.05 |
| adx_entry | — | 22 | — |
| vol_window | — | — | 20 |
| atr_mult | 2.0 | 2.0 | 2.0 |

## Timeframes
15min, 30min, 60min
