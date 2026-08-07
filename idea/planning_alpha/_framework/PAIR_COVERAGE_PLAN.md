# PAIR COVERAGE PLAN — Phủ hết các cặp nhóm dữ liệu còn thiếu

> Date: 2026-08-07
> Mode: `cross_sectional` (`_panel`, `set_portfolio_positions`)
> Reference: `DATA_GROUP_COMBINATIONS.md` (120 pairs), `MASTER_alpha_planning.md` (7-layer), `HYPOTHESIS_LIBRARY.md` (H01-H36)
> Validation framework: `stage_2/2026-08-05_alpha_validation_framework.md`

---

## 1. Mục tiêu

Phủ **toàn bộ 105 cặp dùng được** (120 cặp trừ 15 cặp nhóm P — P là validation-only, không dùng làm signal theo thiết kế).

| Trạng thái | Số cặp | Ghi chú |
|---|---|---|
| Đã phủ (scan 150 file cross_sectional) | **77 / 105** | 44 LARGE + 43 MID + 63 SMALL |
| Còn thiếu cần làm | **28** | Chi tiết bên dưới |
| Loại trừ (P-pairs, validation-only) | 15 | Không gen alpha |

---

## 2. 28 cặp còn thiếu — chia 5 cụm theo cơ chế kinh tế

### Cụm 1 — COST DISCIPLINE (anchor C, 8 cặp)

> Lean operators outperform. Chi phí vận hành thấp, đòn bẩy chi phí, chi phí tài chính thấp.

| # | Cặp | #bảng | Thesis | Công thức tín hiệu (sign) | Field |
|---|---|---|---|---|---|
| 1 | **C+E** | 31 | Cost discipline vs tax burden | `(selling+GAE)/assets` thấp + `tax_current/pre_tax` ổn định | C, E, F |
| 2 | **C+G** | 33 | Cash cost ratio | `(selling+GAE)/cash` thấp (lean vs cash buffer) | C, G |
| 3 | **C+H** | 34 | Operating cost vs WC efficiency (MASTER F7 Payable Days) | `payables/COGS` cao (days payable) hoặc `(selling+GAE)/WC` | C, H, B |
| 4 | **C+I** | 35 | G&A to fixed assets | `(selling+GAE)/tangible_fixed_assets` thấp | C, I |
| 5 | **C+K** | 37 | Cost per share impact | `(selling+GAE)/common_shares` thấp | C, K |
| 6 | **C+M** | 39 | Cost-to-CFO | `CFO/(selling+GAE)` cao (cash bang chi phí) | C, M |
| 7 | **C+N** | 40 | Cost vs capex | `capex/(selling+GAE)` cao = đầu tư hợp lý | C, N |
| 8 | **C+O** | 41 | Financial expense vs borrowings | `financial_expenses/borrowings` thấp (chi phí nợ thấp) | C, O |

### Cụm 2 — TAX EFFICIENCY (anchor E, 7 cặp)

> Thuế ổn định & hiệu quả = lợi nhuận thật, không phải profit management.

| # | Cặp | #bảng | Thesis | Công thức tín hiệu (sign) | Field |
|---|---|---|---|---|---|
| 9 | **E+G** | 56 | Tax paid vs cash buffer | `tax_current/cash` thấp (khả năng nộp thuế) | E, G |
| 10 | **E+H** | 57 | Deferred tax vs WC | `tax_deferred/WC` thấp (ít trì hoãn thuế = thật) | E, H |
| 11 | **E+I** | 58 | Tax shield (depreciation) | `depreciation/tax_current` vừa phải | E, I, M |
| 12 | **E+K** | 60 | Tax per share | `tax_current/common_shares` thấp | E, K |
| 13 | **E+M** | 62 | Tax paid vs CFO | `tax_current/CFO` thấp & ổn định | E, M |
| 14 | **E+N** | 63 | Tax on investment gains | `tax_current/profit_from_investing` thấp | E, N |
| 15 | **E+O** | 64 | Tax shield on debt | `tax_current/financial_expenses` (nợ thuế = lá chắn) | E, O, C |

### Cụm 3 — ASSET PRODUCTIVITY (anchor I, 5 cặp)

> Tài sản cố định sinh ra hiệu quả: dòng tiền, đầu tư, tài trợ.

| # | Cặp | #bảng | Thesis | Công thức tín hiệu (sign) | Field |
|---|---|---|---|---|---|
| 16 | **G+I** | 77 | Cash vs fixed assets (asset-light) | `cash/tangible_fixed_assets` cao | G, I |
| 17 | **H+I** | 85 | Total asset efficiency | `(receivables+inventories-payables)/fixed_assets` thấp | H, I, F |
| 18 | **I+M** | 96 | Depreciation in CFO | `depreciation/CFO` thấp (CFO chất lượng) | I, M |
| 19 | **I+N** | 97 | Capex vs disposal | `capex/proceeds_from_disposal` cao (đầu tư thật) | I, N |
| 20 | **I+O** | 98 | Asset acquisition via debt | `long_term_liabilities/tangible_fixed_assets` thấp | I, F, O |

### Cụm 4 — LIQUIDITY x CAPITAL FLOW (G/H + N/O, 4 cặp)

> Tiền mặt & vốn lưu động đối chiếu dòng đầu tư/tài trợ.

| # | Cặp | #bảng | Thesis | Công thức tín hiệu (sign) | Field |
|---|---|---|---|---|---|
| 21 | **G+N** | 82 | Cash used in investments | `capex/cash` thấp (đầu tư không đốt tiền) | G, N |
| 22 | **G+O** | 83 | Cash returned to investors | `(dividends+repurchases)/cash` vừa phải | G, O |
| 23 | **H+N** | 90 | Receivables from investments | `investments_in_others/WC` thấp (tránh lệch vốn) | H, J, N |
| 24 | **H+O** | 91 | WC funded by borrowings | `short_term_loans/WC` thấp (không vay nuôi WC) | H, O |

