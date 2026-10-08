# MASTER: VN-LARGE-CAP Alpha Universe — Time-Series + Cross-Sectional

> **Session:** 2026-08-04
> **Trạng thái:** Master plan — tổng hợp toàn bộ alpha ideas cho VN-LARGE-CAP
> **Mục đích:** Quản lý unified universe, tránh duplicate, track implementation status
> **Split:** Train 2020–2022, Test OOS 2023–2024
> **Target:** Sharpe≥1.2, CAGR≥15%, MaxDD≥-35%, PF≥1.2, Calmar≥1.1

---

## 0. Kết luận từ kết quả thực tế

### What works

| Pattern | Best performer | Sharpe | Tại sao |
|---|---|---|---|
| **CFO funds CAPEX + trend** | CapexDisciplineTrend | 1.13 | Capital discipline = firm self-funds growth |
| **CFO + NP agreement + trend** | QualityTrendAgreement | 1.00 | Dual quality confirmation |
| **ROA + trend** | RoaTrend | 1.10 | Profitability quality |
| **MACD + trend** | MacdTrend | 1.07 | Momentum confirmation |
| **Profit report momentum** | ProfitReportMomentum | 1.07 | PEAD effect |
| **PreWCCash residual** | PreWcCashStrength (CS) | 0.91 | Cash quality orthogonal to earnings |

### What doesn't work

| Pattern | Root cause | Example |
|---|---|---|
| **Cross-sectional value/quality cap** | Bão hòa ~0.9 Sharpe, beta lấn át | Q04 0.91, V06 0.82 — ceiling |
| **Composite same-family** | Correlation quá cao, không diversify | Q04+V06 = 0.91 ≈ Q04 đơn lẻ |
| **Noise-filter trước rank_demean_l1** | Rank tự loại transformation | Winsorize/Rank = no-op |
| **Over-constrained entry** | Quá nhiều guard → reduced trades | PullbackMeanReversion, BollingerSqueeze |
| **Feature sparse (annual)** | CFO/earnings sparse → 0 trades | CashInterestCoverage, DeleveragingTrend |

### Key insight

**Edge = Thesis quality (70%) + Structural integrity (20%) + Parameter (10%)**

Capex family hoạt động tốt nhất vì thesis "capital discipline" có edge thực sự — không phải do parameter hay构造方法.

---

## I. TIME-SERIES STRATEGIES (Long-Only, Self-Deciding)

### A. Implemented & Submitted

| # | Strategy | Sharpe | Thesis | Status |
|---:|---|---:|---|---|
| T01 | VnLargeCapexDisciplineTrend | 1.13 | CFO funds CAPEX, trend confirms | ✅ Agg 1.13, Train 1.36 → Test 0.66 |
| T02 | VnLargeCapex1442 | 1.12 | Same as T01, EMA 14/42 | ✅ Agg 1.12 |
| T03 | VnLargeCapexProfitGuard | 1.11 | CFO+NP+CAPEX discipline | ✅ Agg 1.11 |
| T04 | VnLargeRoaTrend | 1.10 | ROA > 0 + trend | ✅ Agg 1.10 |
| T05 | VnLargeMacdTrend | 1.07 | MACD signal + EMA trend | ✅ Agg 1.07 |
| T06 | VnLargeProfitReportMomentum | 1.07 | NP q/q increase + trend | ✅ Agg 1.07 |
| T07 | VnLargeQualityTrendAgreement | 1.00 | CFO>0 + NP>0 + dual EMA | ✅ Agg 1.00, stable train/test |
| T08 | VnLargeDualTrend | 1.03 | EMA8/24 + EMA12/36 agreement | ✅ Agg 1.03 |
| T09 | VnLargeCapex1854 | 0.99 | CAPEX discipline, EMA 18/54 | ✅ Agg 0.99 |
| T10 | VnLargeAgreement1442 | 0.74 | Quality agreement, EMA 14/42 | ✅ slower = worse |
| T11 | VnLargeAgreement1854 | 0.93 | Quality agreement, EMA 18/54 | ✅ Agg 0.93 |
| T12 | VnLargeAgreementHysteresis | 0.91 | Quality + deadband | ✅ Agg 0.91 |
| T13 | VnLargeAgreementConversion | 0.98 | Quality + CFO/NP > 0.5 | ✅ Agg 0.98 |
| T14 | VnLargeCapexDeadband | 0.88 | CAPEX + deadband | ✅ Agg 0.88 |
| T15 | VnLargeCapex3090 | 0.93 | CAPEX, EMA 30/90 | ✅ too slow |
| T16 | VnLargeRsiRecoveryTrend | 0.97 | RSI7 recovery + trend | ✅ batch10 |
| T17 | VnLargeCciTrend | 0.99 | CCI + trend | ✅ batch10 |
| T18 | VnLargeAdxStrongTrend | 0.95 | ADX>25 + trend | ✅ batch10 |
| T19 | VnLargeObvTrendConfirm | 0.96 | OBV trend + price trend | ✅ batch10 |
| T20 | VnLargeMfiDivergence | 1.01 | MFI divergence + trend | ✅ batch10, best batch10 |
| T21 | VnLargeStochRecovery | 0.94 | Stoch recovery + trend | ✅ batch10 |
| T22 | VnLargeTrixMomentum | 0.95 | TRIX momentum + trend | ✅ batch10 |
| T23 | VnLargeWillrBounce | 0.93 | Williams %R bounce + trend | ✅ batch10 |
| T24 | VnLargePullbackMeanReversion | 0.56 | Pullback + RSI + mean reversion | ✅ too constrained |
| T25 | VnLargeBollingerSqueezeBreakout | 0.03 | BB squeeze + breakout | ✅ no edge large-cap |

