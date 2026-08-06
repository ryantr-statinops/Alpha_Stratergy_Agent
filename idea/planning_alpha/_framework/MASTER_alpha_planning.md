# MASTER — 7-Layer Research Architecture

> Date: 2026-08-05
> Mode: `cross_sectional` (`_panel`, `set_portfolio_positions`)
> Hypotheses: `HYPOTHESIS_LIBRARY.md`
> Validation: `2026-08-05_alpha_validation_framework.md`

---

## Pipeline Contract

Every alpha follows exactly one path:

```
Layer 0  Raw Data
    ↓
Layer 1  Primitive Transforms
    ↓
Layer 2  Economic Factors
    ↓
Layer 3  Factor Diagnostics
    ↓
Layer 4  Economic Validation
    ↓
Layer 5  Eligibility Filters
    ↓
Layer 6  Composite Alpha
    ↓
Backtest
```

Rules:
- Exactly one mode: `cross_sectional` (all `_panel` fields)
- No mixing: Panel data ↔ Panel features ↔ `_cs_panel` ops ↔ `set_portfolio_positions`
- Point-in-time: fundamentals available only after publication date
- Missing = unavailable, not zero
- Every ratio must answer: "One unit of X creates how much Y?"
- Combine factors, NOT raw features

---

## Layer 0: Raw Data

> 496 fields. Source: `syntax/data_syntax.md`

### Group A — Price & Volume (daily)

| Field | Type |
|---|---|
| `pv_close_panel` | daily |
| `pv_open_panel` | daily |
| `pv_high_panel` | daily |
| `pv_low_panel` | daily |
| `pv_volume_panel` | daily |
| `pv_vn30_close_panel` | daily |
| `pv_vn30_open_panel` | daily |
| `pv_vn30_high_panel` | daily |
| `pv_vn30_low_panel` | daily |
| `pv_vn30_volume_panel` | daily |

### Group B — Profitability (Income Q/A)

| Field | Frequency |
|---|---|
| `fun_is_net_profit_loss_after_tax_*_panel` | Q/A |
| `fun_is_net_accounting_profit_loss_before_tax_*_panel` | Q/A |
| `fun_is_profit_from_financial_activities_*_panel` | Q/A |
| `fun_is_net_operating_income_from_other_activities_*_panel` | Q/A |
| `fun_is_other_income_*_panel` | Q/A |
| `fun_is_gain_loss_from_joint_ventures_*_panel` | Q/A |

### Group C — Cost & Margin (Income Q)

| Field | Frequency |
|---|---|
| `fun_is_selling_expenses_quarterly_panel` | Q |
| `fun_is_general_and_admin_expenses_quarterly_panel` | Q |
| `fun_is_financial_income_quarterly_panel` | Q |
| `fun_is_financial_expenses_quarterly_panel` | Q |
| `fun_is_total_compensation_quarterly_panel` | Q |
| `fun_is_compensation_quarterly_panel` | Q |
| `fun_is_expenses_from_other_activities_quarterly_panel` | Q |
| `fun_is_other_expenses_quarterly_panel` | Q |

### Group D — EPS & Attribution (Income Q/A)

| Field | Frequency |
|---|---|
| `fun_is_eps_basis_*_panel` | Q/A |
| `fun_is_attributable_to_parent_company_*_panel` | Q/A |
| `fun_is_minority_interests_*_panel` | Q/A |

### Group E — Tax & Reserves (Income Q/A)

| Field | Frequency |
|---|---|
| `fun_is_business_income_tax_current_*_panel` | Q/A |
| `fun_is_business_income_tax_deferred_*_panel` | Q/A |
| `fun_is_equalisation_reserve_*_panel` | Q/A |
| `fun_is_provision_for_catastrophe_reserve_*_panel` | Q/A |
| `fun_is_other_deductions_*_panel` | Q/A |

### Group F — Capital Structure (Balance Sheet Q/A)

| Field | Frequency |
|---|---|
| `fun_bs_total_assets_*_panel` | Q/A |
| `fun_bs_owners_equity_*_panel` | Q/A |
| `fun_bs_liabilities_*_panel` | Q/A |
| `fun_bs_total_resources_*_panel` | Q/A |
| `fun_bs_long_term_liabilities_*_panel` | Q/A |
| `fun_bs_capital_and_researves_*_panel` | Q/A |

