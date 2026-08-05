# MASTER — Alpha Planning & Construction Reference

> This is the top-level planning document for all alpha research.
> Date created: 2026-08-05
> Purpose: Master reference for building cross-sectional alpha strategies from scratch
> Mode: `cross_sectional` (`_panel`, market-neutral, `set_portfolio_positions`)
> Predecessor: `idea/planning_alpha/stage_2/2026-08-04_alpha_generation_framework.md` (what to build)
> Companion: `idea/planning_alpha/stage_2/2026-08-05_alpha_validation_framework.md` (how to judge)
> Combinations: `idea/planning_alpha/_framework/DATA_GROUP_COMBINATIONS.md` (16 groups, 120 pairs)

## Pipeline Contract

Every alpha follows exactly one path:

```
DATA → FEAT → MASK → OP → SET_POSITION
```

Rules:
- Exactly one mode: `cross_sectional` (all `_panel` fields)
- No mixing: Panel data ↔ Panel features ↔ `_cs_panel` ops ↔ `set_portfolio_positions`
- Point-in-time: fundamentals available only after publication date
- Missing = unavailable, not zero

---

## TIER 1: DATA (16 groups — see DATA_GROUP_COMBINATIONS.md)

> Full field lists and 120 pair combinations in `DATA_GROUP_COMBINATIONS.md`.

### Group A — Price & Volume (daily)

| Field | Usage |
|---|---|
| `pv_close_panel` | Price level, market value calculation |
| `pv_open_panel` | Gap signals |
| `pv_high_panel` | ATR, VWAP, range signals |
| `pv_low_panel` | ATR, VWAP, range signals |
| `pv_volume_panel` | Liquidity, Amihud, volume signals |
| `pv_vn30_close_panel` | Market reference, beta |
| `pv_vn30_open_panel` | VN30 gap |
| `pv_vn30_high_panel` | VN30 range |
| `pv_vn30_low_panel` | VN30 range |
| `pv_vn30_volume_panel` | Market volume reference |

### Group B — Profitability (Income Q/A)

| Field | Usage |
|---|---|
| `fun_is_net_profit_loss_after_tax_*_panel` | Core profitability (ROA, ROE) |
| `fun_is_net_accounting_profit_loss_before_tax_*_panel` | Pre-tax profit, interest coverage |
| `fun_is_profit_from_financial_activities_*_panel` | Financial income decomposition |
| `fun_is_net_operating_income_from_other_activities_*_panel` | Non-core operating income |
| `fun_is_other_income_*_panel` | Other income |
| `fun_is_gain_loss_from_joint_ventures_*_panel` | JV contribution |

### Group C — Cost & Margin (Income Q)

| Field | Usage |
|---|---|
| `fun_is_selling_expenses_quarterly_panel` | Selling cost discipline |
| `fun_is_general_and_admin_expenses_quarterly_panel` | G&A cost discipline |
| `fun_is_financial_income_quarterly_panel` | Interest income decomposition |
| `fun_is_financial_expenses_quarterly_panel` | Interest expense |
| `fun_is_total_compensation_quarterly_panel` | Labor cost |
| `fun_is_compensation_quarterly_panel` | Direct compensation |
| `fun_is_expenses_from_other_activities_quarterly_panel` | Non-core expenses |
| `fun_is_other_expenses_quarterly_panel` | Other expenses |

### Group D — EPS & Attribution (Income Q/A)

| Field | Usage |
|---|---|
| `fun_is_eps_basis_*_panel` | EPS yield, EPS surprise |
| `fun_is_attributable_to_parent_company_*_panel` | Parent-company EPS |
| `fun_is_minority_interests_*_panel` | Minority drag |

### Group E — Tax & Reserves (Income Q/A)

