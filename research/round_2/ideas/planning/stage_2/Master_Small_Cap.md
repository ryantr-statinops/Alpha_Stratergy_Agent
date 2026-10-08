# VN-SMALL-CAP: 50 Academic Alpha Ideas for a Low-Correlation Portfolio

Ngày nghiên cứu: 2026-08-02  
Phạm vi: Round 2, `VN-SMALL-CAP`, daily equity, point-in-time data  
Vai trò tài liệu: master research universe; thay thế danh sách 12 idea sơ bộ khi có mâu thuẫn

## 0. Kết luận điều hành

Tài liệu này không tạo 50 biến thể bằng cách đổi window. Nó tạo 50 giả thuyết thuộc 10 cơ chế kinh tế khác nhau:

1. Valuation.
2. Earnings information diffusion.
3. Accrual và working-capital quality.
4. Profitability và business quality.
5. Investment và capital allocation.
6. Financing và payout policy.
7. Balance-sheet resilience.
8. Price-path behavior.
9. Risk, lottery demand và benchmark exposure.
10. Liquidity, attention và trading pressure.

Mỗi họ có năm idea. Các idea trong cùng họ thường là **substitutes**, không phải năm alpha độc lập để đưa đồng thời vào portfolio. Quy trình đúng là backtest từng idea, chọn một champion mỗi họ, sau đó cluster lại bằng correlation của **daily PnL**, downside PnL và overlap vị thế.

Ba nguyên tắc xuyên suốt:

- Bằng chứng Việt Nam được ưu tiên hơn việc bê nguyên factor từ Mỹ.
- Chỉ dùng field có trong `syntax/data_syntax.md`; không giả định có sector, market cap, publication date, adjusted close, bid-ask spread, foreign flow hay analyst data.
- Correlation thấp là kết quả phải đo ngoài mẫu, không phải thuộc tính suy ra từ tên factor.

## 1. Vì sao VN-SMALL-CAP cần kiến trúc riêng

Theo HOSE, VNSmallcap là phần còn lại của VNAllshare sau khi loại VN100; chỉ số dùng free-float adjusted market capitalization, có review thành phần vào tháng 1 và tháng 7, cập nhật shares/free float hàng quý, và giới hạn tỷ trọng cổ phiếu đơn lẻ. Vì vậy universe có membership drift và không nên được xem như một tập ticker cố định.

Factsheet ngày 30-01-2026 ghi nhận VNSmallcap có 182 constituents; tỷ trọng ngành lớn nhất thuộc industrials, materials, real estate, financials và consumer. Top 10 chỉ chiếm 25.50%, thấp hơn nhiều so với một chỉ số tập trung. Điều này tạo breadth tốt cho cross-sectional ranking nhưng cũng làm coverage, stale price và capacity trở thành rủi ro trung tâm. [HOSE VNSmallcap factsheet]

Nghiên cứu toàn diện nhất cho thị trường Việt Nam giai đoạn 2007-2022 cho thấy:

- Size premium có ý nghĩa; small-cap có future return cao hơn large-cap.
- Earnings-to-price (`EP`) subsume book-to-market (`BM`) và cash-flow-to-price (`CP`) trong horse race tại Việt Nam.
- VN-4 gồm market, size, EP và turnover giải thích phần lớn anomaly.
- High 12-month turnover dự báo return thấp, đặc biệt ở small firms và nơi limits-to-arbitrage cao.
- One-month abnormal turnover và one-week reversal còn alpha sau VN-4; hai biến này có chiều tín hiệu khác nhau và phải được tách riêng.
- Momentum 12-2 không ổn định bằng 52-week high.