### Group G — Cash & Liquidity (Balance Sheet Q/A)

| Field | Frequency |
|---|---|
| `fun_bs_cash_*_panel` | Q/A |
| `fun_bs_cash_equivalents_*_panel` | Q/A |
| `fun_bs_cash_and_cash_equivalents_*_panel` | Q/A |
| `fun_bs_short_term_investments_*_panel` | Q/A |
| `fun_bs_short_term_financial_investments_*_panel` | Q/A |
| `fun_bs_current_assets_*_panel` | Q/A |
| `fun_bs_current_liabilities_*_panel` | Q/A |

### Group H — Working Capital (Balance Sheet Q/A)

| Field | Frequency |
|---|---|
| `fun_bs_inventories_*_panel` | Q/A |
| `fun_bs_inventories_net_*_panel` | Q/A |
| `fun_bs_trade_accounts_receivable_*_panel` | Q/A |
| `fun_bs_trade_accounts_payable_*_panel` | Q/A |
| `fun_bs_accounts_receivable_*_panel` | Q/A |
| `fun_bs_advances_*_panel` | Q/A |
| `fun_bs_advances_from_customers_*_panel` | Q/A |
| `fun_bs_prepayments_to_suppliers_*_panel` | Q/A |
| `fun_bs_other_receivables_*_panel` | Q/A |
| `fun_bs_short_term_loans_*_panel` | Q/A |

### Group I — Long-term Assets (Balance Sheet Q/A)

| Field | Frequency |
|---|---|
| `fun_bs_tangible_fixed_assets_*_panel` | Q/A |
| `fun_bs_intangible_fixed_assets_*_panel` | Q/A |
| `fun_bs_construction_in_progress_*_panel` | Q/A |
| `fun_bs_good_will_*_panel` | Q/A |
| `fun_bs_investment_properties_*_panel` | Q/A |
| `fun_bs_finance_lease_assets_*_panel` | Q/A |
| `fun_bs_ppe_tangible_cost_*_panel` | Q/A |

### Group J — Investments (Balance Sheet Q/A)

| Field | Frequency |
|---|---|
| `fun_bs_long_term_investments_*_panel` | Q/A |
| `fun_bs_investments_in_subsidiaries_*_panel` | Q/A |
| `fun_bs_investments_in_associates_*_panel` | Q/A |
| `fun_bs_held_to_maturity_investment_current_*_panel` | Q/A |
| `fun_bs_held_to_maturity_investment_non_current_*_panel` | Q/A |
| `fun_bs_long_term_loans_*_panel` | Q/A |
| `fun_bs_short_term_loans_receivables_*_panel` | Q/A |

### Group K — Equity Structure (Balance Sheet Q/A)

| Field | Frequency |
|---|---|
| `fun_bs_paid_in_capital_*_panel` | Q/A |
| `fun_bs_common_shares_*_panel` | Q/A |
| `fun_bs_treasury_shares_*_panel` | Q/A |
| `fun_bs_undistributed_earnings_*_panel` | Q/A |
| `fun_bs_capital_surplus_*_panel` | Q/A |
| `fun_bs_preferred_shares_*_panel` | Q/A |
| `fun_bs_bonus_and_welfare_funds_*_panel` | Q/A |
| `fun_bs_statutory_reserve_*_panel` | Q/A |
| `fun_bs_investment_and_development_funds_*_panel` | Q/A |

### Group L — Financial Institution Identifiers (BS/CF — mask-only)

| Field | Source |
|---|---|
| `fun_bs_insurance_reserve_*_panel` | BS |
| `fun_bs_unearned_premium_reserve_*_panel` | BS |
| `fun_bs_mathematical_reserve_*_panel` | BS |
| `fun_bs_claim_reserve_*_panel` | BS |
| `fun_bs_margin_deposits_*_panel` | BS |
| `fun_bs_reinsurance_assets_*_panel` | BS |
| `fun_bs_insurance_deposits_*_panel` | BS |
| `fun_bs_payables_from_insurance_contract_*_panel` | BS |
| `fun_bs_receivable_from_insurance_contract_*_panel` | BS |
| `fun_bs_equalization_reserves_*_panel` | BS |
| `fun_cf_loans_granted_purchases_of_debt_instruments_*_panel` | CF |
| `fun_cf_collection_of_loans_proceeds_from_sales_of_debts_instruments_*_panel` | CF |