| Field | Usage |
|---|---|
| `fun_is_business_income_tax_current_*_panel` | Current tax |
| `fun_is_business_income_tax_deferred_*_panel` | Deferred tax |
| `fun_is_equalisation_reserve_*_panel` | Insurance tax smoothing |
| `fun_is_provision_for_catastrophe_reserve_*_panel` | Catastrophe reserve |
| `fun_is_other_deductions_*_panel` | Other deductions |

### Group F — Capital Structure (Balance Sheet Q/A)

| Field | Usage |
|---|---|
| `fun_bs_total_assets_*_panel` | Size, ROA denominator, quality gate |
| `fun_bs_owners_equity_*_panel` | ROE denominator, leverage |
| `fun_bs_liabilities_*_panel` | Total debt |
| `fun_bs_total_resources_*_panel` | Total resources |
| `fun_bs_long_term_liabilities_*_panel` | Long-term debt |
| `fun_bs_capital_and_researves_*_panel` | Capital base |

### Group G — Cash & Liquidity (Balance Sheet Q/A)

| Field | Usage |
|---|---|
| `fun_bs_cash_*_panel` | Cash |
| `fun_bs_cash_equivalents_*_panel` | Cash equivalents |
| `fun_bs_cash_and_cash_equivalents_*_panel` | Total cash position |
| `fun_bs_short_term_investments_*_panel` | Liquid investments |
| `fun_bs_short_term_financial_investments_*_panel` | Short-term financial investments |
| `fun_bs_current_assets_*_panel` | Current assets |
| `fun_bs_current_liabilities_*_panel` | Current liabilities |

### Group H — Working Capital (Balance Sheet Q/A)

| Field | Usage |
|---|---|
| `fun_bs_inventories_*_panel` | Inventory |
| `fun_bs_inventories_net_*_panel` | Net inventory |
| `fun_bs_trade_accounts_receivable_*_panel` | Trade receivables |
| `fun_bs_trade_accounts_payable_*_panel` | Trade payables |
| `fun_bs_accounts_receivable_*_panel` | Other receivables |
| `fun_bs_advances_*_panel` | Advances |
| `fun_bs_advances_from_customers_*_panel` | Customer advances |
| `fun_bs_prepayments_to_suppliers_*_panel` | Prepayments |
| `fun_bs_other_receivables_*_panel` | Other receivables |
| `fun_bs_short_term_loans_*_panel` | Short-term loans (liability) |

### Group I — Long-term Assets (Balance Sheet Q/A)

| Field | Usage |
|---|---|
| `fun_bs_tangible_fixed_assets_*_panel` | Tangible FA |
| `fun_bs_intangible_fixed_assets_*_panel` | Intangible FA |
| `fun_bs_construction_in_progress_*_panel` | CIP (idle capital risk) |
| `fun_bs_good_will_*_panel` | Goodwill |
| `fun_bs_investment_properties_*_panel` | Investment property |
| `fun_bs_finance_lease_assets_*_panel` | Finance lease assets |
| `fun_bs_ppe_tangible_cost_*_panel` | PPE cost |

### Group J — Investments (Balance Sheet Q/A)

| Field | Usage |
|---|---|
| `fun_bs_long_term_investments_*_panel` | Long-term investments |
| `fun_bs_investments_in_subsidiaries_*_panel` | Subsidiary investments |
| `fun_bs_investments_in_associates_*_panel` | Associate investments |
| `fun_bs_held_to_maturity_investment_current_*_panel` | HTM (current) |
| `fun_bs_held_to_maturity_investment_non_current_*_panel` | HTM (non-current) |
| `fun_bs_long_term_loans_*_panel` | Long-term loans (receivable) |
| `fun_bs_short_term_loans_receivables_*_panel` | Short-term loans (receivable) |
| `fun_bs_long_term_receivables_*_panel` | Long-term receivables |

### Group K — Equity Structure (Balance Sheet Q/A)

