# Plan — Framework hóa Layer 3 + 4 + 5 + lọc zero (Stage 2)

> Date: 2026-08-06
> Status: APPROVED (user duyệt)
> Nền tảng: `MASTER_alpha_planning.md` (7-Layer) + `2026-08-05_alpha_validation_framework.md` (6 gate)

## Mục tiêu

1. Hiện thực hóa **Layer 3** (factor diagnostics) + **Layer 4** (economic validation) thành tool chạy được.
2. Nguồn dữ liệu: **parse trực tiếp từ file `.py` trong `output/stage_2`** — offline, không data store riêng.
3. Chuẩn hóa **Layer 5** eligibility thành template dùng chung; backfill file thiếu.
4. Chẩn đoán & fix **22 file trả 0.0000**.
5. Đầu ra `backtest/factor_diagnostics.csv` làm gate tự động trước submit.

## Pha A — Layer 3: `tools/factor_diagnostics.py`

- Quét `output/stage_2/**/cross_sectional/*.py`.
- Parse: field set (`self.data.*_panel`), op set (`self.feat.*`, `self.op.*`), eligibility block, mode (`set_portfolio_positions`).
- Whitelist field từ `syntax/data_syntax.md`; phát hiện field không tồn tại / annual-only / quarterly-only.
- Diagnostics mỗi alpha (offline, proxy từ code):
  - `field_valid`: mọi field dùng có trong whitelist?
  - `n_fields`, `freq_annual`, `freq_quarterly`, `freq_pv` (breakdown theo frequency)
  - `has_in_universe` (L0), `has_financial_gate` (L2), `has_liquidity_gate` (L5), `has_pos_denom` (L4)
  - `n_feat_ops`, `n_cs_ops`, `has_set_portfolio_positions`
  - Gắn metrics từ `backtest/results_stage_2.csv` (Sharpe train/test, CAGR, PF, MaxDD) nếu khớp tên file.
- Output: `backtest/factor_diagnostics.csv` + bảng tóm tắt theo universe.

## Pha B — Layer 4: `tools/economic_validation.py`

- Parse field-set mỗi alpha → xác định cặp statement để check:
  - NI↔CFO: `fun_is_net_profit_loss_after_tax_*` vs `fun_cf_net_cash_inflows_outflows_from_operating_activities_*`
  - Inventory↔Revenue, Receivables↔Revenue, Debt↔Interest, Capex↔PPE (presence + cùng frequency).
- Cờ `has_ni`, `has_cfo`, `has_inventory`, `has_revenue`, `has_receivables`, `has_debt`, `has_capex`, `has_ppe`, `freq_consistency` (các cặp dùng cùng frequency).
- Cảnh báo `annual_mix_warning` khi alpha trộn field annual vào ratio (nghi vấn data availability — root cause 18 file zero).
- Output: `backtest/economic_validation.csv`.

## Pha C — Layer 5 template

- Chuẩn eligibility block (L0–L10) theo `MASTER_alpha_planning.md`.
- Backfill file thiếu gate (`in_universe_panel`, financial gate, liquidity rank, positive denominator).

## Pha D — Chẩn đoán 22 file zero (KẾT QUẢ 2026-08-06)

Dùng `factor_diagnostics.py` + `economic_validation.py` + `alpha_gate.py`:

**Phát hiện then chốt: chính gate patch (trước đó) gây zero, KHÔNG phải data annual thiếu.**

- 16/16 file zero có `is_financial` gate; 2 file dùng cùng insurance field nhưng KHÔNG gate (`FinancialNetPayout`, `NetPayoutPersistenceNonFin`) → chạy tốt.
- Idiom lỗi: `is_financial = (x >= 0) | (x < 0)` = "x không NaN". Trên panel fill-missing=0 → field insurance = 0 → `0>=0` True → **mọi mã thành financial** → `~is_financial` rỗng → cagr 0.
- Gate đúng: `FinancialNetPayout` dùng **intensity threshold** `(reserve/TA > 0.05)` + `financial == True`.
- 2 file còn lại (FcfCoveredDividend2x, NetPayoutPersistence25x) = METRICS_TIMEOUT (khác, không phải gate).
- Bước chẩn đoán khác chi tiết: 30 file trộn annual+quarterly; 25 file SMALL quarterly chạy tốt → quarterly không phải nguyên nhân.
- Fix đề xuất: thay idiom `(x>=0)|(x<0)` bằng intensity-threshold gate cho 16 file, resubit để xác nhận.

## Fix gate (2026-08-06) — DONE, verify kèm file

Đã đổi 16 file sang gate intensity-threshold:
`is_financial = (safe_divide(gw_premium, total_assets_q) > 0.03) | ... | (unearned_reserve/TA > 0.05)`
căn theo mẫu đúng `VnSmallCsFinancialNetPayout` (financial = intensity/TA > threshold).

**Kết quả resubmit 16/16 thành công** (PUT/VERIFY/SIMULATE 200):
| File | Agg CAGR | Agg Sharpe | PF | Test Sharpe |
|---|---|---|---|---|
| InterestCoverage | .352 | 1.548 | 1.45 | .779 |
| WorkingCapitalLoanSafety | .355 | 1.546 | 1.45 | .652 |
| CostDiscipline | .339 | 1.514 | 1.44 | .588 |
| FreeSupplierCredit | .321 | 1.462 | 1.42 | .611 |
| QuickNetCashBuffer | .319 | 1.482 | 1.42 | .675 |
| CoreProfitability | .318 | 1.496 | 1.42 | .660 |
| MarginExpansion | .316 | 1.453 | 1.41 | .514 |
| CapitalProductivity | .312 | 1.435 | 1.40 | .477 |
| MinorityDrag | .312 | 1.423 | 1.39 | .482 |
| IdleCipRisk | .308 | 1.414 | 1.38 | .563 |
| IntangibleBurden | .309 | 1.461 | 1.41 | .508→.774 |
| EarningsYieldChange | .290 | 1.419 | 1.38 | .560 |
| RetainedEarningsQuality | .285 | 1.365 | 1.37 | .466 |
| TaxStability | .273 | 1.304 | 1.36 | .350 |
| RelatedPartyRisk | .254 | 1.274 | 1.34 | .260 |
| ProfitabilityStability | .310 | 1.352 | 1.40 | -0.116 |

**Nhận định:** trước fix 18 file = CAGR 0 (universe rỗng do gate sai); sau fix CAGR 0.25–0.36.
2 file test yếu (ProfitabilityStability test -0.12, RelatedPartyRisk test .26) → cần theo dõi Gate 1-3 yearly trước khi promote.
KHÔNG còn alpha SMALL theo gate lỗi.

## Pha E — Pipeline submit mới

- `validate_framework.py --strict → factor_diagnostics (L3) → economic_validation (L4) → submit 1 lần → 6-gate`.
- Chặn submit nếu L3/L4 fail (cờ `block_submit`).

## Pha F — Promote 4 candidate SMALL

- Chạy Gate 6 probe (bank/securities/insurance) cho `VnSmallCsFinancialNetPayout` (đã preregistered).
- Quyết exposure scaling cho CAGR ≥ 25%.

## Xác nhận

- Thay đổi code nằm trong `tools/`; alpha files chỉ sửa khi cần backfill gate (Pha C/D) và được xác nhận trước.
- Tất cả diagnostics offline (đọc `.py` + CSV), không gọi API submit mới.
