# MASTER — Alpha Planning & Construction Reference

> This is the top-level planning document for all alpha research.
> Date created: 2026-08-05
> Purpose: Master reference for building cross-sectional alpha strategies from scratch
> Mode: `cross_sectional` (`_panel`, market-neutral, `set_portfolio_positions`)
> Predecessor: `idea/planning_alpha/stage_2/2026-08-04_alpha_generation_framework.md` (what to build)
> Companion: `idea/planning_alpha/stage_2/2026-08-05_alpha_validation_framework.md` (how to judge)

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

## TIER 1: DATA (nhóm các field lại)

### Group 1: Price & Volume

| Field | Type | Usage |
|---|---|---|
| `pv_close_panel` | daily | Price level, market value calculation |
| `pv_volume_panel` | daily | Liquidity, Amihud, volume signals |
| `pv_high_panel` | daily | ATR, VWAP, range signals |
| `pv_low_panel` | daily | ATR, VWAP, range signals |
| `pv_open_panel` | daily | Gap signals |
| `pv_vn30_close_panel` | daily | Market reference, beta |
| `pv_vn30_volume_panel` | daily | Market volume reference |

### Group 2: Income Statement — Profitability

| Field | Frequency | Usage |
|---|---|---|
| `fun_is_net_profit_loss_after_tax_*_panel` | Q/A | Core profitability (ROA, ROE) |
| `fun_is_eps_basis_*_panel` | Q/A | Earnings yield, EPS surprise |
| `fun_is_net_accounting_profit_loss_before_tax_*_panel` | Q/A | Interest coverage |
| `fun_is_financial_income_*_panel` | Q | Financial income decomposition |
| `fun_is_financial_expenses_*_panel` | Q | Interest expense |
| `fun_is_selling_expenses_*_panel` | Q | Cost discipline |
| `fun_is_general_and_admin_expenses_*_panel` | Q | Cost discipline |
| `fun_is_business_income_tax_current_*_panel` | Q | Tax stability |
| `fun_is_attributable_to_parent_company_*_panel` | Q | Minority interest drag |

### Group 3: Balance Sheet — Structure

| Field | Frequency | Usage |
|---|---|---|
| `fun_bs_total_assets_*_panel` | Q/A | Size, ROA denominator |
| `fun_bs_owners_equity_*_panel` | Q/A | ROE denominator, leverage |
| `fun_bs_cash_and_cash_equivalents_*_panel` | Q | Liquidity buffer |
| `fun_bs_current_assets_*_panel` | Q | Current ratio |
| `fun_bs_current_liabilities_*_panel` | Q | Current ratio |
| `fun_bs_short_term_loans_*_panel` | Q | Working capital safety |
| `fun_bs_inventories_net_*_panel` | Q | Inventory quality |
| `fun_bs_trade_accounts_receivable_*_panel` | Q | Receivables quality |
| `fun_bs_trade_accounts_payable_*_panel` | Q | Supplier credit |
| `fun_bs_advances_from_customers_*_panel` | Q | Customer advances |
| `fun_bs_good_will_*_panel` | Q | Intangible burden |
| `fun_bs_intangible_fixed_assets_*_panel` | Q | Intangible burden |
| `fun_bs_tangible_fixed_assets_*_panel` | Q | Capital productivity |
| `fun_bs_construction_in_progress_*_panel` | Q | Idle CIP risk |
| `fun_bs_common_shares_*_panel` | Q | Market value calculation |

### Group 4: Cash Flow — Operating

| Field | Frequency | Usage |
|---|---|---|
| `fun_cf_net_cash_inflows_outflows_from_operating_activities_*_panel` | A | CFO quality, cash conversion |
| `fun_cf_dividends_paid_*_panel` | A | Dividend sustainability |
| `fun_cf_proceeds_from_borrowings_*_panel` | A | External dependence |
| `fun_cf_repayment_of_borrowings_*_panel` | A | External dependence |
| `fun_cf_proceeds_from_issue_of_shares_*_panel` | A | Dilution, net payout |
| `fun_cf_payments_for_share_returns_and_repurchases_*_panel` | A | Net payout |
| `fun_cf_loans_granted_purchases_of_debt_instruments_*_panel` | A | Financial institution mask |

### Group 5: Financial Institution Identifiers

| Field | Frequency | Usage |
|---|---|---|
| `fun_bs_insurance_reserve_*_panel` | A | Insurance intensity |
| `fun_bs_unearned_premium_reserve_*_panel` | A | Insurance intensity |
| `fun_bs_margin_deposits_*_panel` | A | Securities intensity |

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

**From Group 1 (Price/Volume):**
```python
market_value = close * common_shares
traded_value = self.feat.rolling_value_panel(close, volume)
amihud = self.feat.amihud_illiquidity_panel(close, volume)
returns = self.feat.returns_panel(close)
smoothed = self.feat.ema_panel(returns)
```

