# Panel Feature Contract

This document defines the evidence and usage contract for Round 2 `PanelT` features. `feature_syntax.md` remains the canonical name catalog; this file explains what must be known before a panel feature is used in a research claim.

## 1. Why This Contract Exists

A catalog entry proves that a feature name is documented. It does **not** by itself prove:

- which lookback window is used;
- whether a window argument is accepted;
- how warm-up rows are represented;
- how missing values propagate;
- whether a denominator is safely handled;
- whether the exact call has passed verify and simulate;
- whether backend defaults are stable across versions.

Unknown behavior must not be replaced with an invented assumption.

## 2. Evidence Status

Every panel call used by a canonical template should carry one of these evidence states in its supporting research document:

| Status | Meaning |
|---|---|
| `CATALOG_ONLY` | Name/signature appears in `feature_syntax.md`; runtime behavior is not verified |
| `EXAMPLE_VERIFIED` | Call appears in an official Round 2 example |
| `VERIFY_PASSED` | XNOQuant syntax verification accepted the exact call |
| `SIMULATE_PASSED` | Exact call produced a completed simulation |
| `BEHAVIOR_VERIFIED` | Window, warm-up, missing, and output behavior were inspected |

`SIMULATE_PASSED` does not imply economic robustness. `BEHAVIOR_VERIFIED` does not imply OOS performance.

## 3. Parameter and Default Rules

`feature_syntax.md` currently documents many panel signatures without explicit `window=` or `timeperiod=` arguments, for example:

```python
ema = self.feat.ema_panel(close)
mean = self.feat.rolling_mean_panel(signal)
value = self.feat.rolling_value_panel(close, volume)
```

Until the runtime signature is verified:

1. Do not add an undocumented parameter.
2. Do not state a numeric horizon for the feature.
3. Do not call the default a canonical parameter.
4. Record the dependency as `default_window_dependency: true`.
5. Do not claim parameter-neighbourhood robustness for that window.
6. If backend behavior changes, invalidate comparisons that depend on the old default.

If an explicit parameter is verified, record the exact accepted call and update both `feature_syntax.md` and this contract.

## 4. Feature Contract Table

The table below reflects the current documentation, not inferred runtime defaults.

| Family | Features | Documented explicit window | Required verification |
|---|---|:---:|---|
| Moving average | `sma_panel`, `ema_panel` | No | period, seed/warm-up, missing propagation |
| Rolling statistics | `rolling_mean_panel`, `rolling_std_panel`, `rolling_sum_panel`, `rolling_min_panel`, `rolling_max_panel` | No | window, min observations, missing propagation |
| Rolling rank | `rolling_rank_panel`, `rolling_percentile_rank_panel` | No | window, tie handling, percentile range |
| Rolling relation | `rolling_correlation_panel`, `rolling_covariance_panel` | No | window, missing pairs, zero variance |
| Volatility | `atr_panel`, `natr_panel`, `volume_z_panel` | No | period, warm-up, zero-price handling |
| Traded value | `rolling_value_panel` | No | formula, window, missing/zero volume |
| Returns | `returns_panel`, `log_returns_panel`, `delta_panel` | No | lag/period, non-positive price behavior |
| Safe ratio | `safe_divide_panel` | N/A | zero/negative/missing denominator output |
| Price transform | `hlc3_panel`, `typprice_panel`, `medprice_panel`, `wclprice_panel`, `ohlc4_panel` | N/A | missing component behavior |
| Volume/flow | `vwap_panel`, `rolling_vwap_panel`, `amihud_illiquidity_panel`, `cmf_panel` | No/unknown | formula, window, zero volume, warm-up |
| Momentum | `rsi_panel`, `macd_panel` | No | periods, output selector, warm-up |
| Bands/breakout | `bbands_panel`, `donchian_upper_panel`, `donchian_lower_panel` | No | period, band parameters, current-bar inclusion |
| Bar geometry | `close_location_panel`, `range_pct_panel` | N/A | zero-range handling |

## 5. Shape Contract

All documented panel features:

- accept one or more `PanelT` inputs;
- return a `PanelT` unless explicitly documented otherwise;
- preserve the time index and symbol columns;
- must not be mixed with SeriesT input;
- must not be passed to `self.set_positions`.

Valid:

```python
close = self.data.pv_close_panel
trend = self.feat.ema_panel(close)
rank = self.op.rank_cs_panel(trend)
```

