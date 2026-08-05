# 20 Core-Earnings / Cash-Flow / Balance-Sheet Alpha Ideas — VN-SMALL-CAP

> Date: 2026-08-05
> Universe: `VN-SMALL-CAP`
> Mode: `cross_sectional` (`_panel`, market-neutral)
> Canonical data catalog: `syntax/data_syntax.md`
> Market reference: `data/vietnam_market_characteristics.md`
> Predecessor: `2026-08-02_20_independent_small_cap_alpha_ideas.md` (không trùng lặp cơ chế)

## Objective

20 economic theses **khác cơ chế** so với bộ 20 trước (EPS surprise, profit
acceleration, earnings-yield × trend, ROA/ROE, cash conversion, accruals, FCF,
net cash, leverage, current ratio, lean WC, receivables/inventory build,
reinvestment, asset growth, low vol, low Amihud, momentum, reversal).

Nhóm mới tập trung vào 4 cluster chưa khai thác:
1. **Core Earnings Quality** — tách lợi nhuận ngoài hoạt động, khả năng trả lãi, chi phí, thuế.
2. **Cash-flow Timing & Funding** — thuế/cổ tức/vay/phát hành nhìn từ dòng tiền.
3. **Balance-sheet Micro-Structure** — phải thu nội bộ, goodwill, CIP, vốn lưu động ngắn hạn.
4. **Dynamic / Stability** — sự thay đổi và ổn định, không phải level tĩnh.

Mọi strategy phải:
- Dùng report point-in-time sau ngày publish; không backfill/negative shift.
- Dùng `_panel` fields và `self.set_portfolio_positions(...)`.
- Gate `(close > 0) & (volume > 0)` và denominator dương; mask điều kiện kinh tế rõ ràng.
- Liquidity/capacity gate: rank rolling traded value, ưu tiên `> 0.40` (top-60%) như family PASS đã xác nhận.
- Quality gate: `equity / total_assets > 15%` (capital-strength floor).
- Test cả `rank_demean_l1` và `demean_l1`; không nhân gross exposure.
- Không dùng bank/insurance ratios cho doanh nghiệp phi tài chính.
- Verify dấu (sign) convention của mọi field cash-flow trước khi code (xem §Critical Risks).

## Common Aliases

```text
P      = pv_close_panel
V      = pv_volume_panel
EPS_Q  = fun_is_eps_basis_quarterly_panel
NI_Q   = fun_is_net_profit_loss_after_tax_quarterly_panel
A_Q    = fun_bs_total_assets_quarterly_panel
E_Q    = fun_bs_owners_equity_quarterly_panel

NI_A   = fun_is_net_profit_loss_after_tax_annual_panel
NI_BT  = fun_is_net_accounting_profit_loss_before_tax_quarterly_panel
FI     = fun_is_financial_income_quarterly_panel
FE     = fun_is_financial_expenses_quarterly_panel
SELL   = fun_is_selling_expenses_quarterly_panel
GAE    = fun_is_general_and_admin_expenses_quarterly_panel
TAX_C  = fun_is_business_income_tax_current_quarterly_panel
PARENT = fun_is_attributable_to_parent_company_quarterly_panel
MINO   = fun_is_minority_interests_quarterly_panel

CFO    = fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
TAX_P  = fun_cf_business_income_tax_paid_annual_panel
DIV    = fun_cf_dividends_paid_annual_panel
PRB    = fun_cf_proceeds_from_borrowings_annual_panel
PRS    = fun_cf_proceeds_from_issue_of_shares_annual_panel
RPB    = fun_cf_repayment_of_borrowings_annual_panel

CASH   = fun_bs_cash_and_cash_equivalents_quarterly_panel
STI    = fun_bs_short_term_investments_quarterly_panel
STL    = fun_bs_short_term_loans_quarterly_panel
AP     = fun_bs_trade_accounts_payable_quarterly_panel
ADV    = fun_bs_advances_from_customers_quarterly_panel
INV    = fun_bs_inventories_net_quarterly_panel
OTH_R  = fun_bs_other_receivables_quarterly_panel
INTER_R= fun_bs_intercompany_receivables_quarterly_panel
GW     = fun_bs_good_will_quarterly_panel
INTANG = fun_bs_intangible_fixed_assets_quarterly_panel
TFA    = fun_bs_tangible_fixed_assets_quarterly_panel
CIP    = fun_bs_construction_in_progress_quarterly_panel
RE     = fun_bs_undistributed_earnings_quarterly_panel
```

