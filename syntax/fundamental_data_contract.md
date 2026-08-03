# Fundamental Data Contract

This document defines how Round 2 fundamental fields may be interpreted and combined. `data_syntax.md` remains the canonical field-name catalog. A field existing in the catalog does not guarantee that it is comparable across industries or suitable for a given alpha.

## 1. Core Principles

1. Fundamentals are point-in-time and become available only on publication date.
2. Never shift fundamentals backward or backfill them.
3. Forward-filled values are stale states, not new daily observations.
4. Missing means unavailable, not zero.
5. Compare companies of different size using economically meaningful ratios.
6. Require a valid, normally positive denominator before forming a ratio.
7. Separate persistent states from report events.
8. Do not compare incompatible accounting populations without a valid sector/accounting mask.
9. An eligibility mask can itself create a hidden factor and must be audited.

## 2. Frequencies and Availability

| Suffix | Meaning | Typical use |
|---|---|---|
| `_quarterly` / `_quarterly_panel` | Quarterly report observation | Timelier profitability, change, and event signals |
| `_annual` / `_annual_panel` | Annual report observation | Stable balance-sheet, cash-flow, and quality states |

Quarterly and annual fields may be combined only when the thesis explains the different horizons. Their publication dates, missingness, and staleness remain independent.

## 3. Signal-Type Taxonomy

| Signal type | Definition | Intended persistence |
|---|---|---|
| Level | Signed state such as positive profit or CFO | Until a newer report |
| Ratio | Scale-adjusted state such as profit/assets | Until a newer report |
| Change | Difference from the previous published observation | Report event |
| Growth | Change scaled by a valid economic base | Report event or explicitly decayed overlay |
| Quality | Relation between accounting quantities, e.g. CFO/profit | Persistent with stale-data caveat |
| Risk state | Leverage, liquidity, reserve, or capital condition | Persistent with industry caveat |

A report change is not a daily growth series. On a forward-filled daily timeline it changes primarily when a new report arrives.

## 4. Point-in-Time Rules

Valid research assumes XNOQuant aligns reports to publication date. Strategy code must not attempt to reconstruct an earlier availability date.

Prohibited:

- negative shifts;
- backward fill;
- centered rolling windows;
- using quarter-end as if the report were known then;
- treating revised values as historically known without evidence;
- filling unavailable fundamentals with zero to increase coverage.

The idea document must state whether the signal is a persistent state or a report event and how stale values are expected to behave.

## 5. Missing-Data Rules

### Time series

```python
known = self.op.notna(numerator) & self.op.notna(denominator)
eligible = known & (denominator > 0)
```

### Cross sectional

Use only a PanelT-compatible availability pattern verified by official examples or simulation. Do not assume a SeriesT helper accepts PanelT. Positivity guards may exclude missing values only when positivity is also required by the thesis.

Never use:

```python
# INVALID: unavailable is not economically zero
fundamental = self.op.fillna(fundamental, value=0)
```

Coverage must be measured before and after all masks. A factor that works only because missing companies are excluded requires a coverage-risk label.

## 6. Ratio Contract

A ratio requires:

- numerator and denominator from compatible dates/frequencies or an explicit mixed-frequency thesis;
- a denominator with valid economic meaning;
- denominator guard;
- scale and sign interpretation;
- outlier treatment for cross-sectional use.

Canonical panel computation:

```python
ratio = self.feat.safe_divide_panel(numerator, denominator)
eligible = denominator > 0
```

Canonical time-series computation:

```python
known = self.op.notna(numerator) & self.op.notna(denominator)
eligible = known & (denominator > 0)
ratio = numerator / denominator
```

`safe_divide_panel` is a computational guard, not an economic-validity decision.

## 7. Canonical Factor Recipes

### Profitability

```text
net profit / total assets       -> ROA-like profitability
net profit / owners' equity     -> ROE-like profitability
```

Use positive denominator guards. ROE can become unstable near zero equity and is not automatically comparable across banks, insurers, securities firms, and non-financial firms.

### Earnings quality

```text
operating cash flow / net profit
(net profit - operating cash flow) / total assets
```

Require a clear sign convention and positive-profit guard when interpreting cash conversion. Generic operating cash flow is not a universal hard filter for financial institutions.

### Capital and leverage

```text
owners' equity / total assets
liabilities / total assets
cash and equivalents / total assets
```

These are broad descriptors, but their economic thresholds differ across industries.

### Liquidity

```text
current assets / current liabilities
```

Most meaningful for non-financial operating companies. It must not be assumed comparable for all financial-sector businesses.

### Working-capital quality

```text
receivables / total assets
inventories / total assets
change in receivables or inventories scaled by assets
```