| Field | Usage |
|---|---|
| `fun_bs_paid_in_capital_*_panel` | Paid-in capital |
| `fun_bs_common_shares_*_panel` | Common shares (for market value) |
| `fun_bs_treasury_shares_*_panel` | Treasury shares (negative) |
| `fun_bs_undistributed_earnings_*_panel` | Retained earnings |
| `fun_bs_capital_surplus_*_panel` | Capital surplus |
| `fun_bs_preferred_shares_*_panel` | Preferred shares |
| `fun_bs_bonus_and_welfare_funds_*_panel` | Bonus/welfare funds |
| `fun_bs_statutory_reserve_*_panel` | Statutory reserve |
| `fun_bs_investment_and_development_funds_*_panel` | Investment/dev funds |

### Group L — Financial Institution Identifiers (BS/CF — mask-only)

| Field | Source | Usage |
|---|---|---|
| `fun_bs_insurance_reserve_*_panel` | BS | Insurance intensity |
| `fun_bs_unearned_premium_reserve_*_panel` | BS | Insurance intensity |
| `fun_bs_mathematical_reserve_*_panel` | BS | Insurance intensity |
| `fun_bs_claim_reserve_*_panel` | BS | Insurance intensity |
| `fun_bs_margin_deposits_*_panel` | BS | Securities intensity |
| `fun_bs_reinsurance_assets_*_panel` | BS | Reinsurance intensity |
| `fun_bs_insurance_deposits_*_panel` | BS | Insurance deposits |
| `fun_bs_payables_from_insurance_contract_*_panel` | BS | Insurance payables |
| `fun_bs_receivable_from_insurance_contract_*_panel` | BS | Insurance receivables |
| `fun_bs_equalization_reserves_*_panel` | BS | Equalisation reserve |
| `fun_cf_loans_granted_purchases_of_debt_instruments_*_panel` | CF | Loans granted |
| `fun_cf_collection_of_loans_proceeds_from_sales_of_debts_instruments_*_panel` | CF | Loan collection |

### Group M — Operating Cash Flow (Q/A)

| Field | Usage |
|---|---|
| `fun_cf_net_cash_inflows_outflows_from_operating_activities_*_panel` | CFO |
| `fun_cf_operating_profit_loss_before_changes_in_wc_*_panel` | CFO before WC |
| `fun_cf_business_income_tax_paid_*_panel` | Tax paid |
| `fun_cf_interest_paid_*_panel` | Interest paid |
| `fun_cf_interest_income_and_dividend_*_panel` | Interest/dividend received |
| `fun_cf_dividends_and_interest_received_*_panel` | Dividends + interest received |
| `fun_cf_depreciation_and_amortisation_*_panel` | Depreciation (non-cash add-back) |
| `fun_cf_provisions_*_panel` | Provisions |

### Group N — Investing Cash Flow (Q/A)

| Field | Usage |
|---|---|
| `fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_*_panel` | Capex |
| `fun_cf_proceeds_from_disposal_of_fixed_assets_*_panel` | Disposal proceeds |
| `fun_cf_investments_in_other_entities_*_panel` | Investments in others |
| `fun_cf_proceeds_from_divestment_in_other_entities_*_panel` | Divestment proceeds |
| `fun_cf_profit_loss_from_investing_activities_*_panel` | Investment P&L |

### Group O — Financing Cash Flow (Q/A)

| Field | Usage |
|---|---|
| `fun_cf_dividends_paid_*_panel` | Dividends (outflow <= 0) |
| `fun_cf_proceeds_from_issue_of_shares_*_panel` | Share issuance (inflow > 0) |
| `fun_cf_payments_for_share_returns_and_repurchases_*_panel` | Repurchases (outflow <= 0) |
| `fun_cf_proceeds_from_borrowings_*_panel` | Borrowings proceeds |
| `fun_cf_repayment_of_borrowings_*_panel` | Borrowings repayment |
| `fun_cf_finance_lease_principal_payments_*_panel` | Lease payments |
| `fun_cf_net_cash_inflows_outflows_from_financing_activities_*_panel` | Net financing CF |

