# Cross-Sectional Strategy Patterns

This document contains construction patterns for one execution mode. It is not performance evidence. Exact fields, parameters, masks, and trial budgets must be preregistered and validated. Shared data comes from [`../data_syntax.md`](../data_syntax.md).

## 4. Cross-Sectional Quality Rank

```python
class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel

        quality = self.feat.safe_divide_panel(net_profit, total_assets)
        traded_value = self.feat.rolling_value_panel(close, volume)

        base_eligible = (
            (close > 0)
            & (volume > 0)
            & (net_profit > 0)
            & (total_assets > 0)
        )
        liquidity_rank = self.op.rank_cs_panel(
            traded_value,
            mask=base_eligible,
        )
        eligible = base_eligible & (liquidity_rank > 0.40)

        weights = self.op.portfolio_weights_panel(
            quality,
            method="rank_demean_l1",
            mask=eligible,
        )
        self.set_portfolio_positions(weights)
```

Rules:

- Use an economically meaningful ratio, not raw company size.
- Liquidity is an eligibility layer unless explicitly hypothesized as alpha.
- Audit eligible-symbol coverage and concentration.
- The positive-profit mask narrows the thesis; disclose that choice.
- Panel feature defaults must be recorded under `panel_feature_contract.md`.

## 5. Cross-Sectional Winsorized Magnitude

Use magnitude-sensitive weighting only if magnitude has meaning and outliers are controlled.

```python
factor = self.feat.safe_divide_panel(numerator, denominator)
eligible = (denominator > 0) & other_guards
clean = self.op.winsorize_cs_panel(
    factor,
    mask=eligible,
    lower=0.02,
    upper=0.98,
)
score = self.op.zscore_cs_panel(clean, mask=eligible)
weights = self.op.portfolio_weights_panel(
    score,
    method="demean_l1",
    mask=eligible,
)
self.set_portfolio_positions(weights)
```

Prefer `rank_demean_l1` when factor magnitude is unstable or accounting scales differ. `demean_l1` requires a stronger justification and robustness evidence.

## 6. Value Plus Trend

Keep the components interpretable and avoid repeated exponent search.

```python
earnings_yield = self.feat.safe_divide_panel(eps, close)
trend_ratio = self.feat.safe_divide_panel(
    close,
    self.feat.ema_panel(close),
)
value_rank = self.op.rank_cs_panel(earnings_yield, mask=eligible)
trend_rank = self.op.rank_cs_panel(trend_ratio, mask=eligible)
signal = value_rank + trend_rank
```

Before promotion:

- disclose any hidden/default EMA window;
- preregister component weights;
- compare against value-only and trend-only baselines;
- count all tested weight/exponent variants as one alpha family;
- reject a narrow peak that fails neighbouring specifications.

## 7. Liquidity as Eligibility

Canonical sequence:

```text
Economic factor
-> base validity mask
-> rolling traded value or Amihud measure
-> cross-sectional liquidity rank
-> final eligibility mask
-> factor normalization
-> portfolio weights
```

Do not claim liquidity alpha when liquidity only removes untradeable symbols. Test whether performance is stable across nearby eligibility thresholds.

## 8. Cross-Sectional Noise Filtering

Filter factor noise before weights so a handful of extreme or illiquid symbols do not drive
the book. Compose from existing `self.op` only.

```python
factor = self.feat.safe_divide_panel(numerator, denominator)
eligible = (denominator > 0) & liquidity_rank_eligible

# Remove extreme readings, then standardize with safe zero-variance handling.
clean = self.op.winsorize_cs_panel(factor, mask=eligible, lower=0.02, upper=0.98)
score = self.op.zscore_cs_panel(clean, mask=eligible, ddof=1)

# Ranks absorb magnitude instability; weights stay market-neutral.
signal = self.op.rank_cs_panel(clean, mask=eligible, method="average")
weights = self.op.portfolio_weights_panel(signal, method="rank_demean_l1", mask=eligible)
```

Rules:

- Winsorize/zscore/rank are noise filters, not alpha signals; keep magnitude weighting only
  when magnitude is economically meaningful.
- Restrict the cross-section with an eligibility `mask` (e.g. liquidity rank) before normalizing.
- Prefer `rank_demean_l1` when the factor scale is unstable across dates.
- Keep every filter causal; no centered windows or backfill.

## 9. Ablation Pattern

Every composite starts from a baseline:

```text
B0: price/trend baseline
B1: B0 + one fundamental quality component
B2: B1 + one liquidity eligibility layer
B3: B2 + one sizing or event overlay
```

Change one dimension per step. Record each variant, including failures. Do not optimize field, horizon, threshold, sizing, and exit simultaneously.

## 10. Anti-Patterns

### Raw monetary rank

```python
# INVALID research design: mostly ranks company size
signal = self.data.fun_is_net_profit_loss_after_tax_annual_panel
```

### Missing-to-zero eligibility

```python
# INVALID
profit = self.op.fillna(profit, value=0)
```

### Kitchen-sink entry

```python
# FRAGILE: too many unrelated hard gates
entry = quality & value & momentum & low_vol & low_leverage & volume & breakout
```

### Repeated factor amplification

```python
# FRAGILE unless preregistered and robust as a family
signal = value * trend * trend * trend * trend
```

### Test-driven repair

```text
Test fails -> add another condition -> rerun same test -> call it OOS
```

Once test results influence a change, that test is development data. See `validation_protocol.md`.

### Extreme-symbol dominance

```python
# FRAGILE: a few outliers drive weights; magnitudes never cleaned
weights = self.op.portfolio_weights_panel(factor, method="demean_l1", mask=eligible)
```

Winsorize/zscore/rank before magnitude weighting, or prefer `rank_demean_l1`.

## 11. Pattern Promotion Checklist

- [ ] Thesis selects the mode before testing.
- [ ] Field names and shapes are valid.
- [ ] Fundamental semantics follow `fundamental_data_contract.md`.
- [ ] Panel defaults/evidence follow `panel_feature_contract.md`.
- [ ] Baseline exists.
- [ ] Each ablation changes one component.
- [ ] Entry has no more than four primary economic conditions.
- [ ] Strong entry adds no more than two confirmations.
- [ ] Exit has no more than three OR branches.
- [ ] Cross-sectional coverage and concentration are audited.
- [ ] Factor noise is filtered (winsorize/zscore/rank or liquidity mask) and the filter recorded.
- [ ] All variants are tracked as one family.
- [ ] Final selection follows `validation_protocol.md`.