## Alpha List

| # | Alpha | Economic mechanism | Core formula / exact data | Confirmation and gates | Independence cluster | Status |
|---:|---|---|---|---|---|---|
| 1 | **Core Profitability ex-Financial** | Lợi nhuận thật tới từ hoạt động, không phải thu nhập tài chính/ngoài ngành | `(NI_Q + FE − FI) / A_Q` | `A_Q > 0`, EPS gate, liquidity, quality gate | Core quality | Ready |
| 2 | **Interest Coverage** | Khả năng trả lãi từ lợi nhuận trước thuế → ít rủi ro distress | `safe_divide_panel(NI_BT, FE)` | `FE > 0`, `NI_BT > 0`, liquidity, quality gate | Core quality | Ready |
| 3 | **Cost Discipline (SG&A)** | Lean chi phí bán hàng + quản lý → scale tốt khi re-rating | `−(SELL + GAE) / A_Q` | `A_Q > 0`, EPS gate, liquidity | Core quality | Ready |
| 4 | **Effective Tax Stability** | Thuế suất ổn định = lợi nhuận thật; chập chờn = quản trị lợi nhuận | `−rolling_std_panel(TAX_C / NI_BT)` | `NI_BT > 0`, `TAX_C > 0`, liquidity | Core quality | Ready; rolling window nhỏ do quarterly sparse |
| 5 | **Cash Tax Coverage** | Deferred tax lớn = rủi ro cash tương lai; thuế đã đóng thực tế bao phủ nghĩa vụ | `safe_divide_panel(TAX_P, TAX_C)` (nghịch: cao = tốt) | `TAX_C > 0`, CFO available, liquidity | Cash quality | Sign convention phải verify |
| 6 | **Dividend Sustainability** | Cổ tức được bao bởi dòng tiền hoạt động, không phải vay | `safe_divide_panel(DIV, CFO)` (nghịch) | `CFO > 0`, `DIV > 0`, liquidity | Cash quality | Sign convention phải verify |
| 7 | **Self-Funding (External Dependence)** | Tránh phụ thuộc vay/phát hành để cấp vốn; tự tài trợ bền hơn | `−(PRB + PRS − RPB) / A_Q` | `A_Q > 0`, EPS gate, liquidity | Funding | Sign convention phải verify |
| 8 | **Retained Operating Cash** | Tiền mặt giữ lại sau cổ tức → năng lực tái đầu tư nội bộ | `(CFO − DIV) / A_Q` | `A_Q > 0`, `CFO > 0`, liquidity | Cash quality | Sign convention phải verify |
| 9 | **Working-Capital Loan Safety** | Đệm tiền mặt vs. vay ngắn hạn → tránh rollover shock | `safe_divide_panel(CASH, STL)` | `STL > 0`, liquidity, quality gate | Short-term solvency | Ready |
| 10 | **Free Supplier Credit** | Được nhà cung cấp/khách hàng cấp vốn thay vì ngân hàng | `safe_divide_panel(AP + ADV, INV)` | `INV > 0`, liquidity | Working capital | Sector-sensitive |
| 11 | **Related-Party Receivable Risk** | Phải thu nội bộ/lân cận cao = rủi ro sân sau (tunneling) ở VN | `−(OTH_R + INTER_R) / A_Q` | `A_Q > 0`, liquidity | Receivables quality | Ready; tránh trùng #13 bộ cũ (trade receivables) |
| 12 | **Intangible Burden** | Goodwill + tài sản vô hình cao làm sổ sách "dirty" | `−(GW + INTANG) / E_Q` | `E_Q > 0`, liquidity, quality gate | Asset quality | Ready |
| 13 | **Capital Productivity** | Lợi nhuận trên TSCĐ hữu hình — hiệu quả vốn nặng | `safe_divide_panel(NI_Q, TFA)` | `TFA > 0`, liquidity | Asset efficiency | Ready |
| 14 | **Idle CIP Risk** | XDCB dở dang lớn = vốn kẹt không sinh lời | `−CIP / A_Q` | `A_Q > 0`, liquidity | Investment efficiency | Ready |
| 15 | **Book Quality (Retained Earnings)** | Lợi nhuận giữ lại lớn trên tài sản = nền tảng sổ sách vững | `safe_divide_panel(RE, A_Q)` | `A_Q > 0`, `RE > 0`, liquidity | Book quality | Ready |
| 16 | **Earnings-Yield Change (ΔEY)** | Cổ phiếu đang rẻ dần với nền tảng ổn định → điểm vào value (khác level EY) | `delta_panel(safe_divide_panel(EPS_Q, P))` | EPS gate, liquidity, quality gate | Value change | Ready; yearly stability bắt buộc |
| 17 | **Profitability Stability** | ROE ít biến động = chất lượng lặp lại | `−rolling_std_panel(safe_divide_panel(NI_Q, E_Q))` | `E_Q > 0`, liquidity | Quality stability | Ready |
| 18 | **Quick Net-Cash Buffer** | Cash + đầu tư ngắn hạn − vay ngắn hạn (đệm nhanh, khác net-cash toàn phần) | `(CASH + STI − STL) / A_Q` | `A_Q > 0`, liquidity | Solvency | Ready |
| 19 | **Minority-Interest Drag** | Lợi nhuận bị minority ăn bớt → ít giá trị cho cổ đông parent | `safe_divide_panel(PARENT, NI_Q)` | `NI_Q > 0`, liquidity | Ownership quality | Ready |
| 20 | **Margin Expansion (Op Leverage)** | Tốc độ tăng lợi nhuận vượt tốc độ tăng chi phí → operating leverage | `delta_panel(NI_Q / A_Q) − delta_panel((SELL + GAE) / A_Q)` | `A_Q > 0`, EPS gate, liquidity | Profitability change | Ready; kết hợp #3 với hướng động |