### Group M — Operating Cash Flow (Q/A)

| Field | Frequency |
|---|---|
| `fun_cf_net_cash_inflows_outflows_from_operating_activities_*_panel` | Q/A |
| `fun_cf_operating_profit_loss_before_changes_in_wc_*_panel` | Q/A |
| `fun_cf_business_income_tax_paid_*_panel` | Q/A |
| `fun_cf_interest_paid_*_panel` | Q/A |
| `fun_cf_interest_income_and_dividend_*_panel` | Q/A |
| `fun_cf_depreciation_and_amortisation_*_panel` | Q/A |
| `fun_cf_provisions_*_panel` | Q/A |

### Group N — Investing Cash Flow (Q/A)

| Field | Frequency |
|---|---|
| `fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_*_panel` | Q/A |
| `fun_cf_proceeds_from_disposal_of_fixed_assets_*_panel` | Q/A |
| `fun_cf_investments_in_other_entities_*_panel` | Q/A |
| `fun_cf_proceeds_from_divestment_in_other_entities_*_panel` | Q/A |
| `fun_cf_profit_loss_from_investing_activities_*_panel` | Q/A |

### Group O — Financing Cash Flow (Q/A)

| Field | Frequency |
|---|---|
| `fun_cf_dividends_paid_*_panel` | Q/A |
| `fun_cf_proceeds_from_issue_of_shares_*_panel` | Q/A |
| `fun_cf_payments_for_share_returns_and_repurchases_*_panel` | Q/A |
| `fun_cf_proceeds_from_borrowings_*_panel` | Q/A |
| `fun_cf_repayment_of_borrowings_*_panel` | Q/A |
| `fun_cf_finance_lease_principal_payments_*_panel` | Q/A |
| `fun_cf_net_cash_inflows_outflows_from_financing_activities_*_panel` | Q/A |

### Group P — Cash Reconciliation (Q/A)

| Field | Frequency |
|---|---|
| `fun_cf_net_increase_in_cash_and_cash_equivalents_*_panel` | Q/A |
| `fun_cf_cash_and_cash_equivalents_at_the_beginning_of_period_*_panel` | Q/A |
| `fun_cf_cash_and_cash_equivalents_at_the_end_of_period_*_panel` | Q/A |
| `fun_cf_effect_of_foreign_exchange_differences_*_panel` | Q/A |
| `fun_cf_amortisation_of_goodwill_*_panel` | Q/A |
| `fun_cf_increase_decrease_in_inventories_*_panel` | Q/A |
| `fun_cf_increase_decrease_in_receivables_*_panel` | Q/A |
| `fun_cf_increase_decrease_in_payables_*_panel` | Q/A |

---

## Layer 1: Primitive Transform Library

> Every transform must answer: "What does this operation mean economically?"
> Functions available: `cross_sectional/feature_syntax.md`

### Normalization

| Transform | Function | Economic Meaning | Example |
|---|---|---|---|
| Ratio | `safe_divide_panel(a, b)` | One unit of b creates a of output | ROA = NI / Assets |
| Log | `log(a)` | Diminishing sensitivity | Log market cap |
| Per Share | `safe_divide_panel(value, shares)` | Value per share | EPS, BVPS |
| Per Asset | `safe_divide_panel(value, assets)` | Asset efficiency | ROA, asset turnover |
| Per EV | `safe_divide_panel(value, ev)` | Enterprise value efficiency | EV/EBITDA inverse |

### Temporal

| Transform | Function | Economic Meaning | Example |
|---|---|---|---|
| Growth | `returns_panel(x)` or `(x - x_lag) / abs(x_lag)` | Rate of change | Revenue growth |
| Delta | `delta_panel(x)` | Absolute change | Delta ROE |
| Acceleration | `delta_panel(delta_panel(x))` | Change of change | Earnings acceleration |
| Rolling | `rolling_mean_panel(x)`, `rolling_std_panel(x)` | Smoothed trend/vol | 4Q avg ROA |
| TTM | `rolling_sum_panel(x, 4)` | Trailing twelve months | TTM revenue |
| Stability | `rolling_std_panel(x) / rolling_mean_panel(x)` | Consistency | Earnings stability |
| Trend | `ema_panel(x)` or `sma_panel(x)` | Directional trend | Price trend |

