# Time-Series Operations Syntax

Canonical location for `SeriesT` operations used through `self.op` in Round 2 `time_series` strategies. Data accessors come from the shared [`../data_syntax.md`](../data_syntax.md) catalog without `_panel` suffixes.

## Usage Contract

1. Call operations only through `self.op` inside `CustomStrategy.__algorithm__()`.
2. Inputs and outputs must be `SeriesT` unless a signature explicitly documents otherwise.
3. Time-dependent operations must be causal: negative shifts, centered windows, and backfill are forbidden.
4. Strategy logic uses bitwise `&`, `|`, and `~` for vectorized Boolean composition; `and_`/`or_`/`not_` exist for the same composition when an expression form is clearer.
5. Native arithmetic and comparison operators are preferred where supported: use `a - b` and `a / b`, not non-existent `div`/`sub`.
6. `fillna` must stay causal: fill with a constant or use `ffill` only.
7. Use `notna` to exclude unavailable fundamentals — treat them as unavailable, not zero.
8. Every operation documents signature, output, axis, missing behavior, causal constraints, and evidence status.

## Evidence Labels

| Label | Meaning |
|---|---|
| `CATALOG_ONLY` | Present in the authoritative API inventory; no runtime evidence yet |
| `EXAMPLE_VERIFIED` | Present in an approved strategy example |
| `VERIFY_PASSED` | XNOQuant verify accepted a strategy using it |
| `SIMULATE_PASSED` | Used in a completed XNOQuant simulation |
| `BEHAVIOR_VERIFIED` | Edge behavior and output semantics were checked |
| `PARTIAL_SIGNATURE` | Source signature is incomplete; do not generate strategy usage |

## Signature Convention

Every row represents `self.op.<signature>`. Where evidence is still pending, the row is marked `CATALOG_ONLY` until a runtime probe promotes it.

## Quick Lookup

| Group | Typical use | Representative functions |
|---|---|---|
| Crossover Detection | entry/exit on a level or series crossing | `crossed`, `crossed_above`, `crossed_below`, `crossed_above_value`, `crossed_below_value` |
| Shift & Change | lag, difference, and percentage change | `shift`, `diff`, `pct_change`, `previous`, `current` |
| State & Persistence | sustained conditions over bars | `rising`, `falling`, `bars_since`, `hold_for`, `consecutive_true` |
| Missing Data | test and fill unavailable values | `isna`, `notna`, `isfinite`, `fillna`, `ffill`, `zero_ifna`, `replace` |
| Value Transforms | reshape numeric or Boolean series | `abs`, `clip`, `sign`, `between`, `where`, `value_when` |
| Boolean Composition | combine conditions | `and_`, `or_`, `not_` |

## Crossover Detection

| Name | Returns | Syntax | Description |
|---|---|---|---|
| `crossed` | `SeriesT` | `self.op.crossed(series, level)` | True where `series` crosses `level` in either direction. |
| `crossed_above` | `SeriesT` | `self.op.crossed_above(a, b)` | True where `a` crosses above `b`. |
| `crossed_below` | `SeriesT` | `self.op.crossed_below(a, b)` | True where `a` crosses below `b`. |
| `crossed_above_value` | `SeriesT` | `self.op.crossed_above_value(series, value)` | True where `series` crosses above a scalar `value`. |
| `crossed_below_value` | `SeriesT` | `self.op.crossed_below_value(series, value)` | True where `series` crosses below a scalar `value`. |

## Shift & Change

| Name | Returns | Syntax | Description |
|---|---|---|---|
| `shift` | `SeriesT` | `self.op.shift(series, periods)` | Lag the series by `periods` bars. |
| `diff` | `SeriesT` | `self.op.diff(series, periods)` | Difference of `series` over `periods` bars. |
| `pct_change` | `SeriesT` | `self.op.pct_change(series, periods=1)` | Percentage change of `series` over `periods` bars. |
| `previous` | `SeriesT` | `self.op.previous(series, n)` | Value of `series` `n` bars ago. |
| `current` | `SeriesT` | `self.op.current(series)` | Current value of `series`. |

## State & Persistence

| Name | Returns | Syntax | Description |
|---|---|---|---|
| `rising` | `SeriesT` | `self.op.rising(series, periods)` | True where `series` is rising over `periods` bars. |
| `falling` | `SeriesT` | `self.op.falling(series, periods)` | True where `series` is falling over `periods` bars. |
| `bars_since` | `SeriesT` | `self.op.bars_since(cond)` | Bars elapsed since `cond` was last true. |
| `hold_for` | `SeriesT` | `self.op.hold_for(cond, periods)` | True while `cond` has held for at least `periods` bars. |
| `consecutive_true` | `SeriesT` | `self.op.consecutive_true(cond, periods=1)` | Count of consecutive bars where `cond` is true. |

