# Alpha Ideas — Round 2, Q/V families (10 cross-sectional VN-LARGE-CAP)

> **Session:** 2026-08-04
> **Trạng thái:** 🚀 Đang gen
> **Mode prior (theo `Master_Large_Cap.md` §7):** `cross_sectional`, market-neutral
> (`portfolio_weights_panel(method='rank_demean_l1')`).
> **Universe:** VN-LARGE-CAP (daily)
> **Nhiệm vụ:** hiện thực hóa **Family Q (Q01–Q05)** và **Family V (V06–V10)**.

## Mục tiêu

Master_Large_Cap xếp 9/10 idea này là `Ready`/`Probe`, mode `CS`. Đây là lần đầu
hiện thực Q/V ở chế độ cross-sectional cho LARGE. Phải tôn trọng 2 ràng buộc nền tảng:

1. **Feature khả dụng** (persist theo `agent/stage_2_guideline.md` §5): chỉ
   `safe_divide_panel`, `ema_panel`, `sma_panel`, `rolling_zscore_panel`.
   → Các prototype dùng `rolling_mean/rolling_std` (Q02 stable, Q05 multi-year) phải
   **chuyển thành EMA persistence** (EMA khoảng 1 năm) thay vì std. Đây là
   adaptation bắt buộc — ghi rõ trong docstring + card.
2. **Không residual regression** (cấm global/OLS) → các idea "residual/orthogonal"
   (Q04, V08, V10) hiện thực qua **rank spread / subtract** của 2 component riêng,
   không fit weight.

## Common construction

```python
factor = <tỷ lệ kinh tế>
eligible = <guard các field bắt buộc dương + denominator dương>
score = self.op.zscore_cs_panel(factor, mask=eligible)   # hoặc rank_cs_panel
weights = self.op.portfolio_weights_panel(score, method='rank_demean_l1', mask=eligible)
self.set_portfolio_positions(weights)
```

Guard field "bắt buộc present" dùng `> 0` (missing tự loại); mọi mask phải tham
chiếu numerator để tránh NaN vào z-score. Không dùng rolling_std/rolling_mean/
regression/lambda/import/shift âm.

## 10 Strategy

### Family Q — cash profitability & durability (Q01–Q05)

| # | File | Idea | Factor | Guard |
|---:|---|---|---|---|
| 1 | `VnLargeCsPersistentCashRoa` | Q01 Persistent Positive Cash ROA (Ready) | `ema_panel(CFO_annual/Assets_annual)` | CFO>0, Assets>0 |
| 2 | `VnLargeCsStableCashProfitability` | Q02 Stable Cash Profitability (Ready) | `ema_panel(CFO_annual/Assets_annual)` (level thay std-mean composite) | CFO>0, Assets>0 |
| 3 | `VnLargeCsCashEarningsSpread` | Q03 Cash Earnings Spread (Probe) | `CFO/Assets - PAT/Assets` | CFO>0, PAT>0, Assets>0 |
| 4 | `VnLargeCsPreWcCashStrength` | Q04 Pre-Working-Capital Strength (Probe) | `PreWCCash/Assets - PAT/Assets` (residual spread) | PreWCCash>0, PAT>0, Assets>0 |
| 5 | `VnLargeCsMultiYearFcfConsistency` | Q05 Multi-Year FCF Consistency (Probe) | `ema_panel(FCF/Assets)`, FCF=CFO-Capex | CFO>0, Capex>0, Assets>0, FCF>0 |

### Family V — valuation residual (V06–V10)

| # | File | Idea | Factor | Guard |
|---:|---|---|---|---|
| 6 | `VnLargeCsEarningsYield` | V06 Positive Earnings-to-Price Control (Ready) | `EPS_q/close` | EPS>0, close>0 |
| 7 | `VnLargeCsOcfYield` | V07 Operating-Cash-Flow Yield (Probe) | `CFO_annual/(close*shares)` = CFO/MV | CFO>0, close>0, shares>0 |
| 8 | `VnLargeCsResidualFcfYield` | V08 Capex-Cycle-Residual FCF Yield (Probe) | `(CFO-Capex)/(close*shares)`, level version (Capex intensity leg báo riêng) | FCF>0, close>0, shares>0 |
| 9 | `VnLargeCsEvAdjustedCashYield` | V09 Enterprise-Adjusted Cash Yield (Probe) | `CFO/(MV + Debt - LiquidAssets)` | EV>0, CFO>0 |
| 10 | `VnLargeCsResidualTangibleBook` | V10 EP-Residual Tangible Book (Probe) | `(Equity-goodwill-intangibles)/MV`, level+rank-spread vs EP | TBV>0, MV>0 |