### Cross Feature

| Transform | Function | Economic Meaning | Example |
|---|---|---|---|
| Spread | `a - b` | Differential | Yield spread |
| Difference | `a - b` (different fields) | Gap | CFO - Net Profit |
| Interaction | `a * b` | Combined effect | Value × Momentum |
| Residual | `a - regression(a, b)` | Idiosyncratic component | Factor residual |

### Statistical

| Transform | Function | Economic Meaning | Example |
|---|---|---|---|
| Rank | `rolling_rank_panel(x)` | Relative position | Percentile rank |
| Winsorize | `winsorize_cs_panel(x)` | Outlier control | Clipped signal |
| Z-score | `rolling_zscore_panel(x)` | Standardized deviation | Rolling z-score |
| Neutralize | `demean_cs_panel(x)` | Cross-sectional neutral | Market-neutral signal |

---

## Layer 2: Economic Factors

> 10 factors. Each factor = one testable economic hypothesis.
> Hypothesis details: `HYPOTHESIS_LIBRARY.md`

### Factor 1: Value

> "The market systematically underprices fundamentals."

| Ratio | Formula | Raw Fields | Transform |
|---|---|---|---|
| Book/Market | equity / market_value | F, A, K | Ratio |
| Earnings Yield | EPS / close | D, A | Ratio |
| CFO Yield | CFO / market_value | M, A, K | Ratio |
| Dividend Yield | dividends_paid / market_value | O, A, K | Ratio |
| EV/EBITDA | enterprise_value / EBITDA | F, B, A, K | Ratio |

### Factor 2: Quality

> "Well-run firms with durable profitability outperform."

| Ratio | Formula | Raw Fields | Transform |
|---|---|---|---|
| ROA | net_profit / total_assets | B, F | Ratio |
| ROE | net_profit / equity | B, F | Ratio |
| Cash Conversion | CFO / net_profit | M, B | Ratio |
| Accrual Quality | (CFO - net_profit) / total_assets | M, B, F | Ratio + Ratio |
| Earnings Stability | rolling_std(ROA) / rolling_mean(ROA) | B, F | Rolling + Stability |

### Factor 3: Growth

> "Firms with accelerating growth earn a premium."

| Ratio | Formula | Raw Fields | Transform |
|---|---|---|---|
| Revenue Growth | revenue(t) / revenue(t-1) - 1 | B | Growth |
| EPS Growth | eps(t) / eps(t-1) - 1 | D | Growth |
| Asset Growth | assets(t) / assets(t-1) - 1 | F | Growth |
| Retention Ratio | 1 - (dividends / net_profit) | O, B | Ratio |

### Factor 4: Momentum

> "Recent winners continue to outperform."

| Ratio | Formula | Raw Fields | Transform |
|---|---|---|---|
| Price/EMA | close / ema(close) | A | Trend |
| ROE Improvement | delta(rolling_mean(ROE)) | B, F | Delta + Rolling |
| Earnings Acceleration | delta(delta(EPS)) | D | Acceleration |
| Relative Strength | rank(returns_6m) | A | Rank + Growth |

### Factor 5: Leverage

> "Conservative capital structures outperform."

| Ratio | Formula | Raw Fields | Transform |
|---|---|---|---|
| Debt/Assets | liabilities / total_assets | F | Ratio |
| Net Debt | (debt - cash) / total_assets | F, G | Spread + Ratio |
| Interest Coverage | PBT / interest_expenses | B, C | Ratio |
| Debt/Equity | liabilities / equity | F | Ratio |

### Factor 6: Liquidity

> "Liquid firms are mispriced in illiquid markets."

| Ratio | Formula | Raw Fields | Transform |
|---|---|---|---|
| Current Ratio | current_assets / current_liabilities | G | Ratio |
| Cash/Assets | cash / total_assets | G, F | Ratio |
| Quick Ratio | (cash + receivables) / current_liabilities | G, H, F | Ratio |
| WC/Assets | (receivables + inventories - payables) / total_assets | H, F | Ratio |