### Group P — Cash Reconciliation (Q/A)

| Field | Usage |
|---|---|
| `fun_cf_net_increase_in_cash_and_cash_equivalents_*_panel` | Net cash change |
| `fun_cf_cash_and_cash_equivalents_at_the_beginning_of_period_*_panel` | Beginning cash |
| `fun_cf_cash_and_cash_equivalents_at_the_end_of_period_*_panel` | Ending cash |
| `fun_cf_effect_of_foreign_exchange_differences_*_panel` | FX effect |
| `fun_cf_amortisation_of_goodwill_*_panel` | Goodwill amortisation |
| `fun_cf_increase_decrease_in_inventories_*_panel` | WC: inventories change |
| `fun_cf_increase_decrease_in_receivables_*_panel` | WC: receivables change |
| `fun_cf_increase_decrease_in_payables_*_panel` | WC: payables change |

---

## TIER 2: FEAT (build từ mỗi nhóm data)

### Core Transform Functions

| Function | Input | Output | Usage |
|---|---|---|---|
| `safe_divide_panel(a, b)` | PanelT | PanelT | Ratios (avoids div-by-zero) |
| `ema_panel(x)` | PanelT | PanelT | Smoothing, trend |
| `sma_panel(x)` | PanelT | PanelT | Smoothing, trend |
| `delta_panel(x)` | PanelT | PanelT | Change (1-period) |
| `returns_panel(x)` | PanelT | PanelT | Returns |
| `rolling_zscore_panel(x)` | PanelT | PanelT | Z-score normalization |
| `rolling_mean_panel(x)` | PanelT | PanelT | Rolling average |
| `rolling_std_panel(x)` | PanelT | PanelT | Rolling volatility |
| `rolling_rank_panel(x)` | PanelT | PanelT | Rolling percentile rank |
| `rolling_value_panel(close, volume)` | PanelT | PanelT | Traded value |

### Feature Recipes by Data Group

**From Group A (Price/Volume):**
```python
market_value = close * common_shares    # common_shares from K
traded_value = self.feat.rolling_value_panel(close, volume)
amihud = self.feat.amihud_illiquidity_panel(close, volume)
returns = self.feat.returns_panel(close)
smoothed = self.feat.ema_panel(returns)
```

**From Group B (Profitability):**
```python
roa = self.feat.safe_divide_panel(net_profit, total_assets)     # total_assets from F
roe = self.feat.safe_divide_panel(net_profit, owners_equity)    # owners_equity from F
eps_yield = self.feat.safe_divide_panel(eps, close)             # eps from D
core_profit = self.feat.safe_divide_panel((net_profit + fin_expenses - fin_income), total_assets)
```

**From Group C (Cost & Margin):**
```python
interest_coverage = self.feat.safe_divide_panel(profit_before_tax, fin_expenses)
cost_ratio = self.feat.safe_divide_panel((selling + gae), total_assets)   # total_assets from F
```

**From Group D (EPS & Attribution):**
```python
eps_yield = self.feat.safe_divide_panel(eps, close)             # close from A
minority_drag = self.feat.safe_divide_panel(minority_interests, owners_equity)  # from F
```

**From Group E (Tax & Reserves):**
```python
effective_tax = self.feat.safe_divide_panel(tax_current, profit_before_tax)  # from B
```

**From Group F (Capital Structure):**
```python
leverage = self.feat.safe_divide_panel(liabilities, total_assets)
equity_ratio = self.feat.safe_divide_panel(owners_equity, total_assets)
quality_gate = (equity_ratio > 0.15)
```

**From Group G (Cash & Liquidity):**
```python
current_ratio = self.feat.safe_divide_panel(current_assets, current_liabilities)
cash_ratio = self.feat.safe_divide_panel(cash, total_assets)    # total_assets from F
net_cash = self.feat.safe_divide_panel((cash - short_term_loans), total_assets)
```