Nguồn chính: [Huang, Liu & Shu (2023), Factors and anomalies in the Vietnamese stock market](https://www.pbcsf.tsinghua.edu.cn/__local/7/F5/A9/E0366D36DF73499C8CBFB66C505_4D50779F_1C1EEF.pdf).

## 2. Chuẩn bằng chứng và tính khả thi

### Evidence tier

| Tier | Ý nghĩa |
|---|---|
| A-VN | Có bằng chứng trực tiếp trên thị trường Việt Nam hoặc kiểm định Việt Nam rất gần signal |
| A-INT | Bằng chứng quốc tế mạnh, cơ chế rõ, đã được nghiên cứu rộng |
| B | Bằng chứng tốt nhưng specification/market dependence đáng kể |
| C | Hypothesis khoa học tương thích dữ liệu; phải chịu hurdle OOS cao hơn |

### Feasibility

| Nhãn | Ý nghĩa |
|---|---|
| Ready | Field trực tiếp, công thức và dấu tương đối rõ |
| Probe | Field có sẵn nhưng phải kiểm tra sign convention, coverage hoặc point-in-time update |
| Experimental | Dựng được nhưng estimation noise/capacity cao; chỉ dùng sau robustness test |

### Hurdle khoa học

Không dùng `t > 2` như giấy thông hành. Harvey, Liu và Zhu cho rằng factor mới sau khi tính multiple testing cần hurdle gần `t > 3`; Hou, Xue và Zhang cho thấy phần lớn hàng trăm anomaly không replicate dưới tiêu chuẩn chặt, đặc biệt nhóm trading frictions. Vì Round 2 đang thử nhiều idea trên cùng dữ liệu, mọi kết quả phải có untouched holdout, parameter plateau và false-discovery control. [Harvey, Liu & Zhu](https://www.nber.org/papers/w20592), [Hou, Xue & Zhang](https://academic.oup.com/rfs/article-abstract/33/5/2019/5236964)

## 3. Field map thực tế

Catalog hiện có 496 field dùng chung cho ba universe: 10 price-volume, 130 income statement, 271 balance sheet và 85 cash-flow field. Các nhóm field dùng trong master này:

### Price, volume và benchmark

- `pv_open_panel`, `pv_high_panel`, `pv_low_panel`, `pv_close_panel`, `pv_volume_panel`
- `pv_vn30_open_panel`, `pv_vn30_high_panel`, `pv_vn30_low_panel`, `pv_vn30_close_panel`, `pv_vn30_volume_panel`
- `pv_dji_open_panel`, `pv_dji_high_panel`, `pv_dji_low_panel`, `pv_dji_close_panel`, `pv_dji_volume_panel`
- `in_universe_panel` — boolean: investable universe eligibility gate

### Earnings

- `fun_is_eps_basis_quarterly_panel`
- `fun_is_net_profit_loss_after_tax_quarterly_panel`, `fun_is_net_profit_loss_after_tax_annual_panel`
- `fun_is_net_accounting_profit_loss_before_tax_quarterly_panel`

### Balance sheet

- `fun_bs_total_assets_quarterly_panel`, `fun_bs_owners_equity_quarterly_panel`
- `fun_bs_common_shares_quarterly_panel`, `fun_bs_liabilities_quarterly_panel`
- `fun_bs_cash_and_cash_equivalents_quarterly_panel`
- `fun_bs_current_assets_quarterly_panel`, `fun_bs_current_liabilities_quarterly_panel`
- `fun_bs_short_term_loans_quarterly_panel`, `fun_bs_long_term_loans_quarterly_panel`
- `fun_bs_accounts_receivable_quarterly_panel`, `fun_bs_inventories_net_quarterly_panel`
- `fun_bs_short_term_prepayments_quarterly_panel`, `fun_bs_trade_accounts_payable_quarterly_panel`
- `fun_bs_short_term_investments_quarterly_panel`, `fun_bs_long_term_investments_quarterly_panel`
- `fun_bs_undistributed_earnings_quarterly_panel`, `fun_bs_paid_in_capital_quarterly_panel`
- `fun_bs_fixed_assets_quarterly_panel`, `fun_bs_construction_in_progress_quarterly_panel`
- `fun_bs_good_will_quarterly_panel`

### Cash flow và corporate actions

- `fun_cf_net_cash_inflows_outflows_from_operating_activities_quarterly_panel`
- `fun_cf_operating_profit_loss_before_changes_in_wc_quarterly_panel`
- `fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_quarterly_panel`
- `fun_cf_proceeds_from_disposal_of_fixed_assets_quarterly_panel`
- `fun_cf_proceeds_from_borrowings_quarterly_panel`, `fun_cf_repayment_of_borrowings_quarterly_panel`
- `fun_cf_proceeds_from_issue_of_shares_quarterly_panel`
- `fun_cf_dividends_paid_quarterly_panel`
- `fun_cf_payments_for_share_returns_and_repurchases_quarterly_panel`
- `fun_cf_interest_paid_quarterly_panel`
- `fun_cf_increase_decrease_in_receivables_quarterly_panel`
- `fun_cf_increase_decrease_in_inventories_quarterly_panel`
- `fun_cf_increase_decrease_in_payables_quarterly_panel`

### Giới hạn dữ liệu quyết định thiết kế

- Không có generic revenue/COGS đáng tin cậy cho toàn universe; không tạo sales surprise, gross margin hay full Beneish M-score.
- Không có publication timestamp riêng; PEAD phải dùng point-in-time field update của platform và delay robustness.
- Không có explicit market-cap field; dùng `close * common_shares` như proxy và kiểm tra split/corporate action.
- Không có bid-ask spread; liquidity chỉ dùng Amihud, turnover, zero/stale-return proxy và benchmark liquidity.
- Không có sector classification; các ratio đặc thù ngành phải được mask bằng coverage/behavior, không tự gán ngành.

## 4. Bản đồ 50 idea

| ID | Idea | Tier | Feasibility | Horizon chính | Correlation cluster |
|---|---|---|---|---:|---|
| V01 | Positive Earnings-to-Price | A-VN | Ready | 3-12 tháng | valuation |
| V02 | Book-to-Price Residual Value | B | Ready | 6-18 tháng | valuation |
| V03 | Operating Cash-Flow Yield | B | Probe | 3-12 tháng | valuation/cash |
| V04 | Free-Cash-Flow Yield | A-INT | Probe | 6-18 tháng | valuation/investment |
| V05 | Enterprise-Adjusted Earnings Yield | B | Probe | 6-18 tháng | valuation/distress |
| E06 | Standardized EPS Surprise | A-INT | Probe | 4-12 tuần | earnings event |
| E07 | Asset-Scaled PAT Surprise | B | Probe | 4-16 tuần | earnings event |
| E08 | Operating Cash-Flow Surprise | B | Probe | 4-16 tuần | cash event |
| E09 | Earnings Acceleration | B | Probe | 1-2 quý | fundamental momentum |
| E10 | Persistent Positive Earnings | B | Ready | 1-4 quý | earnings stability |
| A11 | Cash Earnings Minus Accruals | A-VN/A-INT | Probe | 1-4 quý | accrual |
| A12 | Working-Capital Accrual | A-INT | Probe | 1-4 quý | accrual/WC |
| A13 | Receivables Growth Red Flag | B | Ready | 1-4 quý | accrual/collection |
| A14 | Inventory Growth Red Flag | A-INT | Ready | 1-4 quý | accrual/inventory |
| A15 | Net Operating Assets Bloat | A-INT | Probe | 2-8 quý | balance-sheet accrual |
| Q16 | Return on Assets | A-VN | Ready | 1-4 quý | profitability |
| Q17 | Return on Equity with Solvency Guard | A-VN | Ready | 1-4 quý | profitability/leverage |
| Q18 | Cash Return on Assets | A-INT | Probe | 1-4 quý | cash profitability |
| Q19 | Core Operating Profitability | A-INT | Probe | 1-4 quý | operating quality |
| Q20 | Piotroski Small-Cap Anti-Junk | A-VN | Probe | 2-4 quý | composite quality |
| I21 | Conservative Asset Growth | A-INT | Ready | 2-8 quý | investment |
| I22 | Conservative Equity Growth | B | Ready | 2-8 quý | investment/financing |
| I23 | Capex Shock and Overinvestment | A-INT | Probe | 2-8 quý | capex |
| I24 | Construction-in-Progress Buildup | C | Ready | 2-8 quý | project execution |
| I25 | Goodwill Expansion Penalty | B | Ready | 2-8 quý | acquisition quality |
| F26 | Anti-Dilution / Net Share Issuance | A-INT | Probe | 2-8 quý | equity financing |
| F27 | Net Debt Issuance | B | Probe | 1-4 quý | debt financing |
| F28 | External-Financing Dependence | A-INT | Probe | 1-4 quý | funding quality |
| F29 | Debt Repayment Discipline | B | Probe | 1-4 quý | deleveraging |
| F30 | Net Payout Yield | A-INT | Probe | 2-8 quý | payout |
| B31 | Net-Cash Balance-Sheet Strength | B | Ready | 1-4 quý | solvency |
| B32 | Current-Ratio Improvement | A-VN | Ready | 1-4 quý | short-term liquidity |
| B33 | Quick-Ratio Improvement | B | Ready | 1-4 quý | liquid working capital |
| B34 | Leverage Improvement | A-VN | Ready | 1-4 quý | distress |
| B35 | Cash Interest Coverage | A-INT | Probe | 1-4 quý | debt service |
| P36 | 52-Week-High Anchoring | A-VN | Ready | 1-6 tháng | behavioral anchor |
| P37 | Intermediate 12-2 Momentum | B | Ready | 1-6 tháng | price momentum |
| P38 | One-Week Reversal | A-VN | Ready | 1-4 tuần | price correction |
| P39 | VN30-Residual Momentum | B | Experimental | 1-6 tháng | stock-specific trend |
| P40 | Gradual Information / Path Consistency | B | Ready | 1-6 tháng | smooth momentum |
| R41 | Low Idiosyncratic Volatility | A-VN | Experimental | 1-3 tháng | residual risk |
| R42 | Low Beta | B | Experimental | 1-6 tháng | benchmark beta |
| R43 | Downside-Beta Resilience | B | Experimental | 1-6 tháng | downside risk |
| R44 | Anti-Lottery Maximum Return | A-INT | Ready | 1-3 tháng | lottery demand |
| R45 | Liquid Low-Correlation Diversifier | C | Experimental | 1-3 tháng | benchmark correlation |
| L46 | Low 12-Month Turnover | A-VN | Probe | 6-12 tháng | speculative attention |
| L47 | High One-Month Abnormal Turnover | A-VN | Probe | 1-4 tuần | attention continuation |
| L48 | Moderate Amihud Illiquidity Premium | A-VN | Ready | 1-3 tháng | liquidity level |
| L49 | Systematic Liquidity-Shock Exposure | B | Experimental | 1-3 tháng | liquidity beta |
| L50 | Volume-Conditioned Momentum State | A-INT | Experimental | 1-6 tháng | volume/trend interaction |

## 5. Idea cards chi tiết

### Family V: Valuation

#### V01. Positive Earnings-to-Price

- **Cơ chế:** nhà đầu tư trả giá quá thấp cho earnings hiện hữu; tại Việt Nam EP thắng BM và CP trong regression chung.
- **Prototype:** `rank_cs(positive(EPS) / close)`; bản robust dùng `PAT / (close * common_shares)` và chỉ nhận khi hai định nghĩa đồng thuận.
- **Fields:** EPS, PAT, close, common shares.
- **Thiết kế:** lag point-in-time; winsorize numerator/denominator; không thưởng earnings âm chỉ vì ratio âm cực đoan.
- **Orthogonality:** champion mặc định của valuation; V02-V05 chỉ được thay thế nếu có incremental OOS alpha.
- **Failure mode:** value trap, stale earnings, split làm sai EPS/share count.

#### V02. Book-to-Price Residual Value

- **Cơ chế:** book equity là claim chậm thay đổi hơn earnings; có thể bắt recovery/deep value mà EP bỏ lỡ.
- **Prototype:** `owners_equity / (close * common_shares)`, sau đó residualize cross-sectionally với V01 rank để chỉ giữ phần BM không trùng EP.
- **Fields:** owners equity, close, common shares.
- **Thiết kế:** equity phải dương; loại tail ratio do giá quá thấp/stale; rebalance theo report.
- **Orthogonality:** chỉ đáng giữ nếu residual BM có PnL khác V01; bằng chứng Việt Nam nói raw BM không incremental.
- **Failure mode:** book value chất lượng thấp, goodwill lớn, tài sản khó thanh lý.

#### V03. Operating Cash-Flow Yield

- **Cơ chế:** cash flow khó bị accrual manipulation hơn PAT và có thể định giá doanh nghiệp cyclically depressed.
- **Prototype:** trailing CFO / market-value proxy; ưu tiên positive CFO và dùng median/rank thay vì ratio raw.
- **Fields:** CFO, close, common shares.
- **Thiết kế:** probe dấu của CFO; ghép bốn quý nếu quarterly field là discrete-quarter, không cộng nếu field là YTD.
- **Orthogonality:** có thể overlap A11/Q18; chọn valuation expression hoặc quality expression, không dùng cả hai vô điều kiện.
- **Failure mode:** working-capital release tạm thời làm CFO đẹp giả.

#### V04. Free-Cash-Flow Yield

- **Cơ chế:** cash còn lại sau đầu tư duy trì là nguồn phân phối/giảm nợ; tránh công ty earnings tốt nhưng hút vốn liên tục.
- **Prototype:** `(CFO - abs(capex_purchase)) / market_value` sau khi xác minh sign convention.
- **Fields:** CFO, purchases of fixed assets, close, common shares.
- **Thiết kế:** dùng trailing four-quarter FCF; capex âm/dương được chuẩn hóa bằng probe; cho phép sector-neutrality gián tiếp bằng rank coverage nếu cần.
- **Orthogonality:** cầu nối valuation-investment; kỳ vọng correlation với I23 cao hơn V01.
- **Failure mode:** phạt growth capex có NPV dương; cash timing theo quý.

#### V05. Enterprise-Adjusted Earnings Yield

- **Cơ chế:** hai doanh nghiệp cùng market cap nhưng đòn bẩy khác nhau không có cùng mức rẻ; điều chỉnh debt và cash giảm value-trap distress.
- **Prototype:** `PAT / (market_value + short_loans + long_loans - cash)`; denominator phải dương.
- **Fields:** PAT, close, common shares, short/long loans, cash.
- **Thiết kế:** winsorize enterprise-value proxy; thử pre-tax profit để giảm ảnh hưởng tax one-off.
- **Orthogonality:** hybrid valuation-distress; không giữ cùng V01 và B34 nếu PnL cluster hội tụ.
- **Failure mode:** debt fields thiếu ngoài doanh nghiệp công nghiệp; cash bị restricted nhưng vẫn được tính.

### Family E: Earnings information diffusion

#### E06. Standardized EPS Surprise

- **Cơ chế:** small firms/low coverage phản ứng chậm với earnings news; PEAD thường mạnh hơn khi arbitrage cost cao.
- **Prototype:** `(EPS_q - EPS_q-4) / rolling_std(EPS_q - EPS_q-4, 8 quarters)`; giữ event memory 20-60 phiên.
- **Fields:** quarterly EPS, close, volume.
- **Thiết kế:** phát hiện update point-in-time; thử delay 0/1/3/5 ngày để bác bỏ leakage; không cần ngày công bố riêng nếu update đúng PIT.
- **Orthogonality:** event signal, khác level valuation V01.
- **Failure mode:** platform backfill, EPS split adjustment, denominator variance quá nhỏ.

#### E07. Asset-Scaled PAT Surprise

- **Cơ chế:** PAT innovation tránh nhiễu per-share từ issuance/split và phù hợp công ty có EPS coverage kém.
- **Prototype:** `(PAT_q - PAT_q-4) / lag(total_assets_q)`; rank theo cross-section, có sign-consistency với EPS nếu EPS tồn tại.
- **Fields:** quarterly PAT, total assets, EPS.
- **Thiết kế:** assets dương; winsorize; tách positive turnaround khỏi deterioration.
- **Orthogonality:** substitute cho E06, nhưng có thể thắng ở coverage rộng hơn.
- **Failure mode:** seasonal quarter mismatch, extraordinary gains, financial firms có asset scale khác.

#### E08. Operating Cash-Flow Surprise

- **Cơ chế:** cash news ít phụ thuộc accounting estimate hơn earnings news; có thể là catalyst riêng khi PAT chưa đổi.
- **Prototype:** `(CFO_q - CFO_q-4) / lag(total_assets_q)` với event decay 20-80 phiên.
- **Fields:** quarterly CFO, total assets, PAT.
- **Thiết kế:** xác minh YTD-vs-discrete và sign; long positive CFO innovation, ưu tiên khi PAT không xấu.
- **Orthogonality:** cash-event sleeve, kỳ vọng correlation thấp hơn với price momentum nhưng cao với Q18.
- **Failure mode:** working-capital timing, tax/payment seasonality.

#### E09. Earnings Acceleration

- **Cơ chế:** thị trường extrapolate level/growth nhưng phản ứng chậm với thay đổi của tốc độ tăng trưởng.
- **Prototype:** `[(PAT_q-PAT_q-4)/assets_lag] - [(PAT_q-1-PAT_q-5)/assets_lag2]`; EPS version là robustness check.
- **Fields:** quarterly PAT, EPS, total assets.
- **Thiết kế:** dùng differences scaled thay vì percentage growth quanh zero; giữ 1-2 quý.
- **Orthogonality:** second-difference signal, khác surprise level E06/E07.
- **Failure mode:** acceleration cực lớn do base effect; noisy hơn PEAD.

#### E10. Persistent Positive Earnings

- **Cơ chế:** một đồng earnings bền có giá trị hơn earnings biến động; quality expectation có thể được phản ánh chậm ở small-cap.
- **Prototype:** mean asset-scaled PAT 8 quý trừ penalty cho rolling std và số quý âm.
- **Fields:** quarterly PAT, total assets.
- **Thiết kế:** dùng rank of stability, không tối ưu coefficient; rebalance theo quý.
- **Orthogonality:** earnings-state signal, ít event-like hơn E06-E09.
- **Failure mode:** ổn định do accounting smoothing; bỏ lỡ cyclical turnarounds.

### Family A: Accrual và working-capital quality

#### A11. Cash Earnings Minus Accruals

- **Cơ chế:** cash component của earnings bền hơn accrual component; accrual anomaly cũng đã được ghi nhận trong literature Việt Nam.
- **Prototype:** `(CFO - PAT) / lag(total_assets)`; rank cao là cash realization tốt.
- **Fields:** CFO, PAT, total assets.
- **Thiết kế:** probe sign; annual version làm anchor, quarterly version làm update; winsorize mạnh.
- **Orthogonality:** core accounting-quality primitive; Q20 chỉ làm filter nếu correlation cao.
- **Failure mode:** CFO tạm tăng do kéo payables hoặc giảm inventory không bền.

#### A12. Working-Capital Accrual

- **Cơ chế:** accrual có reliability thấp hơn dự báo earnings persistence thấp hơn; WC accrual cô lập phần operating estimate.
- **Prototype:** `-(delta(receivables)+delta(inventory)+delta(prepayments)-delta(payables))/lag(assets)`; dùng cash-flow WC fields để cross-check dấu.
- **Fields:** receivables, inventory, prepayments, trade payables; CF changes in receivables/inventories/payables.
- **Thiết kế:** high negative accrual được thưởng; require component coverage tối thiểu; không thay missing bằng zero.
- **Orthogonality:** granular hơn A11; chỉ giữ cả hai khi A12 residualized còn alpha.
- **Failure mode:** growth thật làm WC tăng; cash-flow statement sign convention.

#### A13. Receivables Growth Red Flag

- **Cơ chế:** receivables tăng nhanh hơn asset base có thể báo collection risk hoặc revenue recognition quá sớm.
- **Prototype:** `-delta_yoy(accounts_receivable) / lag(assets)`; xác nhận bằng CF change in receivables.
- **Fields:** accounts receivable, total assets, CF increase/decrease in receivables.
- **Thiết kế:** chỉ phạt spike có PAT dương nhưng CFO yếu; raw signal vẫn được test riêng để tránh interaction mining.
- **Orthogonality:** collection-quality subfactor, có thể thấp correlation với inventory A14.
- **Failure mode:** credit sales hợp lý trong giai đoạn mở rộng; field definition khác ngành.

#### A14. Inventory Growth Red Flag

- **Cơ chế:** Thomas và Zhang cho thấy inventory change giải thích phần quan trọng của accrual anomaly; buildup có thể báo demand slowdown.
- **Prototype:** `-delta_yoy(inventories_net) / lag(assets)`; confirm bằng CF inventory change.
- **Fields:** inventories net, total assets, CF increase/decrease in inventories.
- **Thiết kế:** không thay missing inventory của service firms bằng zero; mask theo availability tự nhiên.
- **Orthogonality:** operating-cycle risk khác receivables; vẫn thuộc accrual cluster.
- **Failure mode:** commodity stocking có lợi, seasonal build, accounting reclassification.

#### A15. Net Operating Assets Bloat

- **Cơ chế:** accumulated operating accruals trên balance sheet tạo `balance-sheet bloat`; NOA cao dự báo return thấp trong nghiên cứu quốc tế.
- **Prototype:** `-[(total_assets-cash-short_investments) - (liabilities-short_loans-long_loans)] / lag(total_assets)`.
- **Fields:** total assets, cash, short investments, liabilities, short/long loans.
- **Thiết kế:** test cả level và change nhưng đăng ký trước một primary definition; denominator dương.
- **Orthogonality:** stock measure của accumulated accrual, khác flow measure A11/A12.
- **Failure mode:** classification không đồng nhất; debt/liability fields thiếu làm NOA sai.

### Family Q: Profitability và business quality

#### Q16. Return on Assets

- **Cơ chế:** profitable firms có expected return cao hơn; ROA có bằng chứng trong cross-section Việt Nam.
- **Prototype:** trailing PAT / average total assets; positive-only mask optional nhưng phải pre-register.
- **Fields:** PAT, total assets.
- **Thiết kế:** average beginning/end assets; annual anchor để giảm quarterly seasonality.
- **Orthogonality:** profitability level; substitute gần với Q18/Q19.
- **Failure mode:** asset-light và financial firms không so sánh trực tiếp; one-off PAT.

#### Q17. Return on Equity with Solvency Guard

- **Cơ chế:** hiệu quả trên vốn chủ có thể nhận diện compounder, nhưng ROE cao do equity mỏng phải bị loại.
- **Prototype:** PAT / average owners equity, chỉ khi equity dương và liabilities/assets dưới tail threshold.
- **Fields:** PAT, owners equity, liabilities, total assets.
- **Thiết kế:** rank ROE sau solvency mask; không cộng leverage penalty vào score để giữ interpretability.
- **Orthogonality:** có leverage exposure hơn Q16; dùng như challenger, không mặc định giữ cùng ROA.
- **Failure mode:** buyback/accumulated losses làm denominator nhỏ; cyclical peak.

#### Q18. Cash Return on Assets

- **Cơ chế:** cash-based profitability có thể subsume cả profitability có accrual và accrual anomaly.
- **Prototype:** trailing CFO / average total assets.
- **Fields:** CFO, total assets.
- **Thiết kế:** annual/Q4 rolling consistency; loại working-capital release cực đoan bằng winsorization.
- **Orthogonality:** quality interpretation của cash flow; V03 là valuation interpretation nên thường là substitute.
- **Failure mode:** cash timing; không phân biệt maintenance capex.

#### Q19. Core Operating Profitability

- **Cơ chế:** operating result trước thay đổi working capital cô lập core operation tốt hơn PAT chịu tax, financing và one-off.
- **Prototype:** operating profit/loss before WC changes / lag total assets.
- **Fields:** CF operating profit before changes in WC, total assets, PAT.
- **Thiết kế:** require sign agreement với PAT hoặc báo riêng disagreement portfolio; probe coverage.
- **Orthogonality:** profitability core, kỳ vọng ít exposure tới financing hơn ROE.
- **Failure mode:** cash-flow reconciliation field khác nghĩa theo reporter; financial firms.

#### Q20. Piotroski Small-Cap Anti-Junk

- **Cơ chế:** fundamental strength đặc biệt hữu ích ở small/mid-cap và low coverage; kiểm định Việt Nam cho thấy F-score phân tách mạnh winners/losers.
- **Prototype:** score từ positive ROA, positive CFO, CFO>PAT, improving ROA, falling leverage, improving current ratio và no dilution; dùng 7 component khả dụng nhất thay vì giả đủ chín.
- **Fields:** PAT, CFO, assets, loans/liabilities, current assets/liabilities, common shares.
- **Thiết kế:** missing component không tính là fail; yêu cầu tối thiểu 5 component; test standalone và overlay riêng.
- **Orthogonality:** composite nên dễ overlap A11/B32/B34/F26; thường tốt nhất làm anti-junk mask.
- **Failure mode:** double counting nếu vừa là alpha vừa là filter cho mọi alpha.

### Family I: Investment và capital allocation

#### I21. Conservative Asset Growth

- **Cơ chế:** aggressive asset growth có thể phản ánh overinvestment/extrapolation; conservative investment là trụ cột của q/FF5 logic.
- **Prototype:** `-delta_yoy(total_assets) / lag(total_assets)`.
- **Fields:** total assets quarterly/annual.
- **Thiết kế:** không thưởng shrinkage distress; require PAT hoặc CFO không ở bottom tail.
- **Orthogonality:** core investment primitive, khác valuation và price behavior.
- **Failure mode:** phạt firm có growth opportunity thật; merger/reclassification.

#### I22. Conservative Equity Growth

- **Cơ chế:** equity base tăng nhanh có thể kết hợp retained earnings, issuance và acquisition accounting; return predictability khác pure share issuance.
- **Prototype:** `-delta_yoy(owners_equity) / lag(abs(owners_equity))`, equity dương ở cả hai kỳ.
- **Fields:** owners equity, paid-in capital, common shares.
- **Thiết kế:** phân rã change thành earned vs contributed capital trong diagnostics.
- **Orthogonality:** gần I21/F26; chỉ giữ nếu residual equity growth còn alpha.
- **Failure mode:** retained earnings tích lũy tốt cũng làm equity tăng; denominator nhỏ.

#### I23. Capex Shock and Overinvestment

- **Cơ chế:** investment tăng bất thường thường đi trước lower abnormal returns nếu management overinvest hoặc market extrapolate growth.
- **Prototype:** âm của current trailing capex/assets trừ baseline 3 năm; capex dùng absolute cash outflow sau sign probe.
- **Fields:** purchases of fixed assets, total assets.
- **Thiết kế:** test shock thay vì level để không phạt business model vốn nặng cố hữu.
- **Orthogonality:** flow investment, khác balance-sheet growth I21.
- **Failure mode:** project NPV dương; lumpy capex; dữ liệu quý YTD.

#### I24. Construction-in-Progress Buildup

- **Cơ chế:** CIP tăng kéo dài mà earnings/CFO không theo kịp có thể báo delay, cost overrun hoặc capital trapping.
- **Prototype:** `-delta_yoy(CIP)/lag(assets)`; primary signal là buildup level, diagnostics đo PAT/CFO response.
- **Fields:** construction in progress, total assets, PAT, CFO.
- **Thiết kế:** chỉ dùng nơi field có coverage; không dùng zero-imputation.
- **Orthogonality:** project-execution hypothesis, có thể khác capex shock vì CIP là stock chưa hoàn thành.
- **Failure mode:** dự án tốt đang ở giai đoạn xây dựng; low breadth.

#### I25. Goodwill Expansion Penalty

- **Cơ chế:** goodwill tăng mạnh có thể đại diện acquisition overpayment và managerial empire building; future impairment là delayed recognition.
- **Prototype:** `-delta_yoy(goodwill)/lag(assets)`; optional quality guard bằng CFO/PAT.
- **Fields:** goodwill, total assets.
- **Thiết kế:** sparse signal chỉ active khi goodwill thay đổi; không rank missing như zero.
- **Orthogonality:** acquisition-quality sleeve, kỳ vọng event timing khác asset growth.
- **Failure mode:** acquisition tạo synergy thật; accounting treatment không đồng nhất.

### Family F: Financing và payout policy

#### F26. Anti-Dilution / Net Share Issuance

- **Cơ chế:** managers có thể issue equity khi overpriced; dilution làm giảm claim trên mỗi cổ phần.
- **Prototype:** âm của YoY common-share growth; confirm bằng proceeds from share issuance / assets.
- **Fields:** common shares, proceeds from issue of shares, total assets, paid-in capital.
- **Thiết kế:** phát hiện split bằng price/share discontinuity; cash issuance là primary khi coverage tốt.
- **Orthogonality:** equity-financing primitive, khác asset growth dù thường tương quan.
- **Failure mode:** rights issue tài trợ dự án tốt; stock split giả issuance.

#### F27. Net Debt Issuance

- **Cơ chế:** vay ròng cao có thể báo financing need, market timing hoặc future balance-sheet stress.
- **Prototype:** `-(borrowings_proceeds - repayments) / lag(assets)`.
- **Fields:** proceeds from borrowings, repayment of borrowings, total assets.
- **Thiết kế:** chuẩn hóa dấu và magnitude; dùng annual anchor; tách zero-activity khỏi missing.
- **Orthogonality:** debt-financing, khác dilution F26.
- **Failure mode:** debt tài trợ project có return cao; refinancing rollover không làm debt stock tăng.

#### F28. External-Financing Dependence

- **Cơ chế:** investment/operation phải dựa vào vốn ngoài do internal cash generation yếu là dấu hiệu funding fragility.
- **Prototype:** âm của `(net_debt_issuance + equity_issuance - CFO) / lag(assets)`; pre-register treatment của CFO âm.
- **Fields:** borrowings, repayments, share issuance, CFO, assets.
- **Thiết kế:** cap từng component trước khi cộng; test residual sau A11 để biết alpha có chỉ là accrual không.
- **Orthogonality:** interaction funding-quality, không đơn thuần debt hay equity issuance.
- **Failure mode:** financing đi trước growth tốt; Bradshaw et al. lưu ý relation suy yếu sau khi kiểm soát accrual.

#### F29. Debt Repayment Discipline

- **Cơ chế:** khả năng trả nợ bằng dòng tiền thay vì roll-over phản ánh deleveraging thực và governance tốt.
- **Prototype:** `(repayments - new_borrowings) / lag(total_loans)`, chỉ khi prior debt dương; secondary confirmation là loan stock giảm.
- **Fields:** repayment, proceeds from borrowings, short/long loans.
- **Thiết kế:** probe sign; tránh thưởng firm không có debt như một repayment signal.
- **Orthogonality:** change/action signal, khác leverage level B34.
- **Failure mode:** repayment bắt buộc làm cạn cash; debt stock classification changes.

#### F30. Net Payout Yield

- **Cơ chế:** dividends và repurchases là cash returned; trừ issuance giúp đo distribution thực thay vì dividend yield đơn lẻ.
- **Prototype:** `(abs(dividends_paid)+abs(repurchases)-share_issuance) / market_value` sau sign probe.
- **Fields:** dividends paid, share returns/repurchases, issue of shares, close, common shares.
- **Thiết kế:** trailing annual flow; require market value dương; report coverage của repurchase field.
- **Orthogonality:** payout/capital-return sleeve, có thể âm correlation với external financing F28.
- **Failure mode:** high payout do thiếu growth; repurchase field sparse tại Việt Nam.

### Family B: Balance-sheet resilience

#### B31. Net-Cash Balance-Sheet Strength

- **Cơ chế:** cash cushion giảm distress và cho phép small-cap sống qua funding shock mà không dilute.
- **Prototype:** `(cash - short_loans - long_loans) / total_assets`.
- **Fields:** cash, short/long loans, total assets.
- **Thiết kế:** cash và assets dương; test level và change nhưng primary là level.
- **Orthogonality:** solvency state, thường ít event-like; có thể overlap low beta/quality.
- **Failure mode:** idle cash và agency problem; restricted cash; debt coverage thiếu.

#### B32. Current-Ratio Improvement

- **Cơ chế:** cải thiện khả năng đáp ứng current liabilities là một component kinh điển của F-score và đặc biệt quan trọng với small-cap.
- **Prototype:** delta YoY của `current_assets/current_liabilities`.
- **Fields:** current assets, current liabilities.
- **Thiết kế:** denominator dương; cap ratio; dùng improvement thay level để giảm sector bias.
- **Orthogonality:** short-term liquidity trend, khác net cash level B31.
- **Failure mode:** inventory/receivable kém chất lượng làm current assets đẹp giả.

#### B33. Quick-Ratio Improvement

- **Cơ chế:** bỏ inventory và prepayments khỏi current assets tạo thước đo thanh khoản nghiêm hơn current ratio.
- **Prototype:** delta YoY của `(current_assets-inventory-prepayments)/current_liabilities`.
- **Fields:** current assets/liabilities, inventory net, short-term prepayments.
- **Thiết kế:** require component coverage; không thay missing bằng zero; cap ratio.
- **Orthogonality:** substitute cho B32; chỉ incremental khi working-capital composition quan trọng.
- **Failure mode:** service/financial firms; receivables vẫn có thể kém chất lượng.

#### B34. Leverage Improvement

- **Cơ chế:** distress stocks thường có high volatility nhưng low realized return; giảm leverage có thể tránh distress anomaly.
- **Prototype:** âm delta YoY của `(short_loans+long_loans)/assets`; liabilities/assets làm robustness definition.
- **Fields:** loans, liabilities, assets.
- **Thiết kế:** primary dùng interest-bearing loans; level guard để change nhỏ trên debt cực cao không được ưu tiên quá mức.
- **Orthogonality:** leverage trend, khác debt action F27/F29.
- **Failure mode:** giảm debt vì không vay được; assets write-down làm ratio tăng giả.

#### B35. Cash Interest Coverage

- **Cơ chế:** khả năng trả interest từ operating cash flow đo debt-service capacity gần cash hơn accounting EBIT coverage.
- **Prototype:** `CFO / abs(interest_paid)`; long positive/high coverage, cap denominator và ratio.
- **Fields:** CFO, interest paid, loans.
- **Thiết kế:** chỉ active khi interest/debt có materiality; zero interest không mặc định là vô hạn.
- **Orthogonality:** cash debt-service sleeve, khác net cash và leverage.
- **Failure mode:** quarterly payment timing; capitalized interest; interest field sign/sparsity.

### Family P: Price-path behavior

#### P36. 52-Week-High Anchoring

- **Cơ chế:** nhà đầu tư neo vào đỉnh cũ và phản ứng chậm; tại Việt Nam signal này mạnh hơn raw momentum trong nhiều specification.
- **Prototype:** `close / rolling_max(close, 250)`; high-based version làm robustness test.
- **Fields:** close, high, volume.
- **Thiết kế:** liquidity floor; loại one-day price-limit exhaustion bằng turnover/range diagnostic, không nhồi vào primary formula.
- **Orthogonality:** behavioral anchor; có thể bổ sung EP value do value-momentum thường tương quan thấp/âm.
- **Failure mode:** momentum crash và regime reversal.

#### P37. Intermediate 12-2 Momentum

- **Cơ chế:** gradual information diffusion ở firm nhỏ/coverage thấp; bỏ tháng gần nhất để giảm short reversal.
- **Prototype:** cumulative return từ khoảng 12 tháng đến 1 tháng trước; thử 6-1 như robustness, không gọi là idea mới.
- **Fields:** close.
- **Thiết kế:** primary 250-to-20 trading days; require đủ lịch sử; residualize market chỉ trong P39.
- **Orthogonality:** raw trend; bằng chứng Việt Nam mixed nên là challenger, không default champion.
- **Failure mode:** momentum crash, price limits và stale observations.

#### P38. One-Week Reversal

- **Cơ chế:** temporary price pressure/overreaction đảo chiều; tại Việt Nam bottom prior-week return có positive next-week alpha sau VN-4.
- **Prototype:** âm cumulative return 5 phiên trước; rebalance tuần, hold 1-4 tuần theo decay test.
- **Fields:** close, volume.
- **Thiết kế:** loại earnings/news shock bằng fundamental-update flag nếu có; liquidity floor.
- **Orthogonality:** kỳ vọng thấp hoặc âm với P36/P37; tiềm năng portfolio diversifier cao.
- **Failure mode:** bắt falling knife khi thông tin xấu tiếp tục khuếch tán; turnover cao.

#### P39. VN30-Residual Momentum

- **Cơ chế:** loại broad-market move để giữ stock-specific information diffusion, giảm beta contamination.
- **Prototype:** rolling regression/covariance để ước lượng beta với VN30; cộng residual returns trên 6-1 hoặc 12-2 tháng.
- **Fields:** stock close, VN30 close.
- **Thiết kế:** beta window đủ dài, shrink beta về 1, kiểm tra nonsynchronous trading.
- **Orthogonality:** residual trend có thể thấp correlation với market beta R42 và raw P37.
- **Failure mode:** beta estimate nhiễu ở illiquid names; VN30 không phải exact small-cap market factor.

#### P40. Gradual Information / Path Consistency

- **Cơ chế:** cùng một cumulative return, đường đi gồm nhiều bước nhỏ có thể đại diện gradual information tốt hơn một cú jump do attention.
- **Prototype:** signed return strength nhân với tỷ lệ ngày residual return cùng chiều, đồng thời phạt maximum one-day contribution.
- **Fields:** close, VN30 close.
- **Thiết kế:** primary 60-120 ngày; không dùng viewport/window variants như idea mới; cap jump penalty.
- **Orthogonality:** path-shape factor, khác total momentum level.
- **Failure mode:** drift rất mượt có thể do stale prices; cần volume/value floor.

### Family R: Risk, lottery demand và benchmark exposure

#### R41. Low Idiosyncratic Volatility

- **Cơ chế:** short-sale constraints và lottery preference có thể làm high-IVOL stocks overpriced; size-neutral IVOL có bằng chứng tại Việt Nam.
- **Prototype:** âm rolling std của residual return sau beta VN30.
- **Fields:** stock close, VN30 close.
- **Thiết kế:** 60-120 ngày, minimum observations, shrink beta; liquidity mask để tránh stale-price low-vol giả.
- **Orthogonality:** risk/lottery cluster, có thể overlap L46 và R44.
- **Failure mode:** literature replication quốc tế mixed; estimation noise và low-vol crash.

#### R42. Low Beta

- **Cơ chế:** leverage constraints có thể làm low-beta assets có risk-adjusted return cao hơn security market line.
- **Prototype:** âm rolling covariance(stock,VN30)/variance(VN30), beta shrink về cross-sectional median.
- **Fields:** stock close, VN30 close.
- **Thiết kế:** đủ observations; stale-return correction; evaluate alpha lẫn beta-adjusted drawdown.
- **Orthogonality:** systematic exposure, khác residual volatility R41 về mặt định nghĩa.
- **Failure mode:** recent research cho thấy microcap exposure có thể phóng đại BAB; không được bỏ capacity control.

#### R43. Downside-Beta Resilience

- **Cơ chế:** nhà đầu tư quan tâm covariance khi market giảm hơn covariance bình thường; low downside capture có thể là defensive sleeve.
- **Prototype:** beta chỉ trên ngày VN30 return âm/bottom quantile; signal ưu tiên thấp hơn normal beta sau khi kiểm soát R42.
- **Fields:** stock close, VN30 close.
- **Thiết kế:** window dài hơn beta thường; require số ngày downside tối thiểu; xem đây là risk diversifier trước khi gọi alpha.
- **Orthogonality:** tail-state exposure, mục tiêu giảm portfolio drawdown hơn là tối đa standalone return.
- **Failure mode:** downside beta premium trong lý thuyết có thể thưởng high downside risk; low beta chưa chắc có positive alpha.

#### R44. Anti-Lottery Maximum Return

- **Cơ chế:** retail investors trả quá cao cho payoff giống lottery; maximum daily return tháng trước dự báo future return thấp trong nghiên cứu gốc.
- **Prototype:** âm `rolling_max(daily_return, 20)`; optional average top-3 returns để giảm one-tick noise.
- **Fields:** close, high, volume.
- **Thiết kế:** loại stale/zero-price artifacts; kiểm tra price-limit saturation; rebalance tháng.
- **Orthogonality:** tail-shape signal, khác std R41 dù hai tín hiệu có thể correlated.
- **Failure mode:** large replication study không xác nhận ổn định; có thể chỉ là IVOL/illiquidity proxy.

#### R45. Liquid Low-Correlation Diversifier

- **Cơ chế:** trong portfolio objective, stock có low rolling correlation với VN30 có thể giảm common drawdown nếu low correlation là thật chứ không do stale price.
- **Prototype:** âm rolling correlation(stock return,VN30), chỉ trong middle/high liquidity band và positive own variance.
- **Fields:** stock/VN30 close, volume, common shares.
- **Thiết kế:** 60-120 ngày; exclude near-zero volume/return; require downside-correlation cũng thấp.
- **Orthogonality:** trực tiếp nhắm portfolio covariance; evidence tier C vì expected-return thesis yếu.
- **Failure mode:** correlation hội tụ về 1 trong stress; low correlation do idiosyncratic distress.

### Family L: Liquidity, attention và trading pressure

#### L46. Low 12-Month Turnover

- **Cơ chế:** tại Việt Nam high turnover phản ánh speculative attention/overpricing hơn là chỉ liquidity; effect mạnh hơn ở smaller firms.
- **Prototype:** âm average daily `volume/common_shares` trong 250 phiên.
- **Fields:** volume, common shares, close.
- **Thiết kế:** dùng capacity band: loại đáy tuyệt đối về turnover/value; share count PIT và split-aware.
- **Orthogonality:** VN-4 core factor; có thể subsume nhiều price/risk anomaly nên không mặc định giữ cùng R41/R44.
- **Failure mode:** low-turnover tail không giao dịch được; stale-price bias.

#### L47. High One-Month Abnormal Turnover

- **Cơ chế:** khác L46: ratio turnover 20 ngày/250 ngày cao báo attention shock và trong nghiên cứu Việt Nam top quintile có positive alpha sau VN-4.
- **Prototype:** `mean(turnover,20) / mean(turnover,250)`; long high abnormal turnover, không đảo dấu.
- **Fields:** volume, common shares.
- **Thiết kế:** cap extreme events; kiểm tra continuation decay 1-4 tuần; không nhầm với reversal.
- **Orthogonality:** short-horizon continuation quanh baseline long-term; raw correlation với L46 có thể thấp vì một cái level, một cái shock.
- **Failure mode:** pump-and-dump/exhaustion; issuance/listing event làm baseline méo.

#### L48. Moderate Amihud Illiquidity Premium

- **Cơ chế:** price impact trên dollar volume đo compensation cho illiquidity; bằng chứng Việt Nam tồn tại nhưng turnover có thể subsume một phần.
- **Prototype:** average `abs(return)/(close*volume)` trong 20-60 ngày; long quantile illiquid vừa phải, loại extreme tail.
- **Fields/features:** close, volume, `amihud_illiquidity_panel`.
- **Thiết kế:** capacity band, minimum trading value và max position; report gross và cost-adjusted PnL.
- **Orthogonality:** liquidity level, substitute gần với L46.
- **Failure mode:** paper return không executable; zeros, price limits và stale observations.

#### L49. Systematic Liquidity-Shock Exposure

- **Cơ chế:** expected return có thể bù cho covariance với aggregate liquidity, không chỉ own illiquidity level.
- **Prototype:** beta của stock return hoặc own-liquidity change với VN30 liquidity shock dựng từ VN30 Amihud/volume; test long moderate high-risk premium.
- **Fields:** stock/VN30 OHLCV, Amihud feature, rolling covariance.
- **Thiết kế:** innovation của benchmark liquidity phải demean/standardize; estimation window dài; tránh cùng lúc tối ưu sign và window.
- **Orthogonality:** systematic liquidity risk, khác cross-sectional level L48.
- **Failure mode:** VN30 liquidity không đại diện total market; high beta names khó trade đúng lúc stress.

#### L50. Volume-Conditioned Momentum State

- **Cơ chế:** Lee và Swaminathan cho thấy past volume giúp phân biệt momentum life cycle; low-volume winners có thể tiếp tục, high-volume winners dễ tiến gần reversal/glamour state.
- **Prototype:** state machine từ momentum rank và long-horizon turnover rank: long low-volume winners; short/underweight high-volume losers hoặc exhaustion state theo pre-registered table.
- **Fields:** close, volume, common shares.
- **Thiết kế:** đăng ký trước bốn states; không fit arbitrary interaction coefficient; test incremental với P37 và L46.
- **Orthogonality:** interaction có mục tiêu decorrelate trend và speculation; chỉ nhận nếu PnL không chỉ là linear sum hai legs.
- **Failure mode:** sample nhỏ theo state, high turnover và state instability.

## 6. Nguồn học thuật theo cơ chế

### Việt Nam

- Huang, Liu & Shu (2023): size, EP, turnover, 52-week high, IVOL, abnormal turnover và reversal. [Paper](https://www.pbcsf.tsinghua.edu.cn/__local/7/F5/A9/E0366D36DF73499C8CBFB66C505_4D50779F_1C1EEF.pdf)
- Hoang & Phan (2019): liquidity được định giá; market-size-value-liquidity model phù hợp hơn các model không có liquidity. [Publication](https://research.monash.edu/en/publications/is-liquidity-priced-in-the-vietnamese-stock-market/)
- Ho et al. (2022): Piotroski F-score có sức phân tách đáng kể trên 622 listed firms Việt Nam giai đoạn 2009-2019. [Publication](https://research-information.bris.ac.uk/en/publications/fundamental-analysis-and-the-use-of-financial-statement-informati/)
- Nghiên cứu momentum HOSE 2017-2022 tìm thấy một số short-horizon specification có hiệu quả, nhưng kết quả xung đột với mẫu dài hơn; vì vậy P37 là Tier B. [Article](https://www.ajeb.edu.vn/vi/article/hieu-ung-momentum-thi-truong-chung-khoan-viet-nam)

### Valuation, quality, accrual và investment

- Sloan (1996): cash earnings bền hơn accrual earnings. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2598)
- Richardson et al. (2005): accrual reliability thấp đi cùng earnings persistence thấp và mispricing lớn hơn. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=521062)
- Thomas & Zhang (2002): inventory change là thành phần quan trọng của accrual anomaly. [Publication](https://ideas.repec.org/a/spr/reaccs/v7y2002i2d10.1023_a1020221918065.html)
- Hirshleifer et al.: net operating assets dự báo future returns âm. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=404120)
- Ball et al. (2016): cash-based operating profitability có thể subsume accrual và profitability có accrual. [Publication](https://ideas.repec.org/a/eee/jfinec/v121y2016i1p28-45.html)
- Novy-Marx: profitability có sức dự báo cross-section tương đương value trong mẫu gốc. [NBER](https://www.nber.org/papers/w15940)
- Fama & French (2015): profitability và conservative investment là hai dimension quan trọng bên cạnh size/value. [Paper](https://www.aea.ru/data/pdf/fama2015.pdf)
- Cooper, Gulen & Schill: total asset growth cao dự báo abnormal return thấp. [Paper](https://onlinelibrary.wiley.com/doi/pdf/10.1111/j.1540-6261.2008.01370.x)
- Titman, Wei & Xie: abnormal capital investment đi cùng future return thấp. [Publication](https://ideas.repec.org/a/cup/jfinqa/v39y2004i04p677-700_00.html)
- Piotroski: F-score đặc biệt hữu ích ở small/mid-cap, low turnover và low coverage. [Paper](https://www.rentables.fr/wp-content/uploads/2011/01/Piotroski_Value-Investing.pdf)

### Financing, distress và payout

- Pontiff & Woodgate: net share issuance dự báo cross-sectional returns. [Publication](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2008.01335.x)
- Bradshaw, Richardson & Sloan: net external financing liên hệ âm với future returns/profitability, nhưng accrual control rất quan trọng. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=904226)
- Butler & Wan: long-run underperformance sau debt issuance có thể biến mất khi kiểm soát stock liquidity; đây là lý do F27 chỉ ở Tier B và phải horse-race trực tiếp với L46/L48. [Paper](https://academic.oup.com/rfs/article-pdf/23/11/3966/24429827/hhq082.pdf)
- Boudoukh et al.: total/net payout yield cung cấp valuation information rộng hơn dividend yield. [Publication](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2007.01226.x)
- Campbell, Hilscher & Szilagyi: financially distressed stocks có realized return thấp dù beta và volatility cao. [Publication](https://campbell.scholars.harvard.edu/publications/search-distress-risk)
- Gu & Lev: overpricing có thể thúc đẩy acquisition kém chất lượng và future goodwill impairment. [Paper](https://doi.org/10.2139/ssrn.1130940)

### Behavior, risk và liquidity

- George & Hwang: 52-week high chứa thông tin khác raw momentum. [Paper](https://onlinelibrary.wiley.com/doi/pdf/10.1111/j.1540-6261.2004.00695.x)
- Hong, Lim & Stein: gradual information diffusion/momentum mạnh hơn ở small và low-coverage firms. [NBER](https://www.nber.org/system/files/working_papers/w6553/w6553.pdf)
- Novy-Marx: recent fundamental performance chứa momentum information khác price momentum, tạo nền tảng cho E08-E10. [NBER](https://www.nber.org/papers/w20984.pdf)
- George, Hwang & Li: 52-week-high anchoring tương tác với PEAD. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2391455)
- Da, Gurun & Warachka: information đến liên tục qua nhiều price move nhỏ tạo momentum bền hơn cùng cumulative return đến từ vài jump lớn, là nền tảng cho P40. [Paper](https://business.uq.edu.au/sites/default/files/events/files/mitch-warachka-paper.pdf)
- Lee & Swaminathan: past volume dự báo magnitude/persistence của momentum và long-run reversal. [DOI](https://doi.org/10.1111/0022-1082.00280)
- Amihud: absolute return trên dollar volume là measure của illiquidity/price impact. [Paper](https://www.cis.upenn.edu/~mkearns/finread/amihud.pdf)
- Acharya & Pedersen: required return phụ thuộc expected liquidity và covariance của return/liquidity với market return/market liquidity, là nền tảng cho L49. [Publication](https://econpapers.repec.org/paper/cprceprdp/4718.htm)
- Ang et al.: high idiosyncratic volatility đi cùng low future returns trong nghiên cứu gốc và international evidence. [Paper](https://www.ruf.rice.edu/~yxing/AHXZ_011906.pdf)
- Bali, Cakici & Whitelaw: maximum daily return đại diện lottery demand và dự báo future return âm trong mẫu gốc. [NBER](https://www.nber.org/papers/w14804.pdf)
- Ang, Chen & Xing: downside covariance là một dimension khác beta thường. [NBER](https://www.nber.org/papers/w11824)
- Asness, Frazzini & Pedersen: quality gồm profitability, growth, safety và payout. [AQR](https://www.aqr.com/Insights/Research/Working-Paper/Quality-Minus-Junk?from=learning)

## 7. Substitute, complement và expected correlation

### Không được xem là 50 independent bets

| Cụm dễ trùng | Primary champion | Challengers/substitutes | Lý do |
|---|---|---|---|
| Valuation | V01 | V02-V05 | cùng cheapness, khác denominator |
| Earnings event | E06 | E07-E09 | cùng report innovation |
| Cash quality | A11 | A12, Q18 | cùng cash-vs-accrual dimension |
| Profitability | Q19 | Q16-Q18 | cùng operating strength |
| Anti-junk | Q20 | B31-B35 | Q20 đã chứa nhiều balance-sheet legs |
| Investment | I21 | I22-I25 | cùng conservative-vs-aggressive investment |
| Financing | F28 | F26-F29 | external funding components chồng lấn |
| Trend | P36 | P37, P39, P40 | cùng gradual price diffusion |
| Lottery/risk | R41 | R42, R44 | high-risk speculative stocks thường đồng cụm |
| Liquidity/attention | L46 | L48, R45 | stale/illiquid exposure dễ tạo correlation giả |

### Complement candidates có cơ sở trước backtest

- V01 EP value với P36 52-week high: value và momentum/anchor thường có covariance thấp hơn các cặp trong cùng style.
- E06 earnings event với P38 reversal: khác horizon và catalyst, nhưng phải loại overlap quanh report.
- A11 accrual quality với P36 price anchor: accounting slow signal so với behavioral medium signal.
- I21 asset growth với L47 abnormal-turnover shock: corporate investment chậm so với attention nhanh.
- B35 interest coverage với P39 residual momentum: balance-sheet resilience và stock-specific price diffusion.

Đây chỉ là prior. Tất cả phải được xác nhận bằng realized PnL correlation.

## 8. Pipeline sinh và tuyển idea

### 8.1. Chuẩn hóa primitive

1. Dựng raw economic quantity đúng dấu.
2. Convert quarterly YTD thành discrete quarter nếu cần; không mặc định.
3. Lag theo point-in-time; chạy delay robustness 0/1/3/5 ngày cho fundamental update.
4. Safe divide; denominator dương/material; missing giữ missing.
5. Cross-sectional winsorize 2%-98% rồi rank.
6. Apply liquidity/capacity mask độc lập với alpha.
7. Dùng `portfolio_weights_panel(method='rank_demean_l1')` hoặc construction tương đương của repo.

### 8.2. Không tạo pseudo-ideas

- Window 20/40/60 cho cùng một primitive là robustness grid, không phải ba idea.
- Annual và quarterly của cùng quantity là anchor/update, không phải hai idea.
- Rank, z-score và winsorized rank là construction choices, không phải alpha mới.
- Thêm quality filter vào mọi signal không biến chúng thành signal mới và có thể làm tất cả alpha tương quan cao.

### 8.3. Test độc lập

Cho mỗi idea:

- Coverage theo ngày, median names và minimum breadth.
- Rank IC, long-short spread và monotonicity theo quintile.
- Gross/net Sharpe, turnover, maximum drawdown, average holding period.
- Parameter plateau, không chỉ best point.
- Subperiod: bull/bear, high/low VN30 volatility, high/low market liquidity.
- Delay test cho fundamentals; stale-price and capacity test cho small-cap.
- Untouched OOS và deflated/multiple-testing-aware significance.

### 8.4. Correlation gate

1. Align daily PnL của mọi candidate trên cùng calendar.
2. Đo full-sample Pearson, Spearman, rolling 63/126-day correlation.
3. Đo downside correlation trên ngày portfolio/VN30 xấu nhất.
4. Đo tail co-loss: xác suất hai alpha cùng ở bottom decile.
5. Đo holdings overlap và signed rank correlation; PnL correlation thấp có thể chỉ do rebalance timing.
6. Cluster distance: `sqrt(0.5 * (1-rho_shrunk))`.
7. Chọn một champion mỗi empirical cluster, không nhất thiết mỗi taxonomy family.
8. Reject candidate nếu `abs(rho) > 0.35` với incumbent mà không tăng OOS Sharpe/giảm drawdown rõ.

Nghiên cứu correlation structure cho thấy nhiều anomaly nén được vào số factor nhỏ hơn rất nhiều; taxonomy 10 họ ở đây chỉ là prior trước khi data-driven clustering. [Geertsema & Lu](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID3666663_code1315714.pdf?abstractid=3002797&mirid=1)

## 9. Hai seed portfolio để bắt đầu

### Seed A: 10 cơ chế, mỗi họ một champion

| Slot | Candidate | Vai trò |
|---|---|---|
| 1 | V01 | Vietnam-specific value |
| 2 | E06 | earnings event |
| 3 | A11 | accrual quality |
| 4 | Q19 | core profitability |
| 5 | I21 | conservative investment |
| 6 | F28 | funding quality |
| 7 | B35 | debt service |
| 8 | P36 | behavioral anchor |
| 9 | R44 | anti-lottery tail shape |
| 10 | L47 | abnormal-attention continuation |

Seed A chỉ là shortlist cho backtest; không equal-weight cả 10 trước correlation gate.

### Seed B: sáu sleeve có prior diversification tốt hơn

1. V01 Positive EP.
2. E06 EPS Surprise.
3. A11 Cash Earnings Minus Accruals.
4. I21 Conservative Asset Growth.
5. P36 52-Week High.
6. P38 One-Week Reversal.

P38 có thể làm short-horizon counterweight cho P36; V01 và P36 tạo value-anchor barbell; ba fundamental sleeves E06/A11/I21 khác nhau về event, accounting quality và corporate investment.

### Weighting

- Bắt đầu bằng equal risk theo sleeve hoặc `1/N` sau volatility scaling hợp lý.
- Không tối ưu trực tiếp sample mean return.
- Covariance optimizer chỉ dùng shrinkage, weight caps và turnover penalty; luôn so với `1/N`.

DeMiguel, Garlappi và Uppal cho thấy optimizer phức tạp thường khó thắng `1/N` ngoài mẫu do estimation error. [Paper](https://www.heisetraining.at/wpblog/wp-content/uploads/2017/10/DeMiguel-et-al.-2009-Optimal-Versus-Naive-Diversification-How-Ineffici.pdf)

## 10. Research order đề xuất

### Wave 1: bằng chứng Việt Nam trực tiếp

1. V01 Positive EP.
2. L46 Low 12-Month Turnover.
3. L47 High One-Month Abnormal Turnover.
4. P36 52-Week High.
5. P38 One-Week Reversal.
6. Q16 ROA.
7. Q20 Piotroski Anti-Junk.
8. R41 Low IVOL.

### Wave 2: accounting và corporate policy mạnh

9. A11 Cash Earnings Minus Accruals.
10. A12 Working-Capital Accrual.
11. A14 Inventory Growth.
12. A15 Net Operating Assets.
13. Q18 Cash ROA.
14. I21 Asset Growth.
15. I23 Capex Shock.
16. F26 Anti-Dilution.
17. F28 External Financing.
18. B35 Interest Coverage.

### Wave 3: event và diversifier

19. E06 EPS Surprise.
20. E08 CFO Surprise.
21. E09 Earnings Acceleration.
22. P39 Residual Momentum.
23. P40 Path Consistency.
24. R44 Anti-MAX.
25. R45 Liquid Low Correlation.

Các idea còn lại là challengers để thay champion yếu hoặc tạo conditional overlays; không backtest mọi permutation.

## 11. Acceptance checklist trước khi viết strategy production

- Hypothesis và primary formula được pre-register trước khi xem OOS.
- Mọi field tồn tại trong catalog và load được trên `VN-SMALL-CAP`.
- Sign convention của cash-flow fields được xác minh bằng sample observations.
- Quarterly fields được xác định là YTD hay discrete.
- Fundamental update thật sự point-in-time; delay test không làm alpha sụp bất thường.
- Coverage đủ breadth; missing không bị biến thành zero.
- Không có stale-price alpha; có liquidity floor và capacity report.
- Signal có monotonicity hoặc economic shape hợp lý, không chỉ top-bottom accidental spread.
- Net performance sống sót fee/slippage stress.
- Parameter plateau tồn tại.
- OOS alpha sống sót multiple-testing-aware hurdle.
- Correlation, downside correlation và holdings overlap đều qua gate.
- Portfolio mới tăng OOS Sharpe hoặc giảm drawdown, không chỉ giảm gross exposure.

## 12. Những gì chưa thể kết luận từ local workspace

Workspace có schema, feature/operator catalog và strategy examples nhưng không có full Round 2 equity dataset để đo coverage, IC, PnL correlation hay capacity. Vì vậy 50 idea trên là **field-compatible research hypotheses**, chưa phải alpha đã được xác nhận. Bước kế tiếp bắt buộc là probe dữ liệu trên XNOQuant, sau đó chạy Wave 1 theo cùng một backtest harness và cùng cost assumptions.