## Independence Map

Không đưa hai alpha cùng cluster vào portfolio trước khi đo correlation:

| Cluster | Candidates | Initial choice |
|---|---|---|
| Core quality | 1, 2, 3, 4 | 1 làm primary; 3 hoặc 4 làm gate, không cộng đồng thời 4 cái |
| Cash quality | 5, 6, 8 | Chọn một primary sau sign validation; 7 (funding) tách riêng |
| Solvency/short-term | 9, 18 | Có thể tương quan — giữ 1 |
| Working capital | 10 | Sector-sensitive, standalone |
| Asset quality | 12, 14, 15 | 3 góc khác nhau của balance sheet, cơ chế khác |
| Receivables | 11 | Không trùng trade-receivables build (bộ cũ) |
| Efficiency | 13 | Standalone |
| Dynamic | 16, 17, 20 | 16 và 20 khác cơ chế (value vs operating leverage); 17 là gate stability |
| Ownership | 19 | Standalone |

## Recommended Build Order

1. **Wave A — high confidence (field quarterly, sign đơn giản):** 1, 2, 3, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20.
2. **Wave B — rolling/sparse signals:** 4, 10.
3. **Wave C — metadata dependent (sign convention cash-flow):** 5, 6, 7, 8 — chỉ code sau khi profile dấu của `TAX_P`, `DIV`, `PRB`, `PRS`, `RPB`, `CFO`.

## Critical Risks Before Coding

- **Cash-flow sign convention:** `CFO`, `TAX_P`, `DIV`, `PRB`, `PRS`, `RPB` có thể là inflow/outflow dương hay âm tùy quy ước platform. Phải verify metadata/example trước; không suy diễn.
- **Annual cash-flow signals stale:** dữ liệu annual của SMALL-CAP coverage thấp; dùng point-in-time, `.notna()`-style gate, không backfill.
- **Quarterly sparse:** `delta_panel`/`rolling_std_panel` trên quarterly staircase thể hiện report-update shock, không phải QoQ kỳ. Diễn giải đúng.
- **No sector field:** không loại sạch financial firms trong code; ratio phi tài chính cần upstream universe work (như bộ 20 cũ).
- **EPS / close units:** đã có empirical evidence nhưng vẫn nên xác minh price/EPS units khi debug.
- **Related-party & CIP:** dữ liệu có thể sparse; nếu signal rỗng do thiếu field → bỏ khỏi set, không hạ threshold.

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
liquidity/capacity, turnover/cost và correlation với alpha đang giữ
(xem `syntax/research/validation_protocol.md`).

## Status

20 idea sẵn sàng thiết kế chi tiết. Chưa code — chờ duyệt batch declaration
(theo rule `agent/GUIDE.md` §Round 2) trước khi gen vào
`output/stage_2/vn_small_cap/cross_sectional/`.