**From Group H (Working Capital):**
```python
wc_lean = self.feat.safe_divide_panel((receivables + inventories - payables), total_assets)  # from F
receivables_turnover = self.feat.safe_divide_panel(receivables, total_assets)  # from F
inventory_to_assets = self.feat.safe_divide_panel(inventories, total_assets)   # from F
```

**From Group I (Long-term Assets):**
```python
capital_productivity = self.feat.safe_divide_panel(net_profit, tangible_fixed_assets)  # from B
intangible_burden = self.feat.safe_divide_panel((goodwill + intangible), owners_equity)  # from F
cip_risk = self.feat.safe_divide_panel(construction_in_progress, total_assets)  # from F
```

**From Group J (Investments):**
```python
investment_intensity = self.feat.safe_divide_panel(long_term_investments, total_assets)  # from F
subsidiary_burden = self.feat.safe_divide_panel(investments_in_subsidiaries, total_assets)  # from F
```

**From Group K (Equity Structure):**
```python
dilution = self.feat.safe_divide_panel(treasury_shares, common_shares)
book_per_share = self.feat.safe_divide_panel(owners_equity, common_shares)  # from F
retained_ratio = self.feat.safe_divide_panel(undistributed_earnings, owners_equity)  # from F
```

**From Group L (Financial Identifiers — mask-only):**
```python
insurance_intensity = self.feat.safe_divide_panel(insurance_reserve, total_assets)  # from F
unearned_intensity = self.feat.safe_divide_panel(unearned_premium, total_assets)
loan_intensity = self.feat.safe_divide_panel(loans_granted, total_assets)
margin_intensity = self.feat.safe_divide_panel(margin_deposits, total_assets)
```

**From Group M (Operating CF):**
```python
cash_conversion = self.feat.safe_divide_panel(cfo, net_profit)     # net_profit from B
fcf_proxy = self.feat.safe_divide_panel((cfo - capex), market_value)  # capex from N, market_value from A
dividend_sustainability = self.feat.safe_divide_panel(dividends, cfo)  # dividends from O
```

**From Group N (Investing CF):**
```python
capex_intensity = self.feat.safe_divide_panel(capex, total_assets)  # total_assets from F
net_capex = self.feat.safe_divide_panel((capex - disposal), market_value)  # market_value from A
```

**From Group O (Financing CF):**
```python
net_payout = (0 - dividends) + (0 - repurchases) - issuance
net_payout_yield = self.feat.safe_divide_panel(net_payout, market_value)  # market_value from A
persistent_payout = self.feat.ema_panel(net_payout_yield)
external_dependence = self.feat.safe_divide_panel((proceeds_borrowings + proceeds_shares - repayments_borrowings), total_assets)  # from F
```

---

## TIER 3: MASK (build từ feat/nhóm)

### Mask Layer 1: Data Availability

```python
# NaN check via arithmetic identity (PanelT-compatible)
input_sum = field1 + field2 + field3
available = (input_sum == input_sum)

# Positivity guards (also exclude missing)
eligible = (close > 0) & (volume > 0) & (denominator > 0) & (numerator > 0)
```

### Mask Layer 2: Economic/Accounting Population

```python
# Financial institution flag (proxy — no sector field)
financial = (
    (insurance_intensity > 0.05)
    | (unearned_intensity > 0.05)
    | (loan_intensity > 0.03)
    | (loan_intensity < -0.03)
    | (margin_intensity > 0.03)
)
non_financial = (financial == False)
```

### Mask Layer 3: Sign/Semantic Guards

```python
# Cash flow sign convention (verify before use)
dividends_negative = (dividends < 0)          # outflow
repurchases_nonpositive = (repurchases <= 0)  # outflow or zero
common_shares_positive = (common_shares > 0)
equity_positive = (owners_equity > 0)
stl_positive = (short_term_loans > 0)         # for coverage ratio
```

### Mask Layer 4: Liquidity/Capacity Gate