Invalid:

```python
close = self.data.pv_close
trend = self.feat.ema_panel(close)
```

## 6. Missing and Warm-Up Behavior

For each feature used in a promoted strategy, research notes must answer:

- What is emitted before enough history exists?
- Does one missing input invalidate only that symbol/date or a wider window?
- Does the feature resume after missing data?
- Can zero variance, zero range, or zero volume create an invalid value?
- Does the portfolio mask exclude invalid output before ranking/weighting?

Do not convert warm-up or missing output to zero merely to increase coverage. Zero may be an economically meaningful signal and is not equivalent to unavailable.

## 7. Safe Division

Canonical call:

```python
ratio = self.feat.safe_divide_panel(numerator, denominator)
```

The strategy must still provide an economic denominator guard:

```python
eligible = denominator > 0
```

`safe_divide_panel` protects computation; it does not decide whether a negative denominator is economically comparable. For sign-unrestricted denominators, the idea document must define the intended semantics.

Before relying on the output, verify what the runtime emits for:

- denominator equal to zero;
- denominator missing;
- numerator missing;
- negative denominator;
- infinite or extreme result.

## 8. Current-Bar and Look-Ahead Rules

All features must be causal. For rolling highs/lows and breakout features, determine whether the current bar is included.

This distinction changes the condition:

```python
close > self.feat.donchian_upper_panel(high)
```

If the upper band includes the current high, a close-above-band condition may be impossible or have different meaning. Do not infer exclusion of the current bar from the feature name.

Negative shifts, centered windows, backward fill, and future observations are prohibited regardless of feature behavior.

## 9. Multi-Output Features

The documented panel MACD form selects one output:

```python
macd = self.feat.macd_panel(close, output="macd")
```

Only documented output selectors may be used. Do not assume the time-series tuple contract applies to PanelT. Verify each selector separately before using `signal` or `histogram` outputs.

The same rule applies to `bbands_panel(output=...)`.

## 10. Verification Record Template

Add a record to the supporting idea or audit document:

```yaml
feature: ema_panel
call: self.feat.ema_panel(close)
evidence_status: SIMULATE_PASSED
default_window_dependency: true
window: unknown
warmup: unknown
missing_behavior: unknown
verified_on: YYYY-MM-DD
example_or_strategy: path/to/file.py
notes: Do not label the horizon until behavior is verified.
```

For fully verified behavior:

```yaml
feature: safe_divide_panel
call: self.feat.safe_divide_panel(numerator, denominator)
evidence_status: BEHAVIOR_VERIFIED
zero_denominator: <observed behavior>
missing_denominator: <observed behavior>
negative_denominator: computationally accepted; economically masked
verified_on: YYYY-MM-DD
```

## 11. Promotion Rules

A strategy may be simulated with `CATALOG_ONLY` features for exploration, but it must not become a canonical baseline until:

- the exact call reaches at least `SIMULATE_PASSED`;
- unknown defaults are disclosed;
- mask behavior protects invalid output;
- the economic horizon is not falsely described;
- any output selector is documented;
- the strategy passes strict framework validation.

A strategy cannot claim parameter robustness for a hidden default. It can only claim robustness of dimensions that were explicitly and validly varied.

## 12. Known Documentation Gaps

The following must be resolved through official documentation, runtime introspection, or controlled verification:

1. Numeric defaults for panel moving and rolling features.
2. Whether panel functions accept explicit period/window arguments.
3. Minimum observations and warm-up output.
4. Missing-value propagation.
5. Current-bar inclusion for Donchian/breakout features.
6. Exact formulas for Amihud, CMF, rolling value, and VWAP.
7. Valid output selectors for MACD and Bollinger Bands.
8. Panel-compatible availability/not-null operation.

Until resolved, these are limitations of the research claim, not invitations to guess.

## 13. Checklist

- [ ] Input and output are PanelT.
- [ ] Function name exists in `feature_syntax.md`.
- [ ] Exact call has an evidence status.
- [ ] No undocumented argument is used.
- [ ] Hidden defaults are disclosed.
- [ ] Warm-up and missing risk are considered.
- [ ] Zero denominator/range/volume is guarded where applicable.
- [ ] Current-bar semantics are known for breakout logic.
- [ ] Panel multi-output semantics are not copied from time-series assumptions.
- [ ] The output is masked before cross-sectional ranking when invalid values are possible.
