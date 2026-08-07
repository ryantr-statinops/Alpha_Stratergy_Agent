# HYPOTHESIS LIBRARY — Economic Hypotheses for Vietnam Stock Market

> Date: 2026-08-05
> Reference: `MASTER_alpha_planning.md` (7-layer architecture)
> Mode: `cross_sectional` (`_panel`, `set_portfolio_positions`)
> Rule: Every ratio must answer "One unit of X creates how much Y?"

---

## How to Use This Library

1. Pick a hypothesis from below
2. Follow Layer 0-6 pipeline in MASTER
3. Run diagnostics (Layer 3) BEFORE backtest
4. Document results in strategy file header

---

## VALUE (H01-H05)

### H01: Book/Market Value

> Companies trading below book value are systematically mispriced.

**Factor:** Value
**Economic Statement:** One unit of market price buys more than one unit of book equity.

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Book/Market | owners_equity / (close * common_shares) | F, A, K | Ratio |
| Book/Per Share | owners_equity / common_shares | F, K | Ratio |

**Validation:** equity > 0, shares > 0, close > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q, non_financial
**Diagnostics (expected):** IC 0.03-0.05, turnover 30-40%
**Vietnam Evidence:** NOT TESTED

---

### H02: Earnings Yield

> Companies with high earnings relative to price earn a premium.

**Factor:** Value
**Economic Statement:** One unit of price buys one unit of earnings power.

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Earnings Yield | EPS / close | D, A | Ratio |
| NI Yield | net_profit / market_value | B, A, K | Ratio |

**Validation:** EPS > 0, close > 0, equity > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q, capital_strength > 0.15
**Diagnostics (expected):** IC 0.04-0.06, turnover 35-45%
**Vietnam Evidence:** EarningsYieldTrend PASS (Sharpe 2.18, 4/5 years)

---

### H03: CFO Yield

> Cash flow is harder to manipulate than earnings; high CFO yield signals mispricing.

**Factor:** Value
**Economic Statement:** One unit of market price buys one unit of operating cash flow.

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| CFO Yield | CFO / market_value | M, A, K | Ratio |

**Validation:** CFO > 0, market_value > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q
**Diagnostics (expected):** IC 0.03-0.05, turnover 30-40%
**Vietnam Evidence:** NOT TESTED

---

### H04: Dividend Yield

> High dividend yield signals value, but only if sustainable.

**Factor:** Value
**Economic Statement:** One unit of price buys one unit of dividend income.

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Dividend Yield | -(dividends_paid) / market_value | O, A, K | Ratio (sign-flip) |

**Validation:** dividends < 0 (panel convention), market_value > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q, dividends_paid > 0
**Diagnostics (expected):** IC 0.02-0.04, turnover 20-30%
**Vietnam Evidence:** NOT TESTED

---

### H05: EV/EBITDA

> Enterprise value relative to operating earnings identifies cheap firms.

**Factor:** Value
**Economic Statement:** One unit of EV buys one unit of EBITDA.

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| EV/EBITDA | enterprise_value / EBITDA | F, A, K, B | Ratio |

**Validation:** EBITDA > 0, EV > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q
**Diagnostics (expected):** IC 0.02-0.04, turnover 30-40%
**Vietnam Evidence:** NOT TESTED

---

## QUALITY (H06-H10)

### H06: Return on Assets

> Firms that generate more profit per unit of assets outperform.

**Factor:** Quality
**Economic Statement:** One unit of assets creates how much net profit?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| ROA | net_profit / total_assets | B, F | Ratio |
| Core ROA | (net_profit + fin_expenses - fin_income) / total_assets | B, C, F | Ratio |

**Validation:** total_assets > 0, equity > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q, non_financial
**Diagnostics (expected):** IC 0.03-0.05, turnover 25-35%
**Vietnam Evidence:** RoaQuality PASS (Sharpe 1.84), RoaImprovement PASS (2.08). MID-CAP: VnMidCsRoaQualityRank FAIL test (post-retrofit, Agg -0.17, Train 0.70 / Test -2.45)

---

### H07: Return on Equity

> Firms that generate more profit per unit of equity outperform.

**Factor:** Quality
**Economic Statement:** One unit of equity creates how much net profit?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| ROE | net_profit / owners_equity | B, F | Ratio |
| Core ROE | (net_profit + fin_expenses - fin_income) / owners_equity | B, C, F | Ratio |

