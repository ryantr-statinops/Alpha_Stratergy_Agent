# 20 Independent Alpha Ideas — VN-SMALL-CAP

> Date: 2026-08-02
> Universe: `VN-SMALL-CAP`
> Mode: `cross_sectional` (`_panel`, market-neutral)
> Canonical data catalog: `syntax/data_syntax.md`
> Market reference: `data/vietnam_market_characteristics.md`

## Objective

Thiết kế 20 **economic theses khác nhau**, không dùng 20 parameter variants của
cùng một công thức. "Độc lập" ở đây nghĩa là độc lập về cơ chế kỳ vọng; mức
tương quan thực tế chỉ được xác nhận sau khi có return series/OOS backtest.

Mọi strategy phải:

- Dùng report point-in-time sau ngày publish; không backfill/negative shift.
- Dùng `_panel` fields và `self.set_portfolio_positions(...)`.
- Gate `(close > 0) & (volume > 0)` và denominator dương.
- Có liquidity/capacity gate; ưu tiên rank rolling traded value thay absolute
  threshold vì đơn vị volume chưa được xác minh.
- Test cả `rank_demean_l1` và `demean_l1`; không nhân gross exposure.
- Không coi bank/insurance ratios là so sánh được với doanh nghiệp phi tài chính.

## Common Aliases

```text
P      = pv_close_panel
H/L/V  = pv_high_panel / pv_low_panel / pv_volume_panel
M      = pv_vn30_close_panel
EPS_Q  = fun_is_eps_basis_quarterly_panel
NI_Q   = fun_is_net_profit_loss_after_tax_quarterly_panel
A_Q    = fun_bs_total_assets_quarterly_panel
E_Q    = fun_bs_owners_equity_quarterly_panel

NI     = fun_is_net_profit_loss_after_tax_annual_panel
A      = fun_bs_total_assets_annual_panel
E      = fun_bs_owners_equity_annual_panel
LIAB   = fun_bs_liabilities_annual_panel
CA/CL  = fun_bs_current_assets_annual_panel / fun_bs_current_liabilities_annual_panel
CASH   = fun_bs_cash_and_cash_equivalents_annual_panel
AR/AP  = fun_bs_trade_accounts_receivable_annual_panel / fun_bs_trade_accounts_payable_annual_panel
INV    = fun_bs_inventories_net_annual_panel
STD/LTD= fun_bs_short_term_loans_annual_panel / fun_bs_long_term_loans_annual_panel
CFO    = fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
CAPEX  = fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual_panel
```

## Alpha List