## Missing Data

| Name | Returns | Syntax | Description |
|---|---|---|---|
| `isna` | `SeriesT` | `self.op.isna(series)` | True where `series` is missing. |
| `notna` | `SeriesT` | `self.op.notna(series)` | True where `series` is available. |
| `isfinite` | `SeriesT` | `self.op.isfinite(series)` | True where `series` is finite (not NaN/inf). |
| `fillna` | `SeriesT` | `self.op.fillna(series, value)` | Replace missing values with a constant `value`. |
| `ffill` | `SeriesT` | `self.op.ffill(series)` | Forward-fill missing values. |
| `zero_ifna` | `SeriesT` | `self.op.zero_ifna(series)` | Replace missing values with `0`. |
| `replace` | `SeriesT` | `self.op.replace(series, old, new)` | Replace occurrences of `old` with `new`. |

## Value Transforms

| Name | Returns | Syntax | Description |
|---|---|---|---|
| `abs` | `SeriesT` | `self.op.abs(series)` | Absolute value of `series`. |
| `clip` | `SeriesT` | `self.op.clip(series, lower, upper)` | Clip `series` into `[lower, upper]`. |
| `sign` | `SeriesT` | `self.op.sign(series)` | Sign of `series` (`-1`, `0`, `1`). |
| `between` | `SeriesT` | `self.op.between(series, lower, upper)` | True where `series` is within `[lower, upper]`. |
| `where` | `SeriesT` | `self.op.where(cond, a, b)` | `a` where `cond`, else `b`. |
| `value_when` | `SeriesT` | `self.op.value_when(cond, value)` | Scalar `value` where `cond`, else NaN. |

## Boolean Composition

| Name | Returns | Syntax | Description |
|---|---|---|---|
| `and_` | `SeriesT` | `self.op.and_(a, b)` | Element-wise logical AND. |
| `or_` | `SeriesT` | `self.op.or_(a, b)` | Element-wise logical OR. |
| `not_` | `SeriesT` | `self.op.not_(a)` | Element-wise logical NOT. |

## Not Available

The following names do **not** exist as `self.op` operations; use native operators instead:

- `self.op.div(...)` → `a / b`
- `self.op.sub(...)` → `a - b`
- `self.op.minimum(...)` → `min(a, b)` expression or native comparison

## Noise Filtering

Filtering is composed from the existing functions above; no separate `noise_*`
operator is required.

- Drop unavailable or non-finite bars: `notna`, `isfinite`, `isna`.
- Causal forward smoothing (price only, not fundamentals): `ffill`, `fillna(series, value)`.
- Require a signal to persist a single bar does not trade: `hold_for`, `consecutive_true`,
  `rising`, `falling`, `bars_since`.
- De-whipsaw a crossover with an edge: `crossed_above` / `crossed_below` combined with
  `rising` / `falling`.
- Add a dead-band (hysteresis) with native arithmetic: `close > slow * 1.02`, plus `abs`,
  `between`, `clip`.
- Keep it causal: forward-only fills, positive lookbacks, no centered windows.
- Never use `fillna` on a fundamental to hide a missing value as a zero; treat it as unavailable.

## Missing Behavior and Causal Constraints

| Operation | Required research check |
|---|---|
| `fillna`, `zero_ifna`, `ffill` | Never fill fundamental data with a default that changes its meaning; missing means unavailable, not zero. |
| `shift`, `previous`, `diff`, `pct_change` | Must use a positive lookback; negative shifts and backfill are forbidden. |
| `between`, `clip` | Bounds are inclusive; verify sign and orientation in research. |
| `replace` | Missing-value behavior must be verified before use. |

## Pending Evidence

Rows marked `CATALOG_ONLY` above are declared supported by the authoritative inventory but have not yet been promoted by a runtime probe. Do not generate undocumented `self.op` calls from this file. Existing strategy examples provide partial evidence but are not a substitute for the complete authoritative operation catalog.

## Related Documents

- Data fields: [`../data_syntax.md`](../data_syntax.md)
- Feature catalog: [`feature_syntax.md`](feature_syntax.md)
- Parameter profiles: [`parameters.md`](parameters.md)
- Construction patterns: [`strategy_patterns.md`](strategy_patterns.md)
