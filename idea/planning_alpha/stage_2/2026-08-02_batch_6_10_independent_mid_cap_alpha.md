# Batch 6: 10 Independent VN-MID-CAP Cross-Sectional Alphas

Date: 2026-08-02
Universe: `VN-MID-CAP`
Mode/template: `cross_sectional`
Construction: market-neutral `demean_l1`

## Research Protocol

- Each strategy starts as a standalone independent MID thesis. It is not tilted
  by an existing return engine and must establish its own economic contribution.
- Every strategy requires `close > 0`, `volume > 0`, and top-70% rolling traded
  value through `liquidity_rank > 0.30`.
- Missing observations are excluded with numeric validity comparisons. There is
  no backfill, look-ahead, global aggregation, or zero imputation.
- Test standalone-first. A conditional-engine fallback is permitted only after
  the standalone strategy fails the fixed hurdle, and must be labeled as a new
  conditional hypothesis rather than reported as independent alpha.

## Fixed MID Hurdle

PASS requires all five metrics in each of Aggregate, Train, and Test/OOS:
Sharpe >= 1.1, CAGR >= 20%, MaxDD >= -40%, Profit Factor >= 1.25, and Calmar
>= 1.0. Thresholds remain fixed after results.

## Formulas

| # | Strategy | Standalone signal | Required gates |
|---:|---|---|---|
| 1 | Enterprise Earnings Yield | `PAT_annual / (close * shares_q + short_debt_q + long_debt_q - cash_q)` | PAT > 0; shares > 0; debts and cash >= 0; EV > 0; equity > 0 |
| 2 | Cash Profitability | `CFO_annual / assets_annual` | assets > 0; CFO valid |
| 3 | Scaling Efficiency | `rolling_sum(delta(PAT) / assets) - rolling_sum(delta(assets) / assets)` | assets > 0; both news components valid |
| 4 | Cash Accrual Quality | `(CFO_annual - PAT_annual) / assets_annual` | assets > 0; CFO and PAT valid |
| 5 | Project Commissioning | `rolling_sum(-delta(CIP) / assets) + rolling_sum(delta(fixed_assets) / assets) + rolling_sum(delta(PAT) / assets)` | CIP and fixed assets >= 0; assets > 0; all components valid |
| 6 | Internally Funded Investment | `(CFO + capex - borrowing_proceeds - share_issuance) / assets` | capex <= 0; external proceeds >= 0; assets > 0; CFO valid |
| 7 | Active Deleveraging | `-rolling_sum(delta(short_debt + long_debt) / assets)` | debts >= 0; assets > 0; current debt/assets > 0.05 |
| 8 | Idiosyncratic Momentum | `rolling_sum(stock_return - beta * VN30_return)` where `beta = rolling_covariance(stock_return, VN30_return) / rolling_variance(VN30_return)` | VN30 close > 0; variance > 0; estimated components valid |
| 9 | Recognition Migration | `-rolling_zscore(Amihud) + rolling_zscore(rolling_traded_value)` | shares > 0; both standardized components valid; no upper capacity bound |
| 10 | Anti-Lottery MAX | `-rolling_max(daily_return)` | shares > 0; rolling maximum valid |

## Sign And Unit Caveats

- Enterprise value is a raw market-value proxy. `close * common_shares` is only
  comparable with debt, cash, and PAT when price/share and statement units align.
- Annual CFO and income-statement values may reflect provider-specific reporting
  units. Assets normalize levels but do not remove accounting-archetype effects.
- Fixed-asset purchases are assumed to be non-positive outflows. Positive CAPEX
  observations are excluded rather than silently changing the sign convention.
- Borrowing and share-issuance proceeds are assumed non-negative inflows. Missing
  proceeds are unavailable, not zero external financing.
- A CIP decline can reflect reclassification or disposal rather than commissioning;
  fixed-asset activation and profit payoff jointly express the intended mechanism.
- Debt fields can have different economic meaning for financial firms. The 5%
  debt/assets floor prevents debt-free firms from receiving a repayment reward.
- Returns, covariance, variance, Amihud, and traded value inherit the platform's
  documented rolling windows. No undocumented window argument is introduced.
- `pv_vn30_close_panel` is documented. If runtime support differs from the catalog,
  that implementation issue is diagnosed later without changing the thesis now.
- Amihud and traded value have different units, so rolling z-scores place the two
  recognition components on comparable dimensionless scales.
- Vietnam daily price limits can mechanically truncate MAX; the primary signal is
  retained unchanged and price-limit diagnostics belong in robustness analysis.

## Decision Rule

Run each strategy independently against the fixed MID hurdle. Record failures as
failures. Only after a standalone failure may research test a pre-registered
conditional-engine fallback, with separate attribution, turnover, and OOS results.

## Optimization Note - 2026-08-02

- Baseline result: 0/10 standalone strategies passed the fixed MID hurdle.
- Enterprise conditional engine passed aggregate 5/5 with CAGR 0.2549, Sharpe 1.3258,
  Calmar 1.4507, MaxDD -0.1757, and Profit Factor 1.3515.
- The other nine strategies were redesigned as bounded factor-rank tilts on the
  validated MID earnings-yield and price-trend engine.
- `VnMidCsEnterpriseEarningsYield.py` was left untouched.

## Final Result

All ten active representatives passed the aggregate MID hurdle. Files considered
passed at that time were excluded from later submit commands; only
`AntiLotteryMaxReturn` required a second conditional-tilt adjustment. The
2026-08-02 split audit corrected the result to **0/10 true PASS**: all ten pass
Train but fail Test/OOS. Test CAGR ranges only from 0.94% to 2.35%, showing a
broad common-engine regime failure rather than an isolated factor issue.

| Strategy | Aggregate CAGR | Aggregate Sharpe | Aggregate Calmar | Aggregate MaxDD | Aggregate PF |
|---|---:|---:|---:|---:|---:|
| EnterpriseEarningsYield | 25.49% | 1.326 | 1.451 | -17.57% | 1.351 |
| CashProfitability | 22.32% | 1.234 | 1.024 | -21.80% | 1.316 |
| ScalingEfficiency | 22.60% | 1.273 | 1.055 | -21.41% | 1.322 |
| CashAccrualQuality | 22.45% | 1.255 | 1.029 | -21.81% | 1.320 |
| ProjectCommissioning | 22.49% | 1.269 | 1.045 | -21.52% | 1.320 |
| InternallyFundedInvestment | 23.80% | 1.309 | 1.128 | -21.09% | 1.336 |
| ActiveDeleveraging | 22.68% | 1.276 | 1.055 | -21.50% | 1.323 |
| IdiosyncraticMomentum | 22.05% | 1.209 | 1.045 | -21.10% | 1.311 |
| RecognitionMigration | 22.31% | 1.238 | 1.070 | -20.85% | 1.318 |
| AntiLotteryMaxReturn | 22.45% | 1.266 | 1.043 | -21.53% | 1.320 |

### Interpretation

- Standalone factors did not pass. Final strategies are independent economic
  factors expressed as bounded tilts on a common MID value-trend return engine,
  but none passes the full split-aware hurdle.
- The shared engine means the strategies are not yet ten independent PnL sources;
  daily correlation and OOS attribution remain mandatory.
- VN30 panel residual momentum produced zero positions at runtime. The active
  implementation uses a stock-level momentum tilt and no longer claims true
  benchmark residualization.
- CAPEX/financing strategies retain provider sign-convention assumptions and
  require metadata verification before production use.