**Validation:** owners_equity > 0, total_assets > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q, non_financial
**Diagnostics (expected):** IC 0.03-0.05, turnover 25-35%
**Vietnam Evidence:** RoeQuality PASS (Sharpe 2.30), RoeImprovement PASS (2.10). MID-CAP: VnMidCsValueQualityComposite FAIL test (post-retrofit, Agg 0.37, Train 1.11 / Test -1.32)

---

### H08: Cash Conversion

> Earnings backed by cash flow are higher quality.

**Factor:** Quality
**Economic Statement:** One unit of net profit converts to how much cash?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Cash Conversion | CFO / net_profit | M, B | Ratio |

**Validation:** net_profit > 0, CFO > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q
**Diagnostics (expected):** IC 0.02-0.04, turnover 25-35%
**Vietnam Evidence:** NOT TESTED. MID-CAP: VnMidCsCashConversionRank FAIL test (post-retrofit, Agg -0.10, Train 0.99 / Test -2.09)

---

### H09: Accrual Quality

> Low accruals indicate earnings backed by cash, not accounting choices.

**Factor:** Quality
**Economic Statement:** How much of net profit is NOT backed by cash?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Accrual | (net_profit - CFO) / total_assets | B, M, F | Ratio |
| Accrual Quality | CFO / net_profit - 1 | M, B | Ratio |

**Validation:** total_assets > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q
**Diagnostics (expected):** IC 0.02-0.04, turnover 30-40%
**Vietnam Evidence:** LowAccruals PASS (Sharpe 1.61). MID-CAP: VnMidCsAccrualQualityRank FAIL test (post-retrofit, Agg -0.10, Train 0.99 / Test -2.09)

---

### H10: Earnings Stability

> Consistent earnings signal durable competitive advantage.

**Factor:** Quality
**Economic Statement:** How stable is the stream of returns on assets?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Earnings Stability | rolling_std(ROA) / abs(rolling_mean(ROA)) | B, F | Stability |

**Validation:** total_assets > 0, rolling_mean(ROA) != 0
**Eligibility:** liquidity rank > 0.30, history >= 8Q (need rolling window)
**Diagnostics (expected):** IC 0.02-0.03, turnover 20-30%
**Vietnam Evidence:** NOT TESTED. MID-CAP: VnMidCsEarningsStabilityRank FAIL test (post-retrofit, Agg 0.22, Train 1.10 / Test -1.76)

---

## GROWTH (H11-H13)

### H11: Revenue Growth

> Growing revenue signals expanding business.

**Factor:** Growth
**Economic Statement:** What is the rate of revenue expansion?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Revenue Growth | revenue(t) / revenue(t-4) - 1 | B | Growth |

**Validation:** revenue(t-4) > 0
**Eligibility:** liquidity rank > 0.30, history >= 8Q
**Diagnostics (expected):** IC 0.01-0.03, turnover 40-50%
**Vietnam Evidence:** NOT TESTED

---

### H12: EPS Growth

> Growing earnings signal improving business quality.

**Factor:** Growth
**Economic Statement:** What is the rate of earnings expansion?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| EPS Growth | eps(t) / eps(t-4) - 1 | D | Growth |

**Validation:** eps(t-4) > 0
**Eligibility:** liquidity rank > 0.30, history >= 8Q
**Diagnostics (expected):** IC 0.02-0.04, turnover 40-50%
**Vietnam Evidence:** NOT TESTED

---

### H13: Conservative Asset Growth

> Firms that grow assets conservatively outperform aggressive growers.

**Factor:** Growth
**Economic Statement:** Excessive asset growth destroys value.

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Asset Growth | total_assets(t) / total_assets(t-4) - 1 | F | Growth |

**Validation:** total_assets(t-4) > 0
**Eligibility:** liquidity rank > 0.30, history >= 8Q
**Diagnostics (expected):** IC -0.02 to -0.04 (negative = conservative wins), turnover 30-40%
**Vietnam Evidence:** ConservativeAssetGrowth PASS (Sharpe 2.09). MID-CAP: VnMidCsConservativeGrowth FAIL test (post-retrofit, Agg 0.11, Train 1.06 / Test -2.11)

---

## MOMENTUM (H14-H16)

### H14: Price Trend

> Stocks above their moving average continue to outperform.