### Factor 7: Efficiency

> "Lean operations generate superior returns."

| Ratio | Formula | Raw Fields | Transform |
|---|---|---|---|
| Asset Turnover | revenue / total_assets | B, F | Ratio |
| Inventory Days | (inventory / revenue) * 365 | H, B | Ratio |
| Receivable Days | (receivables / revenue) * 365 | H, B | Ratio |
| Payable Days | (payables / COGS) * 365 | H, C | Ratio |

### Factor 8: Capital Allocation

> "Smart capital return creates shareholder value."

| Ratio | Formula | Raw Fields | Transform |
|---|---|---|---|
| Net Payout Yield | (dividends + repurchases - issuance) / market_value | O, A, K | Ratio |
| Buyback Yield | repurchases / market_value | O, A, K | Ratio |
| Capex/Depreciation | capex / depreciation | N, M | Ratio |
| Debt Repayment Rate | repayment / total_debt | O, F | Ratio |

### Factor 9: Operating Quality

> "Operational excellence drives durable alpha."

| Ratio | Formula | Raw Fields | Transform |
|---|---|---|---|
| Margin Stability | rolling_std(margin) / rolling_mean(margin) | B, C | Stability |
| WC Burden | (receivables + inventories - payables) / total_assets | H, F | Ratio |
| Fixed Asset Utilization | revenue / tangible_fixed_assets | B, I | Ratio |
| SG&A Efficiency | (selling + GAE) / revenue | C, B | Ratio |

### Factor 10: Risk

> "Low-risk firms earn superior risk-adjusted returns."

| Ratio | Formula | Raw Fields | Transform |
|---|---|---|---|
| Volatility | rolling_std(returns, 60) | A | Rolling |
| Beta | covariance(r, market) / var(market) | A | Rolling + Statistical |
| Max Drawdown | rolling_min(returns) | A | Rolling |
| Downside Vol | rolling_std(returns[returns < 0]) | A | Rolling |

---

## Layer 3: Factor Diagnostics

> Evaluate BEFORE validation and backtest.
> If diagnostics fail, do not proceed.

### Required Diagnostics

| Diagnostic | Metric | Threshold | Action on Fail |
|---|---|---|---|
| Coverage | % of universe with non-null factor | > 70% | Check data quality |
| IC | Pearson correlation(factor, forward_return) | > 0.02 | Factor weak, review |
| Rank IC | Spearman correlation(factor, forward_return) | > 0.02 | Factor weak, review |
| Turnover | Annual portfolio turnover | < 80% | Over-trading risk |
| Sector Exposure | Max sector weight - min sector weight | < 30% | Sector neutralize |
| Size Exposure | Rank correlation(factor, log_market_cap) | < 0.5 | Size tilt risk |
| Liquidity Exposure | Rank correlation(factor, traded_value) | < 0.5 | Liquidity tilt risk |
| Correlation Matrix | Correlation with existing factors | < 0.6 | Redundant factor |
| Monotonicity | Quintile spread sign consistency | > 70% | Non-monotonic |
| Decay | IC decay half-life (quarters) | > 4 | Signal fades fast |
| Regime Stability | IC sign consistency across regimes | > 60% | Regime-dependent |

### Diagnostic Pipeline

```
Factor computed
    ↓
Calculate: coverage, IC, rank IC
    ↓
Coverage > 70%? → NO → Stop. Check data.
    ↓ YES
IC > 0.02? → NO → Stop. Factor too weak.
    ↓ YES
Calculate: turnover, sector/size/liquidity exposure
    ↓
Turnover < 80%? → NO → Review signal stability.
    ↓ YES
Exposure < 0.5? → NO → Add neutralization.
    ↓ YES
Calculate: correlation with existing factors
    ↓
Correlation < 0.6? → NO → Redundant. Merge or drop.
    ↓ YES
Calculate: monotonicity, decay, regime stability
    ↓
ALL PASS → Proceed to Validation (Layer 4)
```

---

## Layer 4: Economic Validation