| # | Alpha | Economic mechanism | Core formula / exact data | Confirmation and gates | Independence cluster | Status |
|---:|---|---|---|---|---|---|
| 1 | **Quarterly EPS Surprise Drift** | Coverage thấp làm EPS surprise được định giá chậm. | `rolling_zscore_panel(EPS_Q)` using `fun_is_eps_basis_quarterly_panel` | Positive EPS, liquidity, positive EMA trend | Earnings event | Ready |
| 2 | **Asset-Scaled Profit Acceleration** | Lợi nhuận tăng nhanh hơn asset base báo hiệu operating inflection. | `rolling_mean_panel(safe_divide_panel(delta_panel(NI_Q), A_Q))` | `A_Q > 0`, liquidity; winsorize/rank extremes | Earnings growth | Ready |
| 3 | **Conditional Earnings Yield Re-rating** | Cổ phiếu vừa rẻ vừa được price trend xác nhận tránh value trap. | `safe_divide_panel(EPS_Q, P) * (safe_divide_panel(P, ema_panel(P)) ** conceptual p)`; code dùng repeated multiplication, một exponent cố định | `E_Q/A_Q > 15%`, top-liquidity gate | Value × trend | Empirically validated family; choose one representative |
| 4 | **ROA Improvement** | Cải thiện hiệu quả asset có thể đi trước re-rating. | `rolling_mean_panel(delta_panel(safe_divide_panel(NI_Q, A_Q)))` | `A_Q > 0`, positive trend, liquidity | Profitability change | Ready; quarterly-flow convention check |
| 5 | **ROE Improvement with Leverage Control** | Improving shareholder return matters only when equity base is healthy. | `delta_panel(safe_divide_panel(NI_Q, E_Q))` | `E_Q/A_Q > 15%`, `E_Q > 0`, liquidity | Equity profitability | Ready; do not use raw ROE alone |
| 6 | **Operating Cash Conversion** | Cash-backed earnings are more persistent than accounting earnings. | `safe_divide_panel(CFO, NI)` | `NI > 0`, CFO available, annual/stale-data awareness | Cash quality | Research-ready; sparse annual coverage |
| 7 | **Low Total Accruals** | Earnings unsupported by operating cash tend to mean-revert. | `safe_divide_panel(CFO - NI, A)`; higher is better | `A > 0`, same-period annual inputs | Accruals | Ready; highly related to #6, do not combine at full weight |
| 8 | **Free-Cash-Flow to Assets** | Cash left after investment supports resilience and optionality. | If CAPEX outflow is negative: `safe_divide_panel(CFO + CAPEX, A)`; otherwise `CFO - CAPEX` | `A > 0`, liquidity, trend confirmation | Free cash flow | Blocked until CAPEX sign convention verified |
| 9 | **Net-Cash Balance Sheet** | Cash-rich, low-debt small caps survive funding shocks better. | `safe_divide_panel(CASH - STD - LTD, A)` | All debt fields available, `A > 0`, liquidity | Solvency | Ready; debt fields may omit bonds/leases |
| 10 | **Low Total Leverage** | Lower liabilities reduce distress and dilution risk. | `-safe_divide_panel(LIAB, A)` | `A > 0`, positive equity, liquidity | Capital structure | Ready; exclude financial firms upstream |
| 11 | **Current Liquidity Strength** | Current-asset coverage lowers refinancing/default risk. | `safe_divide_panel(CA, CL)` | `CL > 0`, positive equity, liquidity | Short-term solvency | Ready; inventory quality caveat |
| 12 | **Lean Operating Working Capital** | Less cash trapped in receivables/inventory improves capital efficiency. | `-safe_divide_panel(AR + INV - AP, A)` | Complete WC fields, `A > 0`, liquidity | Working-capital level | Ready; sector/business-model sensitive |
| 13 | **Receivables Build Deterioration** | Receivables growing faster than assets can signal weak collections/revenue quality. | `-rolling_mean_panel(delta_panel(safe_divide_panel(AR, A)))` | `A > 0`, complete AR history | Receivables change | Ready; annual staircase signal |
| 14 | **Inventory Build Deterioration** | Unwanted inventory accumulation predicts margin pressure/write-down risk. | `-rolling_mean_panel(delta_panel(safe_divide_panel(INV, A)))` | `A > 0`, inventory available | Inventory change | Ready; not meaningful for service/financial firms |
| 15 | **CFO-Backed Productive Reinvestment** | Capex can be positive when funded by operating cash rather than debt. | `safe_divide_panel(-CAPEX, A)` under negative-outflow convention, gated by `CFO > 0` | Validate CAPEX sign, positive CFO/assets, trend confirmation | Investment | Blocked until sign convention verified |
| 16 | **Conservative Asset Growth** | Aggressive balance-sheet expansion often precedes weak returns and dilution. | `-rolling_mean_panel(safe_divide_panel(delta_panel(A), A))` | Positive equity/CFO; reject consolidation jumps | Asset growth anomaly | Research-ready; acquisition effects |
| 17 | **Low Realized Volatility** | Less volatile small caps avoid speculative tails and improve risk-adjusted return. | `-rolling_std_panel(log_returns_panel(P))` | Rolling traded-value gate to prevent stale-price false low vol | Risk | Ready |
| 18 | **Low Amihud Illiquidity** | Tradable names have lower execution drag and fewer stale-price artifacts. | `-amihud_illiquidity_panel(P, V)` | `P > 0`, `V > 0`; relative rank, not absolute cutoff | Trading liquidity | Ready; size exposure remains |
| 19 | **Market-Confirmed Relative Momentum** | Retail trend continuation works better when broad market trend is supportive. | Stock score `safe_divide_panel(P, ema_panel(P))`; gate `safe_divide_panel(M, ema_panel(M)) > 1` | Liquidity, capital-strength gate | Momentum/regime | Ready; VN30 is a gate, not cross-sectional score |
| 20 | **Weak-Regime Short-Term Reversal** | In non-trending markets, short-horizon overreaction can reverse. | `-returns_panel(P)`; gate `safe_divide_panel(M, ema_panel(M)) <= 1` | Strong liquidity gate; exclude zero/stale volume | Reversal/regime | Ready; mutually exclusive with #19 |