**Factor:** Momentum
**Economic Statement:** How far is price from its trend?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Price/EMA | close / ema(close, 20) | A | Trend |
| Trend Strength | (close / ema(close, 20))^12 | A | Trend + Power |

**Validation:** close > 0, ema > 0
**Eligibility:** liquidity rank > 0.40, history >= 20 days
**Diagnostics (expected):** IC 0.04-0.07, turnover 40-60%
**Vietnam Evidence:** ValueTrendP02-P11 PASS (Sharpe 2.31-2.67, 5/5 years). MID-CAP: VnMidCsMomentumValue FAIL test (post-retrofit, Agg 0.25, Train 0.75 / Test -0.96)

---

### H15: ROE Improvement

> Firms with improving ROE signal operational turnaround.

**Factor:** Momentum
**Economic Statement:** Is profitability accelerating or decelerating?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| ROE Improvement | delta(rolling_mean(ROE, 4)) | B, F | Delta + Rolling |

**Validation:** total_assets > 0, equity > 0
**Eligibility:** liquidity rank > 0.30, history >= 8Q
**Diagnostics (expected):** IC 0.02-0.04, turnover 35-45%
**Vietnam Evidence:** RoeImprovement PASS (Sharpe 2.10), ProfitAcceleration PASS (2.11). MID-CAP: VnMidCsRoeImprovementRank FAIL test (post-retrofit, Agg 0.06, Train 0.89 / Test -2.07)

---

### H16: Earnings Acceleration

> Accelerating earnings signal strengthening business.

**Factor:** Momentum
**Economic Statement:** Is the rate of earnings change itself increasing?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| EPS Acceleration | delta(delta(EPS)) | D | Acceleration |

**Validation:** eps(t-8) > 0
**Eligibility:** liquidity rank > 0.30, history >= 8Q
**Diagnostics (expected):** IC 0.02-0.04, turnover 40-50%
**Vietnam Evidence:** EpsSurpriseDrift PASS (Sharpe 2.09)

---

## LEVERAGE (H17-H19)

### H17: Low Leverage

> Conservatively financed firms outperform.

**Factor:** Leverage
**Economic Statement:** How much debt backs each unit of assets?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Debt/Assets | liabilities / total_assets | F | Ratio |
| Debt/Equity | liabilities / owners_equity | F | Ratio |

**Validation:** total_assets > 0, owners_equity > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q
**Diagnostics (expected):** IC -0.02 to -0.04 (negative = low leverage wins), turnover 25-35%
**Vietnam Evidence:** LowLeverage PASS (Sharpe 1.64). MID-CAP: VnMidCsLowLeverageRank FAIL test (post-retrofit, Agg 0.32, Train 1.38 / Test -2.14)

---

### H18: Net Debt

> Firms with net cash (low net debt) outperform.

**Factor:** Leverage
**Economic Statement:** After paying all debt with cash, what is left?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Net Debt/Assets | (total_debt - cash) / total_assets | F, G | Spread + Ratio |
| Net Cash Position | cash / total_assets | G, F | Ratio |

**Validation:** total_assets > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q
**Diagnostics (expected):** IC 0.02-0.04, turnover 25-35%
**Vietnam Evidence:** NetCash PASS (Sharpe 1.90). MID-CAP: VnMidCsNetCashRank FAIL test (post-retrofit, Agg 0.16, Train 1.02 / Test -1.69)

---

### H19: Interest Coverage

> Firms that easily cover interest expenses are lower risk.

**Factor:** Leverage
**Economic Statement:** One unit of interest expense is covered by how much profit?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Interest Coverage | PBT / interest_expenses | B, C | Ratio |

**Validation:** interest_expenses > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q
**Diagnostics (expected):** IC 0.02-0.03, turnover 25-35%
**Vietnam Evidence:** NOT TESTED

---

## LIQUIDITY (H20-H22)

### H20: Current Ratio

> Liquid firms are less likely to face distress.

**Factor:** Liquidity
**Economic Statement:** One unit of current liability is covered by how much current asset?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Current Ratio | current_assets / current_liabilities | G | Ratio |

**Validation:** current_liabilities > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q
**Diagnostics (expected):** IC 0.01-0.03, turnover 25-35%
**Vietnam Evidence:** CurrentLiquidity PASS (Sharpe 1.81). MID-CAP: VnMidCsCurrentLiquidityRank FAIL test (post-retrofit, Agg -0.37, Train 0.21 / Test -2.11)