> Cross-statement consistency checks.
> Different from Diagnostics (Layer 3): Diagnostics = factor quality; Validation = data truth.

### Accounting Validation

| Rule | Check | Threshold | Meaning |
|---|---|---|---|
| NI vs CFO | `abs(net_profit - CFO) / total_assets` | < 0.05 | Earnings quality |
| Inventory vs Revenue | `inventory_growth / revenue_growth` | < 1.5 OR negative flags | Inventory bloat |
| Receivables vs Cash | `receivables_growth / revenue_growth` | < 1.5 | Channel stuffing |
| Debt vs Capex | `debt_change - capex` | debt_change < 2x capex | Financing mismatch |
| Equity vs Retained Earnings | `delta_equity - net_profit - equity_issuance` | near zero | Accounting integrity |

### Economic Validation

| Rule | Check | Threshold | Meaning |
|---|---|---|---|
| Capex → PPE | `capex > 0` implies `delta_PPE > 0` | consistent | Investment reality |
| Debt → Interest | `interest_paid / avg_debt` | > 0.02 | Debt is real |
| Revenue → Tax | `tax_paid / revenue` | > 0 and < 0.5 | Tax consistency |
| Dividend → Cash | `dividends_paid < CFO` | required | Dividend sustainability |

### Statistical Validation

| Rule | Check | Threshold | Meaning |
|---|---|---|---|
| Coverage | Factor available for > 70% of universe | required | Data completeness |
| Outlier | No > 5% of observations beyond 5 sigma | required | No data errors |
| Missing | Missing rate < 30% per field | required | Data quality |
| Industry Bias | Factor mean difference across sectors | < 2 sigma | No sector artifact |
| Factor Correlation | New factor vs existing factors | < 0.6 | Independence |

---

## Layer 5: Eligibility Filters

> Comprehensive filters applied BEFORE composite and backtest.
> Each filter must have economic justification.

### Filter Layers

| Layer | Filter | Code | Economic Justification |
|---|---|---|---|
| L1 | Data availability | `input_sum == input_sum` | NaN = no data |
| L2 | Population | `financial_flag == False` | Different accounting standards |
| L3 | Sign/semantic | `dividends < 0`, `equity > 0` | Panel convention + solvency |
| L4 | Positive denominator | `denominator > 0` for all ratios | Avoid spurious signals |
| L5 | Liquidity gate | `rank(traded_value) > 0.40` | Tradable universe |
| L6 | Market-cap gate | Optional: `log(market_cap) > threshold` | Minimum size |
| L7 | Minimum history | `quarters_available >= 4` | Sufficient data for rolling |
| L8 | Report availability | Point-in-time publication check | Avoid look-ahead bias |
| L9 | Quality gate | `equity / assets > 0.15` | Capital strength |
| L10 | Accounting validity | `assets > 0`, `equity > -0.5 * assets` | Data reasonableness |

### Combined Eligibility Example

```python
eligible = (
    # L1: Data availability
    (input_sum == input_sum)
    # L2: Non-financial population
    & (financial_flag == False)
    # L3: Sign convention
    & (dividends < 0) & (equity > 0)
    # L4: Positive denominators
    & (total_assets > 0) & (market_value > 0) & (close > 0)
    # L5: Liquidity
    & (liquidity_rank > 0.40)
    # L7: Minimum history
    & (quarters_available >= 4)
    # L9: Quality
    & (equity_ratio > 0.15)
    # L10: Accounting validity
    & (total_assets > 0)
)
```

---

## Layer 6: Composite Alpha

> Combine FACTORS, NOT raw features.
> Each composite must document: which factors, what weights, why.

### Composite Policies

| Policy | Formula | When to Use |
|---|---|---|
| Equal Weight | `signal = mean(z(f1), z(f2), ...)` | Default, simple, robust |
| Inverse Correlation | `w_i = 1 / corr(f_i, sum(f))` | Diversify correlated factors |
| Risk Parity | `w_i = 1 / volatility(f_i)` | Equal risk contribution |
| IC Weighted | `w_i = IC(f_i)` | Reward stronger factors |
| Sharpe Weighted | `w_i = sharpe(f_i)` | Reward risk-adjusted factors |

### Composite Rules

