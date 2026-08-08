# Viable Alpha Pairs — VN-MID-CAP Coverage Gap Plan

Date: 2026-08-09
Universe: `VN-MID-CAP`
Mode/template: `cross_sectional`
Status: PLANNED (chưa gen alpha)

## Mục tiêu

Lưu lại đánh giá coverage cặp nhóm dữ liệu (A-O) trên MID-CAP sau khi
82 file `VnMidCs*.py` đã submit, xác định 24 cặp còn thiếu và phân loại
mức độ phù hợp với universe MID-CAP để lấp kín coverage theo thứ tự ưu tiên.

## Coverage hiện tại

- Tổng cặp dùng được (trừ nhóm L mask + P validation): **91 / 105** cặp.
- MID-CAP đã phủ: **67 cặp** (82 file).
- Còn thiếu: **24 cặp** — đều khả thi về dữ liệu, không cần bổ sung field mới.

## Cảnh báo thiết kế (rút từ 34 alpha MID-CAP fail Test)

Tất cả alpha MID-CAP hiện có đều Test Sharpe âm. Pattern từ `results_stage_2.csv`:
alpha càng "chọn lọc" (ít giao dịch, signal fundamental mạnh) càng ít âm
hoặc dương nhẹ (FinancialProbe +0.73, InternallyFundedInvestment +0.70);
alpha rank-demean phủ toàn universe thì âm nặng (SellingCostDiscipline −2.88,
TaxRateLevel −2.30).

→ Khi gen cặp mới phải ưu tiên signal chọn lọc, gắn dòng tiền/chất lượng
lợi nhuận, và cân nhắc thay `demean_l1` (forced short leg) bằng biến thể
long-only/eligibility chặt. Nếu giữ nguyên cấu trúc cũ, kỳ vọng vẫn fail.

## 24 cặp còn thiếu trên MID-CAP

### Ưu tiên cao (8 cặp) — cơ chế mạnh + field xác nhận có data

| Cặp | #bảng | Thesis | Field chính | Lý do phù hợp MID-CAP |
|---|---|---|---|---|
| **I+N** | 97 | Capex vs disposal — đầu tư thật | `fun_cf_purchases_of_fixed_assets_*`, `fun_cf_proceeds_from_disposal_of_fixed_assets_*` | Evidence `ProductiveReinvestment` PASS ở universe khác; N có data |
| **I+O** | 98 | Mua TSCĐ bằng nợ | `fun_bs_tangible_fixed_assets_*`, `fun_bs_long_term_liabilities_*` | Đòn bẩy tài trợ tài sản, tốt cho names vừa |
| **C+M** | 39 | Cost-to-CFO — chi phí được cash hỗ trợ | `fun_is_selling_expenses_*`, `fun_is_general_and_admin_expenses_*`, `fun_cf_net_cash_inflows_outflows_from_operating_*` | CFO quality; nhóm cash-backed ít fail nhất |
| **C+N** | 40 | Cost vs capex — đầu tư hợp lý | `fun_is_selling_expenses_*`, `fun_cf_purchases_of_fixed_assets_*` | Kết hợp cost discipline + investment discipline |
| **G+M** | 81 | Cash build từ operations | `fun_bs_cash_*`, `fun_cf_net_cash_inflows_outflows_from_operating_*` | Dòng tiền thật, không phụ thuộc rank toàn universe |
| **H+M** | 89 | WC change trong CFO | `fun_bs_inventories_*`, `fun_bs_trade_accounts_receivable_*`, `fun_cf_net_cash_inflows_outflows_from_operating_*` | Top-10 pair trong DATA_GROUP (rank 7) |
| **I+M** | 96 | Depreciation/CFO — CFO chất lượng | `fun_bs_tangible_fixed_assets_*`, `fun_cf_depreciation_and_amortisation_*`, `fun_cf_net_cash_inflows_outflows_from_operating_*` | Asset-heavy names, CFO quality |
| **E+O** | 64 | Lá chắn thuế trên nợ | `fun_is_business_income_tax_current_*`, `fun_cf_financial_expenses_*` | Levered names, tương tác financing |

### Ưu tiên trung bình (6 cặp) — cơ chế OK nhưng dễ redundant/noisy

| Cặp | #bảng | Ghi chú |
|---|---|---|
| **C+I** | 35 | G&A/fixed assets — OK nhưng chồng chéo cụm cost đã fail |
| **C+H** | 34 | Cost vs WC — CẨN THẬN field WC từng rỗng (`payables_to_suppliers`), phải dùng `trade_accounts_payable` |
| **C+O** | 41 | Financial expense vs borrowings — levered names ít trên MID |
| **H+O** | 91 | WC funded by borrowings — liên quan `ShortTermRefinance` (Test −0.26, trades 96) |
| **C+G** | 33 | Cost/cash — cash-rich đã có `NetCashRank` fail; dễ redundant |
| **E+I** | 58 | Tax shield depreciation — niche, ít phân biệt |

### Ưu tiên thấp (10 cặp) — bỏ qua trước

`C+K` (37, cost/share — dilution noise), `C+J` (36), `C+D` (30), `D+E` (43),
`E+J` (59), `I+J` (93), `I+K` (94), `J+M` (102), `J+N` (103), `J+O` (104).

Lý do: nhóm J (investments) và K (shares) signal yếu/khó tin trên MID-CAP
không financial; `J+O` đầu tư bằng nợ thiếu names đủ.

## Kết luận & bước tiếp theo

1. Không cần bổ sung field mới — 24 cặp đều có data; chỉ cần dùng đúng field
   `trade_accounts_payable` thay `payables_to_suppliers` cho nhóm H.
2. Nên gen **8 cặp ưu tiên cao** trước (I+N, I+O, C+M, C+N, G+M, H+M, I+M, E+O).
3. Trước khi gen hàng loạt: quyết định cấu trúc weights — giữ `demean_l1`
   hay thử biến thể long-only/eligibility chặt để kiểm chứng trên 1-2 cặp.
4. Sau khi gen: cập nhật `PAIR_COVERAGE_PLAN.md` + `HYPOTHESIS_LIBRARY.md`
   với trạng thái MID mới.

## Checklist trước khi submit (kế thừa framework 08-05)

- [ ] Cặp phủ khớp script scan (không dùng field ngoài cặp)
- [ ] `python tools/validate_framework.py --strict` pass 0 issue
- [ ] Submit song song: `tools/submit_and_check.py --parallel --workers <n> --force --yes`
- [ ] Ghi kết quả vào `backtest/results_stage_2.csv` + cập nhật evidence library