## Ràng buộc / ghi chú adaptation

- **Q02/Q05:** không có `rolling_std_panel`/`rolling_mean_panel` SIMULATE_PASSED
  (CATALOG_ONLY) → dùng `ema_panel` làm persistence/stability proxy. Không claim
  parameter robustness cho default EMA window (hidden dependency).
- **V08/V10:** "residual" hiện thực bằng guard + rank spread; không regression.
- Định nghĩa: `Debt = short_term_loans + long_term_loans`,
  `LiquidAssets = cash_and_equivalents + short_term_investments`,
  `MV = close * common_shares`, `Capex = purchases_of_fixed_assets_annual`.
- Các field annual: `fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel`,
  `fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual_panel`,
  `fun_bs_short_term_loans_quarterly_panel`, `fun_bs_long_term_loans_quarterly_panel`,
  `fun_bs_cash_and_cash_equivalents_quarterly_panel`, `fun_bs_short_term_investments_quarterly_panel`,
  `fun_bs_total_assets_annual_panel`, `fun_bs_owners_equity_quarterly_panel`,
  `fun_bs_good_will_quarterly_panel`, `fun_bs_intangible_fixed_assets_quarterly_panel`,
  `fun_bs_common_shares_quarterly_panel`, `fun_is_net_profit_loss_after_tax_annual_panel`,
  `fun_cf_operating_profit_loss_before_changes_in_wc_quarterly_panel`,
  `fun_is_eps_basis_quarterly_panel`, `pv_close_panel`.

## Tiêu chí đánh giá (VN-LARGE-CAP)

| Mức | Điều kiện |
|---|---|
| PASS | Sharpe≥1.2, CAGR≥15%, MaxDD≥-35%, PF≥1.2, Calmar≥1.1 |
| Candidate | Sharpe≥1.0 & CAGR≥12% |
| Research | Sharpe≥0.6 |
| Reject | Sharpe<0 |

## Quy trình

1. ✅ Viết plan.
2. ✅ Gen 10 file `output/stage_2/vn_large_cap/cross_sectional/`.
3. ✅ Đăng ký vào `output/index.csv` (thesis_group `cash_quality` / `valuation_residual`).
4. ✅ `python tools/validate_framework.py --strict` → 0 issues.
5. ✅ Dry-run → live submit 10/10 (dùng `--files`), có rate-limit retry.
6. ✅ `check_results` → so Train/Test vs `VnLargeCsCashFlowYield`/`VnLargeCsValueMomentum`.

## Kết quả (2026-08-04)

> ⚠️ **Q/V cross-sectional: 0 PASS.** Chỉ 2 chiến lược giữ được stability train→test;
> phần còn lại yếu hoặc chết. 2 baseline CS cũ (`CashFlowYield` 0.21, `ValueMomentum`
> 0.47) vẫn không bị vượt bởi hầu hết Q/V.

### Family Q — cash profitability (Q01–Q05)

| File | Idea | Agg | Train | Test | Verdict |
|---|---:|---:|---:|---:|---|
| PersistentCashRoa | Q01 | -0.216 | -0.368 | -0.601 | Reject (âm) |
| StableCashProfitability | Q02 | -0.216 | -0.368 | -0.601 | **Degenerate — trùng Q01 từng số** |
| CashEarningsSpread | Q03 | 0.346 | 0.517 | 0.100 | Reject (test gãy) |
| PreWcCashStrength | Q04 | 0.911 | 0.987 | 0.817 | **Candidate — stable nhất family** |
| MultiYearFcfConsistency | Q05 | 0.000 | 0.000 | 0.000 | **Chết — 0 giao dịch** |

### Family V — valuation residual (V06–V10)

| File | Idea | Agg | Train | Test | Verdict |
|---|---:|---:|---:|---:|---|
| EarningsYield | V06 | 0.815 | 0.850 | 0.791 | Candidate (value control, ổn định) |
| OcfYield | V07 | 0.203 | 0.059 | 0.500 | Reject (train yếu) |
| ResidualFcfYield | V08 | 0.188 | -0.021 | 0.676 | Reject (train âm) |
| EvAdjustedCashYield | V09 | 0.247 | 0.238 | 0.264 | Reject |
| ResidualTangibleBook | V10 | 0.986 | 1.327 | 0.417 | Candidate nhưng **overfit** |

### Kết luận chung

1. **Q01 ≡ Q02 degenerate:** cả hai dùng đúng `ema_panel(CFO/Assets)` → metric trùng
   khớp từng số (Sharpe -0.216). "Stable" adaptation không khác "Persistent" — thiếu
   std leg nên Q02 không thêm thông tin. Ghi nhận lỗi thiết kế; xóa hoặc tái thiết.