```python
# Rank traded value — keep top 60%
traded_value = self.feat.rolling_value_panel(close, volume)
ranked_tv = self.op.rank_cs_panel(traded_value)
liquidity_gate = (ranked_tv > 0.40)
```

### Mask Layer 5: Quality Gate

```python
# Capital strength floor
equity_ratio = self.feat.safe_divide_panel(owners_equity, total_assets)
quality_gate = (equity_ratio > 0.15)
```

### Combined Mask Example

```python
eligible = (
    available
    & (close > 0)
    & (volume > 0)
    & (market_value > 0)
    & (common_shares > 0)
    & (dividends < 0)
    & (repurchases <= 0)
    & liquidity_gate
    & quality_gate
    # & financial  # uncomment if restricting to financial population
)
```

---

## TIER 4: OP + SET_POSITION

### Cross-Sectional Normalization

| Function | Usage | When to use |
|---|---|---|
| `rank_cs_panel(signal, mask=)` | Percentile rank | Most signals (robust to outliers) |
| `zscore_cs_panel(signal, mask=)` | Z-score | When magnitude is meaningful |
| `demean_cs_panel(signal, mask=)` | Subtract mean | When direction matters |
| `winsorize_cs_panel(signal, mask=, lower=0.02, upper=0.98)` | Clip outliers | Before zscore |
| `normalize_l1_cs_panel(signal, mask=)` | Unit L1 exposure | Before portfolio weights |

### Portfolio Construction

```python
# Standard: market-neutral, unit gross exposure
weights = self.op.portfolio_weights_panel(
    signal,
    method='rank_demean_l1',
    mask=eligible,
    max_abs_weight=None,  # set if concentration control needed
)
self.set_portfolio_positions(weights)
```

### Common Patterns

**Pattern A: Rank → Z-score → Weights**
```python
score = self.op.zscore_cs_panel(signal, mask=eligible)
weights = self.op.portfolio_weights_panel(score, method='rank_demean_l1', mask=eligible)
```

**Pattern B: EMA → Rank → Weights**
```python
smoothed = self.feat.ema_panel(raw_signal)
score = self.op.zscore_cs_panel(smoothed, mask=eligible)
weights = self.op.portfolio_weights_panel(score, method='rank_demean_l1', mask=eligible)
```

**Pattern C: Winsorize → Z-score → Weights**
```python
clipped = self.op.winsorize_cs_panel(signal, mask=eligible, lower=0.02, upper=0.98)
score = self.op.zscore_cs_panel(clipped, mask=eligible)
weights = self.op.portfolio_weights_panel(score, method='rank_demean_l1', mask=eligible)
```

---

## Worked Examples

### Example 1: VnSmallCsFinancialNetPayout

**Economic thesis:** Financial firms with persistent net payout yield (dividends + repurchases - issuance) signal shareholder-friendly policies and sustainable cash generation.