1. **Z-score before combining:** All factor scores must be cross-sectionally z-scored
2. **Check correlation:** If corr(f1, f2) > 0.6, consider merging
3. **Document rationale:** Why these factors? Why these weights?
4. **Anti-overfit:** Maximum 3 factors in one composite (more = overfit risk)
5. **Diversification benefit:** Composite Sharpe should exceed max(Sharpe of individual factors)

### Reference Composites

```
Quality + Value
    = 0.5 * z(quality_score) + 0.5 * z(value_score)
    Rationale: Quality confirms value is real, not a trap

Value + Momentum
    = 0.5 * z(value_score) + 0.5 * z(momentum_score)
    Rationale: Value catches mispricing, momentum confirms direction

Quality + Value + Momentum
    = 0.4 * z(quality) + 0.3 * z(value) + 0.3 * z(momentum)
    Rationale: Triple factor, highest diversification

Quality + Capital Allocation
    = 0.5 * z(quality_score) + 0.5 * z(capital_allocation_score)
    Rationale: Quality operations + smart capital return
```

---

## Reference Alphas

> Regression tests for the framework. Each reference alpha validates one architecture path.

### Ref-01: Pure Value (Book/Market)

```
Layer 0: equity (F), close (A), shares (K)
Layer 1: book_per_share = equity / shares (Ratio)
         book_to_market = book_per_share / close (Ratio)
Layer 2: Factor = Value
Layer 3: IC ~ 0.03-0.05, turnover ~ 35%
Layer 4: Validation: equity > 0
Layer 5: Eligibility: liquidity > 0.30, history >= 4Q
Layer 6: Single factor, no composite
```

### Ref-02: Pure Quality (ROE)

```
Layer 0: net_profit (B), equity (F)
Layer 1: roe = net_profit / equity (Ratio)
         roe_stability = rolling_std(roe) / rolling_mean(roe) (Stability)
Layer 2: Factor = Quality
Layer 3: IC ~ 0.03-0.04, turnover ~ 25%
Layer 4: Validation: NI vs CFO < 0.05
Layer 5: Eligibility: equity > 0, assets > 0, history >= 4Q
Layer 6: Single factor, no composite
```

### Ref-03: Quality + Value

```
Layer 0-2: Quality score (Ref-02) + Value score (Ref-01)
Layer 3: IC(q) ~ 0.03, IC(v) ~ 0.04, corr(q,v) ~ 0.2
Layer 4: Both validation rules applied
Layer 5: Combined eligibility
Layer 6: Composite: 0.5 * z(quality) + 0.5 * z(value)
```

### Ref-04: Value + Momentum

```
Layer 0-2: Value score (Ref-01) + Momentum score (close/ema)
Layer 3: IC(v) ~ 0.04, IC(m) ~ 0.05, corr(v,m) ~ -0.1
Layer 4: Both validation rules applied
Layer 5: Combined eligibility
Layer 6: Composite: 0.5 * z(value) + 0.5 * z(momentum)
```

### Ref-05: Quality + Momentum

```
Layer 0-2: Quality score (Ref-02) + Momentum score (close/ema)
Layer 3: IC(q) ~ 0.03, IC(m) ~ 0.05, corr(q,m) ~ 0.1
Layer 4: Both validation rules applied
Layer 5: Combined eligibility
Layer 6: Composite: 0.5 * z(quality) + 0.5 * z(momentum)
```

### Ref-06: Triple Composite (Quality + Value + Momentum)

```
Layer 0-2: Quality + Value + Momentum
Layer 3: All ICs > 0.02, all pairwise corr < 0.5
Layer 4: All validation rules applied
Layer 5: Combined eligibility
Layer 6: Composite: 0.4 * z(quality) + 0.3 * z(value) + 0.3 * z(momentum)
```

### Ref-07: Net Payout Yield

```
Layer 0: dividends (O), repurchases (O), issuance (O), close (A), shares (K)
Layer 1: gross_payout = -(dividends) - (repurchases) - issuance (Spread)
         market_value = close * shares (Ratio)
         net_payout_yield = gross_payout / market_value (Ratio)
         persistent_payout = ema(net_payout_yield) (Trend)
Layer 2: Factor = Capital Allocation
Layer 3: IC ~ 0.04-0.06, turnover ~ 30%
Layer 4: Validation: dividends < 0, shares > 0
Layer 5: Eligibility: liquidity > 0.40, history >= 4Q
Layer 6: Single factor, no composite
```