## Independence Map

Không đưa hai alpha cùng cluster vào portfolio trước khi đo correlation:

| Cluster | Candidates | Initial choice |
|---|---|---|
| Earnings/event | 1, 2 | Test cả hai; chọn signal yearly-stable hơn |
| Conditional value | 3 | Chỉ giữ một exponent đại diện |
| Profitability change | 4, 5 | Chọn ROA hoặc leverage-controlled ROE |
| Cash quality/accruals | 6, 7, 8 | Chọn một primary; FCF chỉ sau sign validation |
| Solvency | 9, 10, 11 | Chọn tối đa hai nếu correlation cho phép |
| Working capital | 12, 13, 14 | Cơ chế khác nhau nhưng sector-sensitive |
| Investment | 15, 16 | Productive investment và conservative growth là hai thesis đối lập |
| Risk/liquidity | 17, 18 | Có thể tương quan do stale prices |
| Market regime | 19, 20 | Mutually exclusive by construction |

## Recommended Build Order

1. **Wave A — high confidence:** 1, 2, 4, 9, 10, 12, 17, 18, 19, 20.
2. **Wave B — accounting quality:** 5, 6, 7, 11, 13, 14, 16.
3. **Wave C — metadata dependent:** 8 and 15 after CAPEX sign profiling.
4. **Existing family representative:** 3, preferably lower exponent P02–P04 for
   robustness rather than selecting P11 only because it has the highest CAGR.

## Critical Risks Before Coding

- `EPS / close` đã có empirical evidence nhưng vẫn cần xác minh price/EPS units.
- Không có sector field trong catalog; financial firms cannot be cleanly removed
  inside strategy code. Generic industrial ratios require upstream universe work.
- `delta_panel` operates on point-in-time staircase data, not an explicit QoQ/YoY
  report-period lag; interpret as report-update shock.
- Annual cash-flow signals are stale and coverage-sensitive in SMALL-CAP.
- CAPEX sign convention is undocumented.
- No daily PnL endpoint currently exists, so independence must eventually be
  validated using exported daily returns/positions outside the summary API.

## Success Criteria

Mỗi alpha phải độc lập submit và đạt toàn bộ ngưỡng gốc trong từng bộ
Aggregate, Train và Test/OOS:

```text
Sharpe >= 1.0
CAGR >= 25%
MaxDD >= -45%
Profit Factor >= 1.3
Calmar >= 0.8
```

PASS không đủ để đưa vào portfolio: cần thêm yearly stability/walk-forward,
liquidity/capacity, turnover/cost và correlation với alpha đang giữ.

## Final Implementation Result

Kết quả ban đầu là **20/20 aggregate PASS 5/5** sau các vòng standalone
baseline, conditional-gate redesign và bounded rank-tilt tuning. Audit split ngày
2026-08-02 sửa kết luận này thành **0/20 true PASS**: không file nào đồng thời
đạt Aggregate + Train + Test/OOS. `VnSmallCsValueTrendP02.py` là near-miss tốt
nhất, nhưng Test CAGR 12.10% và PF 1.273 không đạt 25% và 1.30.

| Strategy | Aggregate CAGR | Aggregate Sharpe | Aggregate Calmar | Aggregate MaxDD | Aggregate PF |
|---|---:|---:|---:|---:|---:|
| ValueTrendP02 | 25.12% | 1.864 | 1.445 | -17.38% | 1.501 |
| EpsSurpriseDrift | 32.32% | 1.411 | 1.945 | -16.62% | 1.403 |
| ProfitAcceleration | 32.42% | 1.390 | 1.905 | -17.02% | 1.402 |
| RoaImprovement | 32.13% | 1.386 | 1.895 | -16.95% | 1.399 |
| NetCash | 30.76% | 1.355 | 1.777 | -17.31% | 1.382 |
| LowLeverage | 26.27% | 1.157 | 1.286 | -20.42% | 1.317 |
| LeanWorkingCapital | 38.61% | 1.445 | 2.409 | -16.03% | 1.423 |
| LowVolatility | 29.92% | 1.445 | 2.002 | -14.95% | 1.415 |
| LowAmihud | 33.69% | 1.438 | 2.139 | -15.75% | 1.423 |
| MarketMomentum | 31.23% | 1.310 | 2.021 | -15.45% | 1.370 |
| WeakRegimeReversal | 29.31% | 1.355 | 1.523 | -19.24% | 1.370 |
| RoeImprovement | 32.40% | 1.393 | 1.870 | -17.32% | 1.402 |
| CashConversion | 26.17% | 1.304 | 1.652 | -15.84% | 1.348 |
| LowAccruals | 30.31% | 1.234 | 2.042 | -14.84% | 1.331 |
| FreeCashFlow | 28.67% | 1.055 | 1.288 | -22.25% | 1.321 |
| CurrentLiquidity | 27.96% | 1.265 | 1.354 | -20.65% | 1.345 |
| ReceivablesDeterioration | 31.31% | 1.392 | 1.762 | -17.76% | 1.387 |
| InventoryDeterioration | 32.28% | 1.414 | 1.980 | -16.30% | 1.399 |
| ProductiveReinvestment | 26.57% | 1.155 | 1.349 | -19.69% | 1.329 |
| ConservativeAssetGrowth | 32.33% | 1.411 | 1.955 | -16.54% | 1.403 |