---

### H21: Cash/Assets

> Cash-rich firms have optionality and safety.

**Factor:** Liquidity
**Economic Statement:** What fraction of assets is liquid cash?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Cash/Assets | cash / total_assets | G, F | Ratio |

**Validation:** total_assets > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q
**Diagnostics (expected):** IC 0.01-0.03, turnover 25-35%
**Vietnam Evidence:** NOT TESTED

---

### H22: Working Capital Burden

> Lean working capital signals operational efficiency.

**Factor:** Liquidity
**Economic Statement:** How much capital is locked in operations?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| WC/Assets | (receivables + inventories - payables) / total_assets | H, F | Ratio |
| WC Burden | WC/Assets > 0.30 | H, F | Ratio + Gate |

**Validation:** total_assets > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q
**Diagnostics (expected):** IC -0.02 to -0.04 (negative = lean WC wins), turnover 25-35%
**Vietnam Evidence:** LeanWorkingCapital PASS (Sharpe 2.32)

---

## EFFICIENCY (H23-H25)

### H23: Asset Turnover

> Firms that generate more revenue per asset are efficient.

**Factor:** Efficiency
**Economic Statement:** One unit of assets creates how much revenue?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Asset Turnover | revenue / total_assets | B, F | Ratio |

**Validation:** total_assets > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q
**Diagnostics (expected):** IC 0.02-0.03, turnover 30-40%
**Vietnam Evidence:** NOT TESTED

---

### H24: Inventory Days

> Low inventory days signal efficient operations.

**Factor:** Efficiency
**Economic Statement:** How many days of inventory to support one unit of revenue?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Inventory Days | (inventory / revenue) * 365 | H, B | Ratio |

**Validation:** revenue > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q
**Diagnostics (expected):** IC -0.01 to -0.03 (negative = fewer days wins), turnover 30-40%
**Vietnam Evidence:** InventoryDeterioration PASS (Sharpe 2.08)

---

### H25: Receivable Days

> Low receivable days signal efficient collection.

**Factor:** Efficiency
**Economic Statement:** How many days to collect one unit of revenue?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Receivable Days | (receivables / revenue) * 365 | H, B | Ratio |

**Validation:** revenue > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q
**Diagnostics (expected):** IC -0.01 to -0.03 (negative = fewer days wins), turnover 30-40%
**Vietnam Evidence:** ReceivablesDeterioration PASS (Sharpe 2.02)

---

## CAPITAL ALLOCATION (H26-H28)

### H26: Net Payout Yield

> Firms returning capital to shareholders outperform.

**Factor:** Capital Allocation
**Economic Statement:** One unit of market value returns how much cash to shareholders?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Net Payout Yield | (-(div) - (repurchase) - issuance) / market_value | O, A, K | Ratio |
| Persistent Payout | ema(net_payout_yield) | O, A, K | Trend |

**Validation:** dividends < 0, shares > 0, market_value > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q, dividends_paid > 0
**Diagnostics (expected):** IC 0.04-0.06, turnover 30-40%
**Vietnam Evidence:** NetPayoutPersistence PASS (Sharpe 1.31-1.65), NetPayoutMomentum PASS (2.20)

---

### H27: Buyback Yield

> Share repurchases signal management confidence.

**Factor:** Capital Allocation
**Economic Statement:** One unit of market value is being repurchased?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Buyback Yield | -(repurchases) / market_value | O, A, K | Ratio (sign-flip) |

**Validation:** market_value > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q
**Diagnostics (expected):** IC 0.02-0.04, turnover 25-35%
**Vietnam Evidence:** NOT TESTED (limited buyback market in Vietnam)

---

### H28: Capex Discipline

> Disciplined capital expenditure signals management quality.

**Factor:** Capital Allocation
**Economic Statement:** How much of operating cash flow is reinvested?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Capex/CFO | capex / CFO | N, M | Ratio |
| Capex/Depreciation | capex / depreciation | N, M | Ratio |

**Validation:** CFO > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q
**Diagnostics (expected):** IC 0.01-0.03, turnover 30-40%
**Vietnam Evidence:** ProductiveReinvestment PASS (Sharpe 1.79)

---

## OPERATING QUALITY (H29-H31)

### H29: Margin Stability

> Stable margins signal competitive moat.

