# Thesis 14: BB Squeeze Reversal

## Core Idea

Trade Bollinger Band over-extensions as reversal opportunities. Price touching the outer band signals exhaustion — the move has gone too far, too fast. Combine with volume confirmation to filter low-conviction touches.

---

## Templates

### T14-A — TrendFilter Gate
Add SMA 200 trend filter to avoid counter-trend reversals.
- **Long**: `close > bb_upper` + `volume > vol_sma` + `close > sma(200)`
- **Short**: `close < bb_lower` + `volume > vol_sma` + `close < sma(200)`
- **Exit**: ATR stop + trailing stop (same as original)

### T14-B — Squeeze Detection
Measure BB width contraction as a squeeze phase — only enter when a squeeze is detected.
- **Long**: `close > bb_upper` + `volume > vol_sma` + `bb_width < sma(bb_width, 20)`
- **Short**: `close < bb_lower` + `volume > vol_sma` + `bb_width < sma(bb_width, 20)`
- **Exit**: ATR stop + trailing stop (same as original)

### T14-C — TimeStop
Add time-based exit: if position hasn't worked after `max_hold` bars, exit.
- **Entry**: Same as original (`close > bb_upper` + `volume > vol_sma` / `close < bb_lower` + `volume > vol_sma`)
- **Exit**: ATR stop + trailing stop + `bars_since > max_hold`

---

## Parameters

| Param | T14-A | T14-B | T14-C |
|-------|-------|-------|-------|
| bb_window | 20 | 20 | 20 |
| bb_nbdev | 2 | 2 | 2 |
| atr_mult | 2.0 | 2.0 | 2.0 |
| vol_window | 20 | 20 | 20 |
| trend_window | 200 | — | — |
| squeeze_window | — | 20 | — |
| max_hold | — | — | 15 |

## Timeframes

15min, 30min, 60min
