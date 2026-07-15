## Operations Syntax Reference

Use this file as the canonical catalog for `self.op.*`.

## Section Index

| Group | Jump to |
|---|---|
| Cross / Event | [Cross and Event Primitives](#cross-and-event-primitives) |
| Lag / Time | [Lag and Time Primitives](#lag-and-time-primitives) |
| Range / Mask / Conditional | [Range, Mask, and Conditional Helpers](#range-mask-and-conditional-helpers) |
| Signal Persistence | [Signal Persistence](#signal-persistence) |
| Boolean Logic | [Boolean Logic](#boolean-logic) |

### Quick Lookup
| Group | Typical use | Representative functions |
|---|---|---|
| Cross / Event | detect signal transitions | `crossed`, `crossed_above`, `crossed_below`, `crossed_above_value`, `crossed_below_value` |
| Lag / Time | compare against past bars | `previous`, `shift`, `diff`, `pct_change`, `bars_since` |
| Missing Data | handle nulls safely | `fillna`, `ffill`, `zero_ifna`, `isna`, `notna`, `isfinite` |
| Range / Filter | constrain values | `between`, `clip`, `replace`, `sign` |
| Signal Persistence | keep or fetch prior events | `hold_for`, `value_when`, `current` |
| Boolean Logic | combine conditions | `and_`, `or_`, `not_`, `where` |
| Numeric Helpers | simple transforms | `abs` |

### Reading Tips
- Use the quick lookup to find the right primitive, then check the detailed signature.
- Prefer `previous`, `shift`, `pct_change`, `bars_since`, and `hold_for` for causal logic.
- Keep `fillna` causal by using a constant or forward-fill only.

### Cross and Event Primitives

| Name | Returns | Syntax | Description |
|---|---|---|---|
| `crossed` | `SeriesT` | `self.op.crossed(series1: SeriesT, series2: SeriesT)` | Detect when two series cross each other (either direction). Returns True when series1 crosses series2. |
| `crossed_above` | `SeriesT` | `self.op.crossed_above(series1: SeriesT, series2: SeriesT)` | Detect when series1 crosses above series2. Returns True at the crossover point. |
| `crossed_below` | `SeriesT` | `self.op.crossed_below(series1: SeriesT, series2: SeriesT)` | Detect when series1 crosses below series2. Returns True at the crossover point. |
| `current` | `SeriesT` | `self.op.current(series: SeriesT)` | Get the current value of a series. Used for clarity when comparing current vs previous values. |

### Lag and Time Primitives

| Name | Returns | Syntax | Description |
|---|---|---|---|
| `previous` | `SeriesT` | `self.op.previous(series: SeriesT, periods: int = 1)` | Get the previous value of a series. Shifts the series back by the specified number of periods. |
| `shift` | `SeriesT` | `self.op.shift(series: SeriesT, periods: int = 1)` | Shift series backward by positive periods only. `periods <= 0` is rejected for causal safety. |
| `diff` | `SeriesT` | `self.op.diff(series: SeriesT, periods: int = 1)` | Difference between current and lagged values. Past-looking only, so `periods > 0` is required. |
| `pct_change` | `SeriesT` | `self.op.pct_change(series: SeriesT, periods: int = 1)` | Percent change from lagged values: `(current / previous) - 1`. Requires `periods > 0`. |
| `rising` | `SeriesT` | `self.op.rising(series: SeriesT, periods: int = 1)` | Return True when the current value is greater than the value `periods` bars ago. Equivalent to `series > self.op.previous(series, periods)`. Example: `self.op.rising(close, 3)`. Causal note: this compares only current and past values; it does not require every bar in between to rise. |
| `falling` | `SeriesT` | `self.op.falling(series: SeriesT, periods: int = 1)` | Return True when the current value is less than the value `periods` bars ago. Equivalent to `series < self.op.previous(series, periods)`. Example: `self.op.falling(close, 3)`. Causal note: this compares only current and past values; it does not require every bar in between to fall. |
| `fillna` | `SeriesT` | `self.op.fillna(series: SeriesT, value: float \| None = None, method: str \| None = None)` | Fill NA values with a constant (`value`) or forward-fill (`method='ffill'`). Backfill is rejected. |
| `ffill` | `SeriesT` | `self.op.ffill(series: SeriesT)` | Forward-fill missing values using only past observations. |
| `abs` | `SeriesT` | `self.op.abs(series: SeriesT)` | Absolute value transform. |
| `clip` | `SeriesT` | `self.op.clip(series: SeriesT, lower: float \| None = None, upper: float \| None = None)` | Clip series values to lower/upper bounds. |
| `isna` | `SeriesT` | `self.op.isna(series: SeriesT)` | Element-wise NA/null check. |
| `notna` | `SeriesT` | `self.op.notna(series: SeriesT)` | Element-wise not-NA check. |
| `isfinite` | `SeriesT` | `self.op.isfinite(series: SeriesT)` | Element-wise finite-number check (rejects inf/-inf and NaN). |
| `zero_ifna` | `SeriesT` | `self.op.zero_ifna(series: SeriesT)` | Convenience helper: replace NA values with 0. |

### Range, Mask, and Conditional Helpers

| Name | Returns | Syntax | Description |
|---|---|---|---|
| `sign` | `SeriesT` | `self.op.sign(series: SeriesT)` | Element-wise sign function returning -1, 0, or 1 (NaN remains NaN). |
| `replace` | `SeriesT` | `self.op.replace(series: SeriesT, to_replace: float \| int \| None, value: float \| int \| None)` | Safely replace exact values. Backfill-like method replacement is intentionally unsupported. |
| `between` | `SeriesT` | `self.op.between(series: SeriesT, lower: SeriesOrFloatT, upper: SeriesOrFloatT)` | Inclusive range check. Equivalent to `(series >= lower) & (series <= upper)`. Example: `self.op.between(rsi, 30, 70)`. Causal note: this is pointwise and does not read future rows. |
| `where` | `SeriesT` | `self.op.where(condition: SeriesT, x: SeriesOrFloatT, y: SeriesOrFloatT)` | Element-wise conditional selection. Returns `x` where condition is True, else `y`. |

### Signal Persistence

| Name | Returns | Syntax | Description |
|---|---|---|---|
| `value_when` | `SeriesT` | `self.op.value_when(condition: SeriesT, values: SeriesT, occurrence: int = 0)` | For each row, return the value at the latest prior True condition (`occurrence=0`), or earlier occurrences. |
| `bars_since` | `SeriesT` | `self.op.bars_since(condition: SeriesT)` | Count bars since the latest True condition. Returns 0 on bars where condition is True, 1 on the next bar, and NaN before the condition has ever been True. Example: `self.op.bars_since(entry_signal)`. Equivalent to a causal running count reset by the latest True row. NaN conditions are treated as False. Causal note: each row only uses conditions at or before that row. |
| `hold_for` | `SeriesT` | `self.op.hold_for(condition: SeriesT, periods: int)` | Keep a signal True for a trailing window after it fires. Equivalent to `bars_since(condition) < periods`. Example: `self.op.hold_for(entry_signal, 5)` is True on the entry bar and the next 4 bars. Causal note: this only looks backward from the current row. |
| `crossed_above_value` | `SeriesT` | `self.op.crossed_above_value(series: SeriesT, value: float)` | Detect when a series crosses above a constant threshold. Equivalent to crossing above a constant series with the same threshold value. Example: `self.op.crossed_above_value(rsi, 50)`. Causal note: uses only current and previous values. |
| `crossed_below_value` | `SeriesT` | `self.op.crossed_below_value(series: SeriesT, value: float)` | Detect when a series crosses below a constant threshold. Equivalent to crossing below a constant series with the same threshold value. Example: `self.op.crossed_below_value(rsi, 30)`. Causal note: uses only current and previous values. |

### Boolean Logic

| Name | Returns | Syntax | Description |
|---|---|---|---|
| `and_` | `SeriesT` | `self.op.and_(*conditions: SeriesT)` | Logical AND operation. Combines multiple boolean conditions with element-wise AND. All conditions must be True. |
| `or_` | `SeriesT` | `self.op.or_(*conditions: SeriesT)` | Logical OR operation. Combines multiple boolean conditions with element-wise OR. At least one condition must be True. |
| `not_` | `SeriesT` | `self.op.not_(series: SeriesT)` | Logical NOT operation. Inverts a boolean series. True becomes False and vice vers |

### Tutorial
Use the operators above to assemble a causal signal pipeline: lag first, then filter, then combine, then size positions.
