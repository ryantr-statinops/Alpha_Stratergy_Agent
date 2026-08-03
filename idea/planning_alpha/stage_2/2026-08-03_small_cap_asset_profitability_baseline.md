---
hypothesis_id: HYP-SMALL-QUALITY-002
family_id: small-asset-profitability-baseline
variant_id: baseline
parent_baseline: null
filepath: vn_small_cap/cross_sectional/VnSmallCsAssetProfitabilityBaseline.py
created_at: 2026-08-03
universe: VN-SMALL-CAP
mode: cross_sectional
thesis: Profitable small-cap companies with stronger quarterly earnings relative to their asset base are underpriced relative to weaker peers.
accounting_scope: broad_with_financial_sector_caution
signal_type:
  - ratio
  - quality
fields:
  - pv_close_panel
  - pv_volume_panel
  - fun_is_net_profit_loss_after_tax_quarterly_panel
  - fun_bs_total_assets_quarterly_panel
features:
  - safe_divide_panel
operators:
  - portfolio_weights_panel
planned_variants: 1
trial_number: 1
trials_run: 1
dimensions_changed: []
selection_metric: final_test_sharpe
rejection_rule: Reject as validated unless Aggregate, Train, and Test each pass all five VN-SMALL-CAP thresholds; label fragile if Test Sharpe retention is below 50 percent.
default_window_dependency: false
validation_status: DRAFT
final_test_opened: false
final_test_opened_at: null
retuned_after_test: false
embargo_verified: true
train_pass: null
validation_pass: null
final_oos_pass: null
sharpe_retention: null
coverage_train: null
coverage_test: null
concentration_note: Platform output does not currently expose sector or symbol contribution diagnostics.
known_limitations:
  - ROA-like profitability is not fully comparable across banks, insurers, securities firms, and non-financial companies.
  - No documented sector-neutralization operator is available.
  - Positive-profit and positive-asset eligibility can create an accounting-coverage tilt.
---

# Small-Cap Asset Profitability Baseline

## Concept

Build the simplest possible cross-sectional fundamental-quality baseline: rank companies by quarterly net profit relative to total assets and hold a market-neutral portfolio through `rank_demean_l1` weights.

This is deliberately a one-variant family. It tests whether a broad, interpretable profitability signal survives the platform's chronological Train/Test split without parameter search.

## Why VN-SMALL-CAP

Small-cap prices may incorporate fundamental quality more slowly than larger, more widely followed companies. Scaling profit by assets avoids ranking companies primarily by size.

## Mode

`cross_sectional` is required because the hypothesis asks which companies are relatively more profitable at each timestamp, rather than when one company should be held.

## Signal

```text
asset_profitability = quarterly net profit after tax / quarterly total assets
```

Eligibility requires:

- positive close;
- positive volume;
- positive quarterly net profit;
- positive quarterly total assets.

The positive-profit guard is part of the thesis and also prevents sign-changing loss observations from being treated as comparable profitability.

## Portfolio Construction

```text
Raw panel fields
-> safe asset-profitability ratio
-> economic validity mask
-> rank_demean_l1 portfolio weights
-> market-neutral portfolio
```

No EMA, rolling feature, threshold search, factor exponent, or extra liquidity rank is used. Therefore the strategy has no hidden rolling-window dependency.

## Point-in-Time Discipline

Quarterly fields are consumed only after XNOQuant aligns them to publication date. The latest published values may remain forward-filled until a new report appears. They are treated as persistent quality states, not daily earnings observations.

No backward shift, backfill, daily fundamental growth, or missing-to-zero conversion is allowed.

## Preregistered Validation Decision

The strategy is accepted as `OOS_PASS` only if Aggregate, Train, and Test independently pass all five current VN-SMALL-CAP thresholds:

| Metric | Threshold |
|---|---:|
| Sharpe | >= 1.0 |
| CAGR | >= 25% |
| Max Drawdown | >= -45% |
| Profit Factor | >= 1.30 |
| Calmar | >= 0.8 |

Additional governance:

- Report Test/Train Sharpe retention.
- Label `OOS_FRAGILE` if retention is below 50%, even if absolute metrics pass.
- Do not modify the strategy after viewing Test and continue calling the same Test OOS.
- If it fails, report the failure without adding rescue conditions.

## Expected Risks

1. Hidden sector/accounting exposure because no sector-neutralization primitive is documented.
2. Eligibility may favor companies with cleaner or more complete reporting.
3. Fundamental values update infrequently, reducing effective sample size.
4. Market-neutral weighting can still contain sector, size, beta, or liquidity exposure.
5. Small-cap transaction costs and capacity may not be fully represented by reported summary metrics.