### B. Not Yet Implemented — High Priority (from Master_Large_Cap)

#### B1. Cash Flow Family (extend Capex success)

| # | Idea ID | Name | Thesis | Expected edge |
|---:|---|---|---|---|
| T26 | I22 | InternallyFundedCapexTrend | CFO covers capex + no external financing + trend | Capital self-sufficiency |
| T27 | I23 | LaggedCapexPayoffTrend | Past capex → current CFO improvement + trend | Investment realization |
| T28 | Q03 | CashEarningsSpreadTrend | (CFO-PAT)/Assets positive + trend | Cash quality > accrual |
| T29 | Q04 | PreWcCashTrend | PreWCCash/Assets > PAT/Assets + trend | Operating cash strength |
| T30 | V07 | OcfYieldTrend | CFO/MV high + trend | Cash value |

#### B2. Balance Sheet Family

| # | Idea ID | Name | Thesis | Expected edge |
|---:|---|---|---|---|
| T31 | B16 | NetLiquidAssetTrend | (LiquidAssets-Debt)/Assets high + trend | Financial buffer |
| T32 | B17 | InterestCoverageTrend | CFO/interest_paid improving + trend | Debt service improvement |
| T33 | B19 | CapitalRatioTrend | Equity/Assets high + trend | Shock absorber |
| T34 | B20 | EarnedCapitalTrend | Retained earnings / contributed capital + trend | Lifecycle quality |

#### B3. Payout Family

| # | Idea ID | Name | Thesis | Expected edge |
|---:|---|---|---|---|
| T35 | P12 | NetPayoutTrend | Persistent net payout yield + trend | Shareholder return |
| T36 | P13 | ShareholderYieldTrend | Dividends + buybacks + debt paydown + trend | Total return to holders |
| T37 | P15 | AntiDilutionTrend | No share issuance + trend | Per-share protection |

#### B4. Event Family

| # | Idea ID | Name | Thesis | Expected edge |
|---:|---|---|---|---|
| T38 | E27 | CashConfirmedPatSurprise | PAT surprise + CFO confirmation + trend | Filtered PEAD |
| T39 | E28 | CfoSurpriseTrend | CFO q/q surprise + hold 20-60 days | Cash flow PEAD |
| T40 | E29 | CashConversionInflection | (CFO-PAT)/Assets improving + trend | Quality inflection |

#### B5. Momentum/Residual Family (for low correlation)

| # | Idea ID | Name | Thesis | Expected edge |
|---:|---|---|---|---|
| T41 | M31 | ResidualMomentumTrend | VN30-residual momentum + trend | Factor-removed momentum |
| T42 | M32 | ResidualReversal | Short-term residual reversal + quality | Contrarian + quality |
| T43 | M33 | Residual52HighAnchoring | Distance from residual 52-week high | Behavioral anchor |

#### B6. Downside Defense Family

| # | Idea ID | Name | Thesis | Expected edge |
|---:|---|---|---|---|
| T44 | D36 | DownsideBetaImprovement | Declining downside beta + trend | Becoming defensive |
| T45 | D38 | LowResidualVolTrend | Low residual vol + trend | Idiosyncratic safety |
| T46 | D40 | DrawdownRecoveryTrend | Fast recovery from drawdown + quality | Resilience |

#### B7. Flow/Pressure Family

| # | Idea ID | Name | Thesis | Expected edge |
|---:|---|---|---|---|
| T47 | F41 | AbnormalVolumeTrend | Volume spike + same-sign return + trend | Attention continuation |
| T48 | F43 | IndexPressureReversal | Abnormal volume + return → contrarian | Flow reversal |

#### B8. Value-Trend Combination

| # | Idea ID | Name | Thesis | Expected edge |
|---:|---|---|---|---|
| T49 | V06+T | EarningsYieldTrend | EPS>0 + positive EY + trend | Value + trend |
| T50 | V08+T | FcfYieldTrend | FCF/MV high + trend | Cash value + trend |