```python
class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # TIER 1: DATA
        dividends = self.data.fun_cf_dividends_paid_annual_panel            # Group O
        repurchases = self.data.fun_cf_payments_for_share_returns_and_repurchases_annual_panel  # Group O
        issuance = self.data.fun_cf_proceeds_from_issue_of_shares_annual_panel  # Group O
        common_shares = self.data.fun_bs_common_shares_annual_panel         # Group K
        close = self.data.pv_close_panel                                    # Group A

        # Financial identifiers (Group L)
        insurance_reserve = self.data.fun_bs_insurance_reserve_annual_panel
        unearned_premium = self.data.fun_bs_unearned_premium_reserve_annual_panel
        loans_granted = self.data.fun_cf_loans_granted_purchases_of_debt_instruments_annual_panel
        margin_deposits = self.data.fun_bs_margin_deposits_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel           # Group F

        # TIER 2: FEAT
        # Financial intensity
        insurance_intensity = self.feat.safe_divide_panel(insurance_reserve, total_assets)
        unearned_intensity = self.feat.safe_divide_panel(unearned_premium, total_assets)
        loan_intensity = self.feat.safe_divide_panel(loans_granted, total_assets)
        margin_intensity = self.feat.safe_divide_panel(margin_deposits, total_assets)

        # Market value
        market_value = close * common_shares

        # Net payout yield
        gross_payout = (0 - dividends) + (0 - repurchases) - issuance
        net_payout_yield = self.feat.safe_divide_panel(gross_payout, market_value)
        persistent_payout = self.feat.ema_panel(net_payout_yield)

        # TIER 3: MASK
        financial = (
            (insurance_intensity > 0.05)
            | (unearned_intensity > 0.05)
            | (loan_intensity > 0.03)
            | (loan_intensity < -0.03)
            | (margin_intensity > 0.03)
        )

        input_sum = dividends + repurchases + issuance + common_shares + close
        eligible = (
            (input_sum == input_sum)
            & (dividends < 0)
            & (repurchases <= 0)
            & (common_shares > 0)
            & (close > 0)
            & (market_value > 0)
            & (financial == True)
        )

        # TIER 4: OP + SET_POSITION
        payout_score = self.op.zscore_cs_panel(persistent_payout, mask=eligible)
        weights = self.op.portfolio_weights_panel(
            payout_score,
            method='rank_demean_l1',
            mask=eligible,
        )
        self.set_portfolio_positions(weights)
```

### Example 2: VnSmallCsNetPayoutPersistence

**Economic thesis:** Smoothed net payout yield indicates durable shareholder returns; persistence separates signal from noise.

```python
class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # TIER 1: DATA (same as Example 1)
        dividends = self.data.fun_cf_dividends_paid_annual_panel            # Group O
        repurchases = self.data.fun_cf_payments_for_share_returns_and_repurchases_annual_panel  # Group O
        issuance = self.data.fun_cf_proceeds_from_issue_of_shares_annual_panel  # Group O
        common_shares = self.data.fun_bs_common_shares_annual_panel         # Group K
        close = self.data.pv_close_panel                                    # Group A
        total_assets = self.data.fun_bs_total_assets_annual_panel           # Group F

        # TIER 2: FEAT
        market_value = close * common_shares
        gross_payout = (0 - dividends) + (0 - repurchases) - issuance
        net_payout_yield = self.feat.safe_divide_panel(gross_payout, market_value)
        persistent_payout = self.feat.ema_panel(net_payout_yield)

        # TIER 3: MASK
        input_sum = dividends + repurchases + issuance + common_shares + close
        eligible = (
            (input_sum == input_sum)
            & (dividends < 0)
            & (repurchases <= 0)
            & (common_shares > 0)
            & (close > 0)
            & (market_value > 0)
        )

        # TIER 4: OP + SET_POSITION
        payout_score = self.op.zscore_cs_panel(persistent_payout, mask=eligible)
        weights = self.op.portfolio_weights_panel(
            payout_score,
            method='rank_demean_l1',
            mask=eligible,
        )
        self.set_portfolio_positions(weights)
```

---

## Checklist Before Submit

- [ ] Exactly one mode declared (`cross_sectional`)
- [ ] All data fields end in `_panel`
- [ ] All features use `_panel` form
- [ ] All operators use `_cs_panel` form
- [ ] Position API is `set_portfolio_positions`
- [ ] No SeriesT helper assumed to support PanelT
- [ ] Missing fundamentals are unavailable, not zero
- [ ] Denominator guards on all ratios
- [ ] Point-in-time: no backward shift/backfill
- [ ] Mask is economic, not just NaN-filter
- [ ] Signal type classified (level/ratio/event/quality/risk)
- [ ] Sign conventions verified for cash-flow fields
- [ ] Passes `python tools/validate_framework.py --strict`

---

## Quick Reference: Data Groups → Features → Masks → Ops