**Factor:** Operating Quality
**Economic Statement:** How consistent are operating margins over time?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Margin Stability | rolling_std(margin, 8) / abs(rolling_mean(margin, 8)) | B, C | Stability |

**Validation:** rolling_mean(margin) != 0
**Eligibility:** liquidity rank > 0.30, history >= 8Q
**Diagnostics (expected):** IC -0.01 to -0.03 (negative = stable wins), turnover 25-35%
**Vietnam Evidence:** NOT TESTED

---

### H30: Fixed Asset Utilization

> High asset utilization signals efficient operations.

**Factor:** Operating Quality
**Economic Statement:** One unit of fixed assets creates how much revenue?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| FA Utilization | revenue / tangible_fixed_assets | B, I | Ratio |

**Validation:** tangible_fixed_assets > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q
**Diagnostics (expected):** IC 0.02-0.03, turnover 30-40%
**Vietnam Evidence:** NOT TESTED

---

### H31: SG&A Efficiency

> Low SG&A relative to revenue signals cost discipline.

**Factor:** Operating Quality
**Economic Statement:** One unit of revenue costs how much in SG&A?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| SG&A/Revenue | (selling + GAE) / revenue | C, B | Ratio |

**Validation:** revenue > 0
**Eligibility:** liquidity rank > 0.30, history >= 4Q
**Diagnostics (expected):** IC -0.01 to -0.03 (negative = efficient wins), turnover 30-40%
**Vietnam Evidence:** NOT TESTED

---

## RISK (H32-H33)

### H32: Low Volatility

> Low volatility stocks earn superior risk-adjusted returns.

**Factor:** Risk
**Economic Statement:** How much does price fluctuate?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Volatility | rolling_std(returns, 60) | A | Rolling |
| Downside Vol | rolling_std(returns[returns < 0]) | A | Rolling |

**Validation:** returns available
**Eligibility:** liquidity rank > 0.40, history >= 60 days
**Diagnostics (expected):** IC -0.02 to -0.04 (negative = low vol wins), turnover 20-30%
**Vietnam Evidence:** LowVolatility PASS (Sharpe 2.20), LowAmihud PASS (2.14)

---

### H33: Beta

> Low beta stocks outperform on risk-adjusted basis.

**Factor:** Risk
**Economic Statement:** How much does the stock move with the market?

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Beta | covariance(r, r_market) / var(r_market) | A | Rolling + Statistical |

**Validation:** market returns available
**Eligibility:** liquidity rank > 0.40, history >= 60 days
**Diagnostics (expected):** IC -0.01 to -0.03 (negative = low beta wins), turnover 25-35%
**Vietnam Evidence:** NOT TESTED

---

## COMPOSITE HYPOTHESES (H34-H36)

> These combine multiple factors into a single alpha.

### H34: Quality + Value

> High-quality firms at cheap prices are the best investment.

**Factor:** Quality + Value
**Economic Statement:** One unit of quality-adjusted price creates superior returns.

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Composite | 0.5 * z(quality_score) + 0.5 * z(value_score) | Multi | Composite |

**Validation:** All individual factor validations apply
**Eligibility:** Combined eligibility from both factors
**Diagnostics (expected):** IC 0.05-0.08, turnover 30-40%, Sharpe 1.5-2.0
**Vietnam Evidence:** ValueMomentumComposite PASS (Sharpe 2.20)

---

### H35: Value + Momentum

> Cheap stocks with positive momentum outperform.

**Factor:** Value + Momentum
**Economic Statement:** Price trend confirms value thesis.

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Composite | 0.5 * z(value_score) + 0.5 * z(momentum_score) | Multi | Composite |

**Validation:** All individual factor validations apply
**Eligibility:** Combined eligibility from both factors
**Diagnostics (expected):** IC 0.05-0.07, turnover 35-45%
**Vietnam Evidence:** ValueTrendP02-P11 PASS (Sharpe 2.31-2.67)

---

### H36: Triple Composite (Quality + Value + Momentum)

> The three-factor approach: quality confirms, value buys, momentum timing.

**Factor:** Quality + Value + Momentum
**Economic Statement:** Three independent factors provide maximum diversification.

| Ratio | Formula | Fields | Transform |
|---|---|---|---|
| Composite | 0.4 * z(Q) + 0.3 * z(V) + 0.3 * z(M) | Multi | Composite |