### C. Novel Ideas (from analysis, not in Master)

| # | Name | Thesis | Expected edge |
|---:|---|---|---|
| T51 | CashFlowAcceleration | CFO growth acceleration + trend | Improving cash generation |
| T52 | EarningsQualityShift | EPS growth + CFO growth alignment | Quality regime change |
| T53 | CapitalEfficiencyTrend | ROA improvement + low capex intensity | Efficient growth |
| T54 | DefensiveQualityTrend | Low beta + high ROE + trend | Quality defensiveness |
| T55 | CashFlowBreakout | CFO new high + price breakout | Fundamental + technical |

---

## II. CROSS-SECTIONAL STRATEGIES (Market-Neutral)

### A. Implemented & Submitted

| # | Strategy | Sharpe | Thesis | Status |
|---:|---|---:|---|---|
| C01 | VnLargeCsPreWcCashStrength | 0.91 | Q04 PreWCCash residual spread | ✅ best CS, stable |
| C02 | VnLargeCsEarningsYield | 0.82 | V06 EPS/close value control | ✅ stable |
| C03 | VnLargeCsEarningsMagnitude | 0.84 | V06 demean_l1 magnitude | ✅ |
| C04 | VnLargeCsCompositeMagnitude | 0.88 | Q04+V06 composite | ✅ ≈ Q04 alone |
| C05 | VnLargeCsCashEarningsMagnitude | 0.63 | Q03 demean_l1 | ✅ improved from base |
| C06 | VnLargeCsPreWcMagnitude | 0.63 | Q04 demean_l1 | ✅ worse than rank |
| C07 | VnLargeCsCashEarningsSpread | 0.35 | Q03 CFO-PAT spread | ✅ weak |
| C08 | VnLargeCsOcfYield | 0.20 | V07 CFO/MV | ✅ weak |
| C09 | VnLargeCsResidualFcfYield | 0.19 | V08 FCF/MV | ✅ weak |
| C10 | VnLargeCsEvAdjustedCashYield | 0.25 | V09 enterprise yield | ✅ weak |
| C11 | VnLargeCsPersistentCashRoa | -0.22 | Q01 cash ROA | ❌ negative |
| C12 | VnLargeCsStableCashProfitability | -0.22 | Q02 stable cash | ❌ degenerate ≡ Q01 |
| C13 | VnLargeCsMultiYearFcfConsistency | 0.00 | Q05 FCF consistency | ❌ 0 trades |
| C14 | VnLargeCsResidualTangibleBook | -0.43 | V10 tangible book | ❌ overfit |
| C15 | VnLargeCsPreWcRanked | 0.91 | Q04 rank filter | ✅ ≡ Q04 (no-op) |
| C16 | VnLargeCsPreWcWinsorized | 0.91 | Q04 winsorize filter | ✅ ≡ Q04 (no-op) |
| C17 | VnLargeCsPreWcRankedWinsorized | 0.91 | Q04 rank+winsorize | ✅ ≡ Q04 (no-op) |
| C18 | VnLargeCsCashEarningsWinsorized | 0.35 | Q03 winsorize | ✅ ≡ Q03 (no-op) |
| C19 | VnLargeCsEarningsWinsorized | 0.82 | V06 winsorize | ✅ ≡ V06 (no-op) |
| C20 | VnLargeCsEarningsRanked | 0.82 | V06 rank filter | ✅ ≡ V06 (no-op) |
| C21 | VnLargeCsCashValueComposite | 0.91 | Q04+V06 blend | ✅ ≈ Q04 |

### B. Not Yet Implemented — CS

| # | Idea ID | Name | Thesis | Expected edge |
|---:|---|---|---|---|
| C22 | P12 | CsNetPayoutYield | Net payout yield cross-section | Shareholder return |
| C23 | P13 | CsShareholderYield | Total shareholder yield | Cash distribution |
| C24 | B16 | CsNetLiquidBuffer | Liquid assets - debt / assets | Financial safety |
| C25 | B19 | CsCapitalRatio | Equity/assets cross-section | Balance strength |
| C26 | I21 | CsAssetGrowthNeutral | Asset growth residualized vs cash quality | Overinvestment signal |
| C27 | M31 | CsResidualMomentum | VN30-residual momentum rank | Factor-removed momentum |
| C28 | D38 | CsLowResidualVol | Low residual volatility | Idiosyncratic safety |
| C29 | F41 | CsAbnormalVolume | Volume continuation cross-section | Attention factor |
| C30 | E27 | CsCashConfirmedSurprise | Cash-confirmed earnings surprise | Filtered PEAD |

---

## III. DEFENSE 2022 VARIANTS (Wave 2)