### Cụm 5 — PAYOUT, RETENTION, INVESTMENT (B/J + N/O, 4 cặp)

> Lợi nhuận giữ lại, cổ tức, dòng đầu tư.

| # | Cặp | #bảng | Thesis | Công thức tín hiệu (sign) | Field |
|---|---|---|---|---|---|
| 25 | **B+N** | 27 | Investment return quality | `net_profit/capex` cao (ROIC proxy) | B, N, F |
| 26 | **B+O** | 28 | Retention ratio (MASTER F3 Growth) | `1 - dividends/net_profit` cao | B, O |
| 27 | **J+N** | 103 | Investment flows | `investments_in_other_entities/capex` thấp (tập trung core) | J, N |
| 28 | **J+O** | 104 | Investment funded by debt | `long_term_liabilities/long_term_investments` thấp | J, F, O |

---

## 3. Batching & thứ tự ưu tiên

> Nguyên tắc: mỗi cặp → tối thiểu 1 alpha độc lập về cơ chế (KHÔNG tạo nhiều alpha cùng 1 engine khác nhau mỗi tilt — bài học `2026-08-02_batch_6_10_independent_mid_cap_alpha.md`).

| Batch | Cụm | #alpha | Ưu tiên | Lý do |
|---|---|---|---|---|
| B1 | Cụm 1 Cost (8 cặp) | 8 | **Cao** | Chi phí là đầu vào chưa khai thác; `VnSmallCsCostDiscipline` đã tồn tại (lean tilt PASS hướng) |
| B2 | Cụm 3 Asset Productivity (5 cặp) | 5 | Cao | I+N, I+M gần hướng FCF/capex đã có evidence (`ProductiveReinvestment` PASS 1.79) |
| B3 | Cụm 2 Tax (7 cặp) | 7 | Trung bình | `VnSmallCsTaxStability` là tiền lệ; tax hiếm dùng, dễ bổ sung coverage |
| B4 | Cụm 4 + 5 (8 cặp) | 8 | Trung bình | B+O (retention) & J+O mang giá trị MASTER completeness |

---

## 4. Blueprint chung mỗi alpha (chuẩn 7-layer)

Mẫu cấu trúc file (tham chiếu `VnSmallCsCostDiscipline.py`):

```python
name:    <Universe><Cs><Thesis>
summary: <1 câu> rank-tilt trên engine value-trend đã validate (hoặc alpha độc lập)
idea:    <cặp> — <thesis kinh tế 1 câu>

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # Layer 0: data._panel fields (đúng cặp)
        # Layer 1: primitive (safe_divide_panel, rolling_mean, delta, ema)
        # Layer 5 gates:
        #   base_eligible = eps>0 & close>0 & volume>0 & equity_q>0 &
        #                   total_assets_q>0 & capital_strength>0.15 &
        #                   (~is_financial)   # L-field mask
        #   liquidity_rank = rank_cs_panel(rolling_value_panel(close,volume), mask=base_eligible)
        #   eligible = base_eligible & (liquidity_rank > 0.40)
        # factor_rank = rank_cs_panel(factor, mask=eligible)  hoặc demean
        # signal = core * tilt  (tilt = 1.5 - rank cho chi phí/thuế thấp)
        # weights = portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        # self.set_portfolio_positions(weights)
```

### Rule cứng
1. Mỗi alpha phủ **đúng 1 cặp** (đếm được bằng script scan `self.data.*_panel`).
2. `sign convention` CF: dividends ≤ 0, issuance > 0, borrowings > 0 → dùng `-dividends` khi cần.
3. Denominator guards: `safe_divide_panel` + mask denominator > 0.
4. Point-in-time: fundamental chỉ dùng sau ngày công bố; missing = unavailable.
5. `method='demean_l1'` hoặc `rank_demean_l1` — **KHÔNG** pre-winsorize/rank trước (no-op — bài học `2026-08-04_q_v_noise_filter_w3_large_cap.md`).
6. Không tạo biến thể cùng cặp cùng engine; nếu muốn 2nd alpha cho 1 cặp, phải đổi cơ chế.

---

## 5. Validation & tiêu chuẩn PASS (kế thừa 08-05 framework)

| Gate | Tiêu chí | Ngưỡng |
|---|---|---|
| Gate 1 | Aggregate Sharpe | ≥ 1.2 |
| Gate 2 | Train Sharpe | ≥ 1.0 |
| Gate 3 | Test Sharpe | ≥ 0.8 & không âm |
| Robust | Sharpe 2022 (crash) + 2024 | dương cả 2 |
| Magnitude | CAGR | ≥ 25% (SMALL) / theo universe |
| Anti-overfit | Survival check + correlation vs existing | < 0.6 |

**Discriminator chuẩn:** Train/Test Sharpe + Sharpe 2022 & 2024. Survival 84→4 (α=5%) — đừng kỳ vọng nhiều PASS.

---

## 6. Checklist trước khi submit

- [ ] Cập nhật `HYPOTHESIS_LIBRARY.md` (Vietnam Evidence cho từng hypothesis mới)
- [ ] Cặp phủ khớp script scan (không dùng field ngoài cặp)
- [ ] `python tools/validate_framework.py --strict` pass 0 issue
- [ ] Submit song song: `tools/submit_and_check.py --parallel --workers <n> --force --yes`
- [ ] Ghi kết quả vào `backtest/results_stage_2.csv` (tự động) + cập nhật evidence trong library