**Validation:** All individual factor validations apply
**Eligibility:** Combined eligibility from all three factors
**Diagnostics (expected):** IC 0.06-0.09, turnover 35-45%, Sharpe 1.8-2.5
**Vietnam Evidence:** QualityMomentum PASS (Sharpe 1.77)

---

## Summary: Hypothesis Count by Factor

| Factor | Count | ID Range | Vietnam PASS |
|---|---|---|---|
| Value | 5 | H01-H05 | 1 (H02) |
| Quality | 5 | H06-H10 | 4 (H06, H07, H09) |
| Growth | 3 | H11-H13 | 1 (H13) |
| Momentum | 3 | H14-H16 | 3 (H14, H15, H16) |
| Leverage | 3 | H17-H19 | 2 (H17, H18) |
| Liquidity | 3 | H20-H22 | 2 (H20, H22) |
| Efficiency | 3 | H23-H25 | 2 (H24, H25) |
| Capital Allocation | 3 | H26-H28 | 3 (H26, H28) |
| Operating Quality | 3 | H29-H31 | 0 |
| Risk | 2 | H32-H33 | 2 (H32) |
| Composite | 3 | H34-H36 | 3 (H34, H35, H36) |
| **Total** | **36** | **H01-H36** | **21 PASS** |

---

## Priority Ranking (Vietnam-specific)

Based on Gate 1-3 evidence:

| Priority | Hypothesis | Factor | Evidence |
|---|---|---|---|
| P0 | H14: Price Trend | Momentum | ValueTrend PASS (Sharpe 2.67) |
| P0 | H07: ROE | Quality | RoeQuality PASS (Sharpe 2.30) |
| P0 | H22: WC Burden | Liquidity | LeanWC PASS (Sharpe 2.32) |
| P0 | H35: Value+Momentum | Composite | ValueTrendComposite PASS (2.20) |
| P1 | H02: Earnings Yield | Value | EarningsYieldTrend PASS (2.18) |
| P1 | H15: ROE Improvement | Momentum | RoeImprovement PASS (2.10) |
| P1 | H13: Conservative Growth | Growth | ConservativeGrowth PASS (2.09) |
| P1 | H16: EPS Acceleration | Momentum | EpsSurpriseDrift PASS (2.09) |
| P1 | H26: Net Payout | Capital Allocation | NetPayoutPersistence PASS (1.65) |
| P1 | H32: Low Volatility | Risk | LowVolatility PASS (2.20) |
| P2 | H06: ROA | Quality | RoaQuality PASS (1.84) |
| P2 | H18: Net Debt | Leverage | NetCash PASS (1.90) |
| P2 | H20: Current Ratio | Liquidity | CurrentLiquidity PASS (1.81) |
| P2 | H24: Inventory Days | Efficiency | InventoryDeterioration PASS (2.08) |
| P2 | H25: Receivable Days | Efficiency | ReceivablesDeterioration PASS (2.02) |
| P2 | H28: Capex Discipline | Capital Allocation | ProductiveReinvestment PASS (1.79) |
| P2 | H34: Quality+Value | Composite | ValueMomentumComposite PASS (2.20) |
| P3 | H36: Triple Composite | Composite | QualityMomentum PASS (1.77) |
| P3 | H17: Low Leverage | Leverage | LowLeverage PASS (1.64) |
| P3 | H09: Accrual Quality | Quality | LowAccruals PASS (1.61) |
| P4 | H01, H03-H05, H08, H10-H12, H19, H21, H23, H27, H29-H31, H33 | Various | NOT TESTED |

---

## Universe Status (2026-08-07)

> Evidence lines above carry MID-CAP numbers from the 11-file VnMidCs* batch post-retrofit (2026-08-07 16:44-16:48, self-baseline + trend vote + demean_l1).

- **SMALL-CAP:** 4 alphas PASS Gate 1-3 (FinancialNetPayout, NetPayoutPersistence, RoaQuality, ValueTrendP02); blocker = CAGR magnitude.
- **LARGE-CAP:** 0/40 annual + 0/4 quarterly pass; CS saturated ~0.9, best TS CapexDiscipline 1.13 (Train 1.36 / Test 0.66).
- **MID-CAP:** 0 PASS across 13 TS + 20 TS + 20 CS + 11 post-retrofit CS; all Test Sharpe negative (common-engine regime failure, no OOS edge).