**From Group 2 (Income):**
```python
roa = self.feat.safe_divide_panel(net_profit, total_assets)
roe = self.feat.safe_divide_panel(net_profit, owners_equity)
eps_yield = self.feat.safe_divide_panel(eps, close)
core_profit = self.feat.safe_divide_panel((net_profit + fin_expenses - fin_income), total_assets)
interest_coverage = self.feat.safe_divide_panel(profit_before_tax, fin_expenses)
cost_ratio = self.feat.safe_divide_panel((selling + gae), total_assets)
```

**From Group 3 (Balance Sheet):**
```python
leverage = self.feat.safe_divide_panel(liabilities, total_assets)
equity_ratio = self.feat.safe_divide_panel(owners_equity, total_assets)
current_ratio = self.feat.safe_divide_panel(current_assets, current_liabilities)
cash_ratio = self.feat.safe_divide_panel(cash, total_assets)
intangible_burden = self.feat.safe_divide_panel((goodwill + intangible), owners_equity)
capital_productivity = self.feat.safe_divide_panel(net_profit, tangible_fixed_assets)
cip_risk = self.feat.safe_divide_panel(construction_in_progress, total_assets)
```

**From Group 4 (Cash Flow):**
```python
net_payout = (0 - dividends) + (0 - repurchases) - issuance
net_payout_yield = self.feat.safe_divide_panel(net_payout, market_value)
persistent_payout = self.feat.ema_panel(net_payout_yield)
cash_conversion = self.feat.safe_divide_panel(cfo, net_profit)
dividend_sustainability = self.feat.safe_divide_panel(dividends, cfo)
external_dependence = self.feat.safe_divide_panel((proceeds_borrowings + proceeds_shares - repayments_borrowings), total_assets)
```

**From Group 5 (Financial Identifiers):**
```python
insurance_intensity = self.feat.safe_divide_panel(insurance_reserve, total_assets)
unearned_intensity = self.feat.safe_divide_panel(unearned_premium, total_assets)
loan_intensity = self.feat.safe_divide_panel(loans_granted, total_assets)
margin_intensity = self.feat.safe_divide_panel(margin_deposits, total_assets)
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
        dividends = self.data.fun_cf_dividends_paid_annual_panel
        repurchases = self.data.fun_cf_payments_for_share_returns_and_repurchases_annual_panel
        issuance = self.data.fun_cf_proceeds_from_issue_of_shares_annual_panel
        common_shares = self.data.fun_bs_common_shares_annual_panel
        close = self.data.pv_close_panel

        # Financial identifiers
        insurance_reserve = self.data.fun_bs_insurance_reserve_annual_panel
        unearned_premium = self.data.fun_bs_unearned_premium_reserve_annual_panel
        loans_granted = self.data.fun_cf_loans_granted_purchases_of_debt_instruments_annual_panel
        margin_deposits = self.data.fun_bs_margin_deposits_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel

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
        dividends = self.data.fun_cf_dividends_paid_annual_panel
        repurchases = self.data.fun_cf_payments_for_share_returns_and_repurchases_annual_panel
        issuance = self.data.fun_cf_proceeds_from_issue_of_shares_annual_panel
        common_shares = self.data.fun_bs_common_shares_annual_panel
        close = self.data.pv_close_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel

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
GROUP 1 (Price/Volume)
  ├── market_value = close × common_shares
  ├── traded_value = rolling_value_panel(close, volume)
  ├── amihud = amihud_illiquidity_panel(close, volume)
  └── returns = returns_panel(close)

GROUP 2 (Income)
  ├── roa = safe_divide_panel(ni, assets)
  ├── roe = safe_divide_panel(ni, equity)
  ├── eps_yield = safe_divide_panel(eps, close)
  ├── core_profit = safe_divide_panel((ni + fe - fi), assets)
  └── interest_coverage = safe_divide_panel(ni_bt, fe)

GROUP 3 (Balance Sheet)
  ├── leverage = safe_divide_panel(liabilities, assets)
  ├── equity_ratio = safe_divide_panel(equity, assets)
  ├── current_ratio = safe_divide_panel(ca, cl)
  ├── cash_ratio = safe_divide_panel(cash, assets)
  └── intangible_burden = safe_divide_panel(gw + intang, equity)

GROUP 4 (Cash Flow)
  ├── net_payout_yield = safe_divide_panel(gross_payout, mv)
  ├── persistent_payout = ema_panel(net_payout_yield)
  ├── cash_conversion = safe_divide_panel(cfo, ni)
  └── external_dependence = safe_divide_panel(borrow + issue - repay, assets)

GROUP 5 (Financial Identifiers)
  ├── insurance_intensity = safe_divide_panel(insurance_reserve, assets)
  ├── unearned_intensity = safe_divide_panel(unearned_premium, assets)
  └── margin_intensity = safe_divide_panel(margin_deposits, assets)

MASK LAYERS
  ├── L1: data availability (input_sum == input_sum)
  ├── L2: economic population (financial flag)
  ├── L3: sign/semantic (dividends < 0, equity > 0)
  ├── L4: liquidity gate (rank rolled_value > 0.40)
  └── L5: quality gate (equity/assets > 0.15)

OPS
  ├── normalize: rank_cs_panel / zscore_cs_panel / winsorize_cs_panel
  ├── weights: portfolio_weights_panel(method='rank_demean_l1')
  └── position: set_portfolio_positions(weights)
```