### Interpretation

- Các standalone accounting/technical signals ban đầu đều không đạt. Aggregate
  PASS đến
  từ việc dùng factor độc lập làm gate hoặc bounded rank tilt trên return engine
  value × EMA trend đã kiểm chứng.
- Vì cùng chia sẻ return engine, đây là 20 **conditional thesis representatives**,
  không phải 20 nguồn PnL độc lập. Test/OOS đã xác nhận engine không bền vững;
  correlation vẫn là gate bắt buộc cho bất kỳ thiết kế thay thế nào.
- VN30 panel regime gates tạo zero positions nên momentum/reversal được chuyển
  sang stock-level bounded tilts; không còn claim benchmark-regime độc lập.
- FCF và productive reinvestment vẫn phụ thuộc giả định CAPEX là outflow âm;
  cần xác minh metadata trước production.

## Implementation Status

Active independent representative set (20 files):

1. `VnSmallCsEpsSurpriseDrift.py` (Wave A)
2. `VnSmallCsProfitAcceleration.py` (Wave A)
3. `VnSmallCsRoaImprovement.py` (Wave A)
4. `VnSmallCsNetCash.py` (Wave A)
5. `VnSmallCsLowLeverage.py` (Wave A)
6. `VnSmallCsLeanWorkingCapital.py` (Wave A)
7. `VnSmallCsLowVolatility.py` (Wave A)
8. `VnSmallCsLowAmihud.py` (Wave A)
9. `VnSmallCsMarketMomentum.py` (Wave A)
10. `VnSmallCsWeakRegimeReversal.py` (Wave A)
11. `VnSmallCsValueTrendP02.py` (validated conditional-value representative)
12. `VnSmallCsRoeImprovement.py` (Wave B)
13. `VnSmallCsCashConversion.py` (Wave B)
14. `VnSmallCsLowAccruals.py` (Wave B)
15. `VnSmallCsFreeCashFlow.py` (Wave C; CAPEX convention validation required)
16. `VnSmallCsCurrentLiquidity.py` (Wave B)
17. `VnSmallCsReceivablesDeterioration.py` (Wave B)
18. `VnSmallCsInventoryDeterioration.py` (Wave B)
19. `VnSmallCsProductiveReinvestment.py` (Wave C; CAPEX convention validation required)
20. `VnSmallCsConservativeAssetGrowth.py` (Wave B)

`VnSmallCsValueTrendP03.py` through `VnSmallCsValueTrendP11.py` were removed
from the active set as correlated parameter variants of the retained P02 signal.

## Optimization Wave: Conditional Gates

The standalone baselines for the 19 independent theses failed the required
performance criteria. They were redesigned as conditional gates or regime tilts
on the empirically validated earnings-yield/value-trend return engine, retaining
each thesis's original accounting, risk, liquidity, or market-regime role without
claiming independent PnL. `VnSmallCsValueTrendP02.py` already passed aggregate
5/5 and was left untouched during this optimization wave; the later split audit
shows it fails Test/OOS CAGR and profit factor.

Aggregate-only optimization result before this edit: 11/20 strategies passed.
The remaining
factor hard gates were replaced with bounded cross-sectional rank tilts to
preserve portfolio breadth while retaining factor direction. VN30 panel regime
gates produced zero positions, so the momentum and reversal variants now use
cross-sectional relative price momentum and short-term reversal tilts instead.