### Ref-08: Value-Trend Engine

```
Layer 0: eps (D), close (A), equity (F), assets (F)
Layer 1: earnings_yield = eps / close (Ratio)
         trend_ratio = close / ema(close) (Trend)
         capital_strength = equity / assets (Ratio)
Layer 2: Factor = Value × Momentum interaction
Layer 3: IC ~ 0.05-0.08, turnover ~ 40%
Layer 4: Validation: eps > 0, equity > 0
Layer 5: Eligibility: capital_strength > 0.15, liquidity > 0.40, history >= 4Q
Layer 6: Composite: core = earnings_yield * trend_ratio^12
```

---

## Checklist Before Submit

- [ ] Hypothesis documented in `HYPOTHESIS_LIBRARY.md`
- [ ] Every ratio answers "one unit of X creates how much Y?"
- [ ] Factor passes Layer 3 diagnostics (coverage, IC, turnover, exposure)
- [ ] Validation passes Layer 4 (accounting + economic + statistical)
- [ ] Eligibility filters applied (Layer 5)
- [ ] Composite uses factors, not raw features (Layer 6)
- [ ] All data fields end in `_panel`
- [ ] All operators use `_cs_panel` form
- [ ] Position API is `set_portfolio_positions`
- [ ] Missing fundamentals are unavailable, not zero
- [ ] Denominator guards on all ratios
- [ ] Point-in-time: no backward shift/backfill
- [ ] Sign conventions verified for cash-flow fields
- [ ] Passes `python tools/validate_framework.py --strict`

---

## Quick Reference

```
LAYER 0 — Raw Data
    496 fields: pv_* (10), fun_is_* (130), fun_bs_* (271), fun_cf_* (85)

LAYER 1 — Primitive Transforms
    Normalization: Ratio, Log, Per Share, Per Asset, Per EV
    Temporal: Growth, Delta, Acceleration, Rolling, TTM, Stability, Trend
    Cross Feature: Spread, Difference, Interaction, Residual
    Statistical: Rank, Winsorize, Z-score, Neutralize

LAYER 2 — Economic Factors
    Value: Book/Market, Earnings Yield, CFO Yield, Dividend Yield
    Quality: ROA, ROE, Cash Conversion, Accrual, Earnings Stability
    Growth: Revenue Growth, EPS Growth, Asset Growth, Retention
    Momentum: Price/EMA, ROE Improvement, Earnings Acceleration
    Leverage: Debt/Assets, Net Debt, Interest Coverage
    Liquidity: Current Ratio, Cash/Assets, Quick Ratio
    Efficiency: Asset Turnover, Inventory Days, Receivable Days
    Capital Allocation: Net Payout, Buyback, Capex/Debt
    Operating Quality: Margin Stability, WC Burden, Asset Utilization
    Risk: Volatility, Beta, Max Drawdown

LAYER 3 — Factor Diagnostics
    Coverage, IC, Rank IC, Turnover, Sector/Size/Liquidity Exposure
    Correlation Matrix, Monotonicity, Decay, Regime Stability

LAYER 4 — Economic Validation
    Accounting: NI vs CFO, Inv vs Rev, Rec vs Cash, Debt vs Capex
    Economic: Capex→PPE, Debt→Interest, Rev→Tax, Div→Cash
    Statistical: Coverage, Outlier, Missing, Industry Bias

LAYER 5 — Eligibility Filters
    L1-L10: Data availability, Population, Sign, Positive denominator
    Liquidity gate, Market-cap gate, Minimum history, Report availability
    Quality gate, Accounting validity

LAYER 6 — Composite Alpha
    Policies: Equal Weight, Inverse Correlation, Risk Parity, IC/Sharpe Weighted
    Rules: Max 3 factors, Z-score first, Corr < 0.6, Document rationale

OPS
    normalize: rank_cs_panel / zscore_cs_panel / winsorize_cs_panel
    weights: portfolio_weights_panel(method='rank_demean_l1')
    position: set_portfolio_positions(weights)
```