```
GROUP A (Price/Volume)
  ├── market_value = close × common_shares (K)
  ├── traded_value = rolling_value_panel(close, volume)
  ├── amihud = amihud_illiquidity_panel(close, volume)
  └── returns = returns_panel(close)

GROUP B (Profitability)
  ├── roa = safe_divide_panel(ni, assets)
  ├── roe = safe_divide_panel(ni, equity)
  ├── core_profit = safe_divide_panel((ni + fe - fi), assets)
  └── eps_yield = safe_divide_panel(eps (D), close)

GROUP C (Cost & Margin)
  ├── interest_coverage = safe_divide_panel(ni_bt, fe)
  └── cost_ratio = safe_divide_panel((selling + gae), assets)

GROUP D (EPS & Attribution)
  ├── eps_yield = safe_divide_panel(eps, close)
  └── minority_drag = safe_divide_panel(minority, equity)

GROUP E (Tax & Reserves)
  └── effective_tax = safe_divide_panel(tax, ni_bt)

GROUP F (Capital Structure)
  ├── leverage = safe_divide_panel(liabilities, assets)
  ├── equity_ratio = safe_divide_panel(equity, assets)
  └── quality_gate = (equity_ratio > 0.15)

GROUP G (Cash & Liquidity)
  ├── current_ratio = safe_divide_panel(ca, cl)
  ├── cash_ratio = safe_divide_panel(cash, assets)
  └── net_cash = safe_divide_panel((cash - st_loans), assets)

GROUP H (Working Capital)
  ├── wc_lean = safe_divide_panel((rec + inv - pay), assets)
  └── receivables_turnover = safe_divide_panel(rec, assets)

GROUP I (Long-term Assets)
  ├── capital_productivity = safe_divide_panel(ni, tangible_fa)
  ├── intangible_burden = safe_divide_panel((gw + intang), equity)
  └── cip_risk = safe_divide_panel(cip, assets)

GROUP J (Investments)
  ├── investment_intensity = safe_divide_panel(lt_inv, assets)
  └── subsidiary_burden = safe_divide_panel(sub_inv, assets)

GROUP K (Equity Structure)
  ├── dilution = safe_divide_panel(treasury, common_shares)
  ├── book_per_share = safe_divide_panel(equity, common_shares)
  └── retained_ratio = safe_divide_panel(undistributed, equity)

GROUP L (Financial ID — mask-only)
  ├── insurance_intensity = safe_divide_panel(insurance_reserve, assets)
  ├── unearned_intensity = safe_divide_panel(unearned_premium, assets)
  ├── loan_intensity = safe_divide_panel(loans_granted, assets)
  └── margin_intensity = safe_divide_panel(margin_deposits, assets)

GROUP M (Operating CF)
  ├── cash_conversion = safe_divide_panel(cfo, ni)
  └── fcf_proxy = safe_divide_panel((cfo - capex), mv)

GROUP N (Investing CF)
  ├── capex_intensity = safe_divide_panel(capex, assets)
  └── net_capex = safe_divide_panel((capex - disposal), mv)

GROUP O (Financing CF)
  ├── net_payout_yield = safe_divide_panel(gross_payout, mv)
  ├── persistent_payout = ema_panel(net_payout_yield)
  └── external_dependence = safe_divide_panel((borrow + issue - repay), assets)

GROUP P (Cash Reconciliation — validation only)
  └── cash_bridge: beginning → operating → investing → financing → ending

MASK LAYERS
  ├── L1: data availability (input_sum == input_sum)
  ├── L2: economic population (financial flag from L)
  ├── L3: sign/semantic (dividends < 0, equity > 0)
  ├── L4: liquidity gate (rank rolled_value > 0.40)
  └── L5: quality gate (equity/assets > 0.15)

OPS
  ├── normalize: rank_cs_panel / zscore_cs_panel / winsorize_cs_panel
  ├── weights: portfolio_weights_panel(method='rank_demean_l1')
  └── position: set_portfolio_positions(weights)
```