| # | Strategy | Baseline | Agg | Train | Test | Status |
|---:|---|---|---:|---:|---:|---|
| D01 | Agreement1442 | QTA | 0.74 | 0.71 | 0.80 | ❌ degrade |
| D02 | Agreement1854 | QTA | 0.93 | 0.99 | 0.84 | ❌ test worse |
| D03 | AgreementFullExit | QTA | 1.00 | 1.06 | 1.02 | ❌ degenerate |
| D04 | AgreementConversion | QTA | 0.98 | 0.88 | 1.21 | ❌ train degrade |
| D05 | AgreementHysteresis | QTA | 0.91 | 0.89 | 0.95 | ❌ |
| D06 | Capex1442 | CDT | 1.12 | 1.32 | 0.61 | ❌ test worse |
| D07 | Capex1854 | CDT | 0.99 | 1.12 | 0.62 | ❌ |
| D08 | Capex3090 | CDT | 0.93 | 0.93 | 0.91 | ❌ train degrade |
| D09 | CapexDeadband | CDT | 0.88 | 0.95 | 0.74 | ❌ |
| D10 | CapexProfitGuard | CDT | 1.11 | 1.31 | 0.72 | ❌ close but no |

**Kết luận:** Slow EMA không improve 2022 defense. Nguồn lợi nhuận nằm ở fast re-entry, không phải hold-through.

---

## IV. DEGENERATE/NO-OP TRACKER

| Case | Cause | Lesson |
|---|---|---|
| Q01 ≡ Q02 | Same `ema_panel(CFO/Assets)` — no std leg | Different construction needed |
| AgreementFullExit ≡ QTA | `close < EMA36` redundant with fast break | Verify each exit leg independently |
| Winsorize/Rank = no-op | `rank_demean_l1` re-ranks internally | Use `demean_l1` for magnitude |
| 0-trade strategies | Over-constrained entry (4+ conditions) | Max 3 entry conditions |

---

## V. IMPLEMENTATION PRIORITY

### Phase 1: Extend Capex Success (highest expected ROI)

| # | Idea | Why |
|---:|---|---|
| T26 | InternallyFundedCapexTrend | Same thesis family as T01-T03 (proven) |
| T27 | LaggedCapexPayoffTrend | Cash-realized investment payoff |
| T28 | CashEarningsSpreadTrend | Cash quality, different angle |
| T29 | PreWcCashTrend | CS candidate 0.91 → TS could be higher |
| T51 | CashFlowAcceleration | CFO growth momentum |

### Phase 2: Fundamental Event (PEAD family)

| # | Idea | Why |
|---:|---|---|
| T38 | CashConfirmedPatSurprise | Filtered PEAD — proven in mid-cap |
| T39 | CfoSurpriseTrend | Cash flow PEAD — less crowded |
| T40 | CashConversionInflection | Quality regime change |

### Phase 3: Residual/Flow (low correlation)

| # | Idea | Why |
|---:|---|---|
| T41 | ResidualMomentumTrend | Literature-backed, low corr prior |
| T47 | AbnormalVolumeTrend | Attention/flow signal |
| T48 | IndexPressureReversal | Short-horizon contrarian |

### Phase 4: Balance Sheet + Payout

| # | Idea | Why |
|---:|---|---|
| T31 | NetLiquidAssetTrend | Defensive quality |
| T35 | NetPayoutTrend | Payout factor (literature strong) |
| T33 | CapitalRatioTrend | Balance strength |

---

## VI. EVALUATION STACK

### PASS criteria

| Metric | Threshold | Notes |
|---|---|---|
| Aggregate Sharpe | ≥ 1.2 | Primary gate |
| CAGR | ≥ 15% | Return target |
| MaxDD | ≥ -35% | Risk limit |
| Profit Factor | ≥ 1.2 | Win/loss ratio |
| Calmar | ≥ 1.1 | Return/drawdown |

### Stability checks

- Train Sharpe not degrade > 15% vs baseline
- Test Sharpe not degrade > 30% vs Train
- 2022 MaxDD ≤ baseline MaxDD (defense requirement)
- No single year contributing > 50% of total return

### Correlation gates (for portfolio construction)

| Gate | Target |
|---|---|
| vs each small/mid incumbent | |corr| ≤ 0.30 |
| Ultra-low target | |corr| ≤ 0.20 |
| Downside correlation | ≤ 0.30 |
| Co-loss probability | Bottom decile co-occurrence |

---

## VII. NEXT STEPS

1. **Phase 1 implementation:** Write 5 TS strategies (T26-T30) based on Capex family pattern
2. **Quick screen:** Validate all 5 → submit live
3. **Phase 2:** Event family (T38-T40)
4. **Phase 3:** Residual/flow (T41, T47-T48)
5. **Phase 4:** Balance sheet (T31, T33, T35)
6. **Portfolio construction:** Once >5 strategies pass, build diversified portfolio with correlation gates

---

*Master plan — updated 2026-08-04*