Use primarily for accounting populations where receivables and inventory represent normal operations.

### Investment and financing

```text
capital expenditure / total assets
borrowings change / total assets
operating cash flow net of investment requirements
```

Verify cash-flow sign conventions before interpreting purchases, repayments, or outflows.

## 8. Accounting-Population Compatibility

The following is a conservative starting map, not a substitute for field-level domain verification.

| Factor family | Non-financial | Bank | Insurance | Securities |
|---|:---:|:---:|:---:|:---:|
| ROA/profitability | Broadly usable | Industry-specific interpretation | Use with caution | Use with caution |
| ROE | Usable with equity guard | Relevant but capital structure differs | Relevant but reserves matter | Relevant but volatile income mix |
| Generic CFO/assets | Broadly usable | Not a universal hard filter | Use with caution | Use with caution |
| Inventory/assets | Often meaningful | Not comparable | Not comparable | Not comparable |
| Current ratio | Often meaningful | Not comparable | Usually weak | Usually weak |
| Insurance premiums/reserves | Not applicable | Not applicable | Relevant | Not applicable |
| Commission/trading income | Business-dependent | Business-dependent | Sometimes relevant | Relevant |
| Leverage | Meaningful | Structurally different | Reserve-driven | Structurally different |

If no sector mask is available, prefer broadly meaningful factors, narrow the declared accounting scope, or classify the research result as coverage-fragile.

## 9. Event Versus Persistent State

### Persistent state

```python
roa = net_profit / total_assets
quality = known & (total_assets > 0) & (net_profit > 0) & (roa > 0.01)
```

The condition remains meaningful between reports, subject to staleness.

### Report event

```python
profit_change = self.op.pct_change(net_profit, periods=1)
report_event = self.op.notna(profit_change) & (profit_change > 0)
```

This is a step-change signal at new observations. It must not be described as continuously improving daily profit.

Raw percentage change is unsafe when the previous value is zero, negative, or changes sign. Prefer a delta scaled by positive assets/equity when economically appropriate.

## 10. Coverage and Hidden-Selection Risk

For each fundamental factor, record:

- median and minimum eligible-symbol count;
- eligible percentage of the universe;
- train/test coverage;
- zero-position or empty-cross-section periods;
- whether availability selects a particular industry/accounting template;
- whether performance survives a broader/narrower liquidity mask.

A mask is part of the model. It may encode size, liquidity, reporting quality, or sector exposure even when those effects are not named in the thesis.

## 11. Effective Sample Size

Daily forward-filled fundamentals do not create independent daily accounting observations. Research claims should consider:

- number of actual report updates;
- number of covered companies;
- cross-company correlation;
- common market and sector regimes;
- repeated exposure to the same stale value.

Do not describe sample size as `symbols × daily rows` for a fundamental event study.

## 12. Field Selection Record

Each idea file should record:

```yaml
fields:
  numerator: fun_is_net_profit_loss_after_tax_quarterly_panel
  denominator: fun_bs_total_assets_quarterly_panel
frequency: quarterly
signal_type: persistent_ratio
accounting_scope: broad_with_financial_sector_caution
missing_policy: unavailable
point_in_time: publication_date
coverage_risk: to_be_measured
sign_convention_verified: true
```

For a report event, also state the previous-observation logic and zero/sign-change handling.

## 13. Invalid Patterns

```python
# INVALID: raw size dominates cross-company comparison
signal = self.data.fun_is_net_profit_loss_after_tax_annual_panel
```

```python
# INVALID: missing becomes economically meaningful zero
profit = self.op.fillna(profit, value=0)
```

```python
# INVALID: denominator has no guard
yield_signal = eps / close
```

```python
# INVALID: daily forward-filled change described as daily earnings growth
growth = self.op.pct_change(quarterly_profit, periods=1)
```

The final example may be computed as a report-event indicator, but its thesis and holding logic must reflect that meaning.

## 14. Promotion Checklist

- [ ] Field names exactly match `data_syntax.md`.
- [ ] Publication-date point-in-time behavior is respected.
- [ ] Missing values remain unavailable.
- [ ] Signal is classified as level, ratio, event, quality, or risk state.
- [ ] Denominator is guarded and economically valid.
- [ ] Quarterly/annual mixing is justified.
- [ ] Percentage changes handle zero, negative, and sign-changing bases.
- [ ] Accounting populations are comparable or the scope is narrowed.
- [ ] Eligibility coverage and stability are measured.
- [ ] The mask is treated as part of the alpha model.
- [ ] Effective sample size is not overstated.
- [ ] Sign conventions for cash-flow fields are verified.
