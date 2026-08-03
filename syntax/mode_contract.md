# Round 2 Mode Contract

This document is the canonical contract separating the two XNOQuant Round 2 execution modes. A strategy must select exactly one mode and keep its data, features, operators, and position API in that mode from end to end.

## 1. Contract Summary

| Contract | `time_series` | `cross_sectional` |
|---|---|---|
| Research question | When should each symbol be held? | How should capital be allocated across symbols? |
| Data shape | One series per field per symbol | Panel with time on rows and symbols on columns |
| Data fields | No suffix, e.g. `pv_close` | `_panel`, e.g. `pv_close_panel` |
| Feature family | Suffix-less, e.g. `ema` | `_panel`, e.g. `ema_panel` |
| Main operators | Suffix-less causal operators | Cross-sectional `_cs_panel` operators |
| Position API | `self.set_positions` | `self.set_portfolio_positions` |
| Exposure | Long-only, `[0, +1]` | Market-neutral long/short weights |

The exact mode names are `time_series` and `cross_sectional`. `timeseries` is invalid.

## 2. Shape Invariants

### 2.1 Time series

A suffix-less field is evaluated independently for the current symbol. Every intermediate expression must remain a single-symbol time series or a boolean time series.

```python
close = self.data.pv_close
ema24 = self.feat.ema(close, timeperiod=24)
long_setup = close > ema24
self.set_positions(long_setup, position=1)
```

### 2.2 Cross sectional

A panel has time on rows and symbols on columns. Panel features preserve that shape; cross-sectional operators compare eligible symbols independently at each timestamp.

```python
close = self.data.pv_close_panel
signal = self.feat.returns_panel(close)
weights = self.op.portfolio_weights_panel(
    signal,
    method="rank_demean_l1",
)
self.set_portfolio_positions(weights)
```

A one-symbol universe is still represented as a panel in `cross_sectional` mode.

## 3. Valid API Families

### 3.1 Time-series family

```text
self.data.<field>
    -> self.feat.<feature>(..., explicit parameters)
    -> self.op.<causal_operator>(...)
    -> self.set_positions(condition, position)
```

Rules:

- Data fields do not end in `_panel`.
- Features do not end in `_panel`.
- Positions are restricted to `0`, `0.5`, and `1` unless another long-only size is explicitly approved.
- Calls are ordered Exit -> Weak Long -> Strong Long.
- Negative positions are invalid.

### 3.2 Cross-sectional family

```text
self.data.<field>_panel
    -> self.feat.<feature>_panel(...)
    -> self.op.<normalizer>_cs_panel(...)
    -> self.op.portfolio_weights_panel(...)
    -> self.set_portfolio_positions(weights)
```

Rules:

- Every raw field ends in `_panel`.
- Transform features use their documented `_panel` form.
- Cross-sectional normalization uses the documented `_cs_panel` operators.
- Portfolio weights are constructed by `portfolio_weights_panel` unless an official example documents another method.
- Symbols outside the eligibility mask receive zero weight.
- Preferred default construction is `method="rank_demean_l1"`: approximately zero net exposure and unit gross exposure.

## 4. Missing-Data Contract

Missing fundamental data means **unavailable**, not zero.

### Time series

Use the documented suffix-less availability operator:

```python
known = self.op.notna(net_profit) & self.op.notna(total_assets)
eligible = known & (total_assets > 0)
```

Do not use `fillna(..., value=0)` to make a company fundamentally eligible.

### Cross sectional

Do not assume that a suffix-less SeriesT operator accepts PanelT. Construct eligibility only with PanelT-compatible expressions that have been verified by the platform or an official example.

Until a canonical PanelT `notna` call is documented, positive-denominator and economically valid level guards may be used only when they also exclude missing values under verified platform semantics:

```python
eligible = (
    (close > 0)
    & (volume > 0)
    & (numerator > 0)
    & (denominator > 0)
)
```

This pattern is not a universal substitute for missing checks: it is valid only when positivity is part of the economic thesis. See `panel_feature_contract.md` and `fundamental_data_contract.md` before using nullable or sign-unrestricted fields.

## 5. Position Contracts

### 5.1 Time series

```python
self.set_positions(exit_setup, position=0)
self.set_positions(weak_long, position=0.5)
self.set_positions(strong_long, position=1)
```

Later calls override earlier calls when conditions overlap. Entry and exit should therefore normally be mutually exclusive by construction.

### 5.2 Cross sectional

```python
weights = self.op.portfolio_weights_panel(
    signal,
    method="rank_demean_l1",
    mask=eligible,
)
self.set_portfolio_positions(weights)
```

A cross-sectional signal is not a position. It must be converted to a normalized portfolio. Raw factor magnitudes must not be sent directly to the position API.

## 6. Invalid Mixing Patterns

### Panel data with a time-series feature

```python
# INVALID
close = self.data.pv_close_panel
ema = self.feat.ema(close, timeperiod=24)
```

### Series data with a panel feature

```python
# INVALID
close = self.data.pv_close
ema = self.feat.ema_panel(close)
```

### Panel data with the time-series position API

```python
# INVALID
close = self.data.pv_close_panel
self.set_positions(close > 0, position=1)
```

### Series data with the portfolio position API

```python
# INVALID
close = self.data.pv_close
self.set_portfolio_positions(close)
```

### Series-only availability helper applied to PanelT

```python
# INVALID unless the PanelT behavior is explicitly documented and verified
known = self.op.notna(self.data.fun_is_eps_basis_quarterly_panel)
```

### Mixed fundamental frequency is allowed; mixed shape is not

Quarterly and annual fields may appear in one strategy if the economic thesis explains the mixed horizons and all fields share the same mode. This is valid:

```python
quarterly_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly_panel
annual_assets = self.data.fun_bs_total_assets_annual_panel
```

It still requires point-in-time alignment, denominator guards, and a stale-data rationale.

## 7. Mode Selection Guide

Choose `time_series` when:

- the signal asks whether a symbol is in a valid holding regime;
- long-only exposure is appropriate;
- persistent quality and trend determine entry/exit;
- symbol-level timing matters more than relative ranking.

Choose `cross_sectional` when:

- the signal compares companies at the same timestamp;
- factor ranks or normalized scores have economic meaning;
- a market-neutral portfolio is required;
- eligibility, coverage, and concentration can be audited.

Do not select a mode merely because one produces a better backtest. The mode must follow from the hypothesis before testing.

## 8. Validation Checklist

- [ ] Exactly one mode is declared.
- [ ] Every data field has the correct suffix for that mode.
- [ ] Every feature belongs to the selected mode family.
- [ ] Every operator accepts the actual intermediate shape.
- [ ] The position API matches the mode.
- [ ] Time-series positions remain within `[0, +1]`.
- [ ] Cross-sectional weights are normalized and market-neutral.
- [ ] Missing fundamentals are unavailable, not zero.
- [ ] No SeriesT helper is assumed to support PanelT without evidence.
- [ ] Quarterly/annual horizon mixing is economically justified.
- [ ] The strategy passes `python tools/validate_framework.py --strict`.

## 9. Canonical References

- Raw fields: `syntax/data_syntax.md`
- Features: `syntax/feature_syntax.md`
- Operators: `syntax/operations_syntax.md`
- Fundamental semantics: `syntax/fundamental_data_contract.md`
- Panel defaults and verified behavior: `syntax/panel_feature_contract.md`
- Construction recipes: `syntax/strategy_patterns.md`
- Research validation: `syntax/validation_protocol.md`