2. **Q05 chết (0 giao dịch):** guard `free_cash_flow > 0 & capex > 0` quá hẹp cho
   LARGE-CAP — đa số large cap annual Capex/FCF không thỏa đồng thời. Cần nới guard
   hoặc bỏ gate dương FCF.
3. **Q04 `PreWcCashStrength` là phát hiện giá trị:** Agg 0.911, Train 0.987 → Test
   0.817, **ổn định nhất toàn batch**, MaxDD thấp (-0.13). Residual spread
   (PreWCCash/Assets − PAT/Assets) đúng hướng master dự đoán (Q04 = residual, low corr).
4. **V10 `ResidualTangibleBook` là overfit kinh điển:** Train 1.327 (PASS) → Test
   0.417. Tangible book value không bền vững OOS như Train.
5. **V06 `EarningsYield` = value control ổn định nhất** (Agg 0.815, Train 0.850 →
   Test 0.791, không gãy). Đây là control leg chuẩn để residualize V07–V10.
6. **Hướng tiếp:** giữ Q04 + V06 + V10 làm candidates; sửa Q05 (nới guard), tái thiết
   Q02 (thêm dimension thật — vd mean−λ·std nếu rolling_std được verify, hoặc dùng
   quarterly thay annual). CS LARGE vẫn chưa có chiến lược nào chạm Sharpe 1.2.

## Kết quả cải thiện Wave 2 (2026-08-04)

> ⚠️ **Phát hiện gốc rễ: sai sign convention field Capex.** Trong chế độ
> `cross_sectional`, `fun_cf_purchases_of_fixed_assets_*` là **nonpositive outflow**
> (giống `VnSmallCsFreeCashFlow`/`VnSmallCsProductiveReinvestment`: `capex <= 0`,
> `FCF = CFO + capex`). Batch Q/V dùng `capex > 0` và `CFO - capex` → **Q05 chết
> (0 giao dịch)**, **V08 bị bóp méo**. Đã sửa Q05 + V08 + tái thiết V10 + thêm composite.

### 4 chiến lược đã sửa resubmit

| File | Thay đổi | Agg | Train | Test | Verdict |
|---|---|---:|---:|---:|---|
| **CashValueComposite (mới)** | Q04 + V06 blend | 0.910 | 1.027 | 0.747 | **Bằng Q04 đơn lẻ — không tăng** |
| ResidualTangibleBook (V10) | rank-spread TBV vs EP | -0.434 | -0.462 | -0.463 | **Tệ hơn hẳn** (0.986 → -0.43) |
| MultiYearFcfConsistency (Q05) | sửa sign FCF=CFO+capex | 0.041 | -0.087 | -0.485 | Có giao dịch nhưng gần 0 |
| ResidualFcfYield (V08) | sửa sign FCF=CFO+capex | 0.163 | -0.056 | 0.776 | Test cải thiện (0.68→0.78) |

### Phân tích

1. **Composite Q04+V06 ≈ Q04 đơn lẻ (0.910 vs 0.911).** Blend không thêm sức mạnh —
   V06 (EP value) cùng chiều beta với Q04 ở LARGE, correlation giữa 2 leg quá cao để
   tạo diversifying alpha. Kết luận: cộng 2 value-quality signal cùng họ không phải
   con đường tới Sharpe 1.2.
2. **Tái thiết V10 thất bại hoàn toàn** (0.986 → -0.43). Orthogonalization vs EP đã
   xóa luôn cả tín hiệu lẫn sức mạnh; rank-spread làm mất thông tin magnitude. V10
   level cũ đẹp nhờ beta/cheapness chứ không phải leftover-alpha.
3. **Sửa sign không cứu Q05/V08:** Q05 vẫn gần 0 (guard vẫn hẹp hoặc FCF/Assets hiếm
   phân tán trong LARGE); V08 chỉ test cải thiện, train vẫn âm.

### Điểm mấu chốt cho hướng đi

- Các fundamental value/quality cross-sectional tại LARGE **bão hòa ở Sharpe ~0.9**,
  giới hạn bởi beta + efficiency — composite cùng họ không độn lên được.
- Q04 (0.911, ổn định Train 0.987→Test 0.817) vẫn là candidate tốt nhất, nhưng muốn
  qua 1.2 cần thêm nguồn alpha **thực sự orthogonal** (VN30-residual price/flow,
  family M/F — không phải thêm value leg).
- Phải verify `rolling_std_panel`/`rolling_mean_panel` để làm Q02 đúng (mean−λ·std)
  hoặc chuyển Q/V sang mid/small nơi dispersion lớn hơn.