# VN-MID-CAP: 50 Academic Alpha Ideas for a Low-Correlation Portfolio

Ngày nghiên cứu: 2026-08-02  
Phạm vi: Round 2, `VN-MID-CAP`, daily equity, point-in-time fundamentals  
Vai trò: master research universe cho mid-cap; chưa phải danh sách strategy đã được xác nhận

## 0. Kết luận điều hành

VNMIDCAP không phải “small-cap nhưng thanh khoản hơn”. Theo phương pháp HOSE, đây là 70 cổ phiếu vốn hóa cao nhất trong VNAllshare sau khi loại VN30; cùng VN30, chúng tạo thành VN100. Do đó mid-cap nằm đúng vùng chuyển tiếp giữa doanh nghiệp đang scale và doanh nghiệp đủ lớn để tiến vào VN30.

Master này xây 50 hypothesis thuộc 10 cơ chế:

1. Valuation có quality guard.
2. Profitability level, change và persistence.
3. Scaling và investment efficiency.
4. Earnings/cash-flow information diffusion.
5. Accrual và working-capital conversion.
6. Financing, payout và internally funded growth.
7. Capital structure, debt service và corporate lifecycle.
8. Price behavior và firm-specific momentum.
9. VN30 graduation, demotion và investor recognition.
10. Downside risk, lottery demand và attention.

Khác với master small-cap:

- Không đặt extreme illiquidity premium làm trọng tâm.
- Không xem value tĩnh là đủ; local guide của repo xác định mid-cap nhạy với ROE, leverage, profit growth và trend.
- Tập trung vào **profit growth so với capital growth**, **cash-funded scaling** và **liquidity/investor-recognition migration**.
- Giữ một số anchor chung như EP, accrual và 52-week high để kiểm định transferability giữa universe; đây là scientific controls, không phải sao chép thiếu chủ đích.

## 1. Cấu trúc chính thức của VNMIDCAP

HOSE Index Ground Rules 4.0 định nghĩa:

- VN30: 30 constituent có market cap và liquidity cao nhất trong VNAllshare theo tiêu chí.
- VNMidcap: 70 constituent có market cap cao nhất trong VNAllshare sau khi loại VN30.
- VN100: VN30 cộng VNMidcap.
- Chỉ số dùng free-float adjusted market capitalization, constituent review bán niên và cap 10% cho một cổ phiếu.

Nguồn: [HOSE Index Ground Rules 4.0](https://staticfile.hsx.vn/Uploads/LocalFiles/ef15ff11e799483abd11677ad0443887/20250114_20241230_QD%20747%20HOSE%20Index%20Ground%20Rules.pdf).

Factsheet ngày 30-01-2026 cho thấy:

| Thuộc tính | Giá trị |
|---|---:|
| Constituents | 70 |
| Raw market capitalization | 1,218,091 tỷ VND |
| Free-float adjusted capitalization | 647,184 tỷ VND |
| Median adjusted capitalization | 6,508 tỷ VND |
| Largest constituent weight | 6.03% |
| Top-10 weight | 40.03% |
| 1-year correlation với VN-Index | 87.40% |
| 3-year correlation với VN-Index | 89.98% |
| Financials weight | 30.72% |
| Industrials weight | 24.88% |
| Real estate weight | 16.67% |

Nguồn: [HOSE VNMIDCAP Factsheet 30-01-2026](https://staticfile.hsx.vn/Uploads/UploadDocuments/2438018/Form_Factsheet_MCIndices_VN_T02.2026.pdf).

### Hệ quả nghiên cứu

1. Universe hẹp: 70 mã nghĩa là một decile chỉ khoảng bảy cổ phiếu; tail portfolio rất dễ concentration.
2. Top-10 concentration 40.03% và correlation cao với VN-Index làm common-beta/sector risk lớn.
3. Financials + industrials chiếm hơn 55%; raw accounting ratios không thể mặc định comparable.
4. Mid-cap có capacity tốt hơn small-cap nên có thể dùng event/momentum nhanh hơn, nhưng fee vẫn phạt turnover.
5. Vì đây là phần ngay dưới VN30, relative size, liquidity và recognition migration có ý nghĩa riêng.

## 2. Local evidence và research prior

### 2.1. Prior từ chính repo

`data/vietnam_market_characteristics.md` mô tả `VN-MID-CAP` là nhóm tăng trưởng chu kỳ, nhạy với ROE và leverage; ưu tiên ROE, capital ratio, profit growth cộng medium-term trend, tránh static cheapness đơn thuần. Đây là local prior quan trọng nhưng vẫn phải falsify bằng data.

Round 2 yêu cầu daily equity, point-in-time, một strategy chỉ dùng `time_series` hoặc `cross_sectional`; fundamental chỉ được dùng sau publication date, missing không được zero-fill. Source of truth: `agent/stage_2_guideline.md` và [XNOQuant VQC 2026](https://xnoquant.io/vqc2026).

### 2.2. Bằng chứng Việt Nam

- Huang, Liu & Shu (2023) cho thấy size effect có ý nghĩa, EP là value measure tốt hơn BM/CP, và turnover là factor quan trọng trong VN-4. [Paper](https://www.pbcsf.tsinghua.edu.cn/__local/7/F5/A9/E0366D36DF73499C8CBFB66C505_4D50779F_1C1EEF.pdf)
- `Choosing Factors for the Vietnamese Stock Market` cho thấy value và operating profitability có marginal contribution lớn trong factor models Việt Nam; cash profitability cũng được kiểm định. [Paper](https://www.mdpi.com/1911-8074/14/3/96)
- Fundamental analysis/F-score phân tách winners và losers trên 622 listed firms Việt Nam giai đoạn 2009-2019. [Publication](https://research-information.bris.ac.uk/en/publications/fundamental-analysis-and-the-use-of-financial-statement-informati/)
- Idiosyncratic momentum có quan hệ dương và có ý nghĩa với future returns tại Việt Nam trong mẫu 2010-2021. [Publication](https://mx5.jst-ud.vn/jst-ud/article/view/8112)
- Low nominal price stocks trên HOSE 2009-2018 có future abnormal return cao hơn, tồn tại sau nhiều controls và kéo dài đến 12 tháng. [Publication](https://research.monash.edu/en/publications/nominal-price-anomaly-in-emerging-markets-risk-or-mispricing/)
- Momentum Việt Nam phụ thuộc mạnh sample và horizon: nghiên cứu 2017-2022 tìm thấy 4-week formation/1-week holding, trong khi các mẫu dài hơn cho kết quả mixed. [Article](https://www.ajeb.edu.vn/vi/article/hieu-ung-momentum-thi-truong-chung-khoan-viet-nam)

## 3. Evidence tier và scientific hurdle

| Tier | Ý nghĩa |
|---|---|
| A-VN | Direct Vietnam evidence hoặc rất gần signal |
| A-INT | International literature mạnh, cơ chế rõ |
| B | Có nền tảng tốt nhưng market/specification dependent |
| C | Novel mid-cap hypothesis, phải có strict untouched OOS |

| Feasibility | Ý nghĩa |
|---|---|
| Ready | Raw fields và chiều signal rõ |
| Probe | Phải xác minh sign, quarterly convention hoặc coverage |
| Experimental | Estimation/API/capacity risk cao; chưa phải production candidate |

Harvey, Liu & Zhu chỉ ra multiple-testing khiến `t > 2` không đủ cho factor mới; Hou, Xue & Zhang cho thấy phần lớn anomaly không replicate dưới weighting và test chặt. Vì master có 50 hypotheses, selection phải dùng untouched OOS, false-discovery control và parameter plateau. [Multiple testing](https://www.nber.org/papers/w20592), [Replicating Anomalies](https://academic.oup.com/rfs/article-abstract/33/5/2019/5236964)

## 4. Field map và alias

Catalog dùng chung ba universe có 496 field. Master này chỉ dùng field đã tồn tại.

### 4.1. Price, volume và benchmark

- `pv_open_panel`, `pv_high_panel`, `pv_low_panel`, `pv_close_panel`, `pv_volume_panel`
- `pv_vn30_open_panel`, `pv_vn30_high_panel`, `pv_vn30_low_panel`, `pv_vn30_close_panel`, `pv_vn30_volume_panel`
- `pv_dji_open_panel`, `pv_dji_high_panel`, `pv_dji_low_panel`, `pv_dji_close_panel`, `pv_dji_volume_panel`
- `in_universe_panel` — boolean: investable universe eligibility gate

### 4.2. Earnings

- `fun_is_eps_basis_quarterly_panel`
- `fun_is_net_profit_loss_after_tax_quarterly_panel`
- `fun_is_net_profit_loss_after_tax_annual_panel`
- `fun_is_net_accounting_profit_loss_before_tax_quarterly_panel`

### 4.3. Balance sheet

- `fun_bs_total_assets_quarterly_panel`
- `fun_bs_owners_equity_quarterly_panel`
- `fun_bs_common_shares_quarterly_panel`
- `fun_bs_liabilities_quarterly_panel`
- `fun_bs_cash_and_cash_equivalents_quarterly_panel`
- `fun_bs_current_assets_quarterly_panel`, `fun_bs_current_liabilities_quarterly_panel`
- `fun_bs_short_term_loans_quarterly_panel`, `fun_bs_long_term_loans_quarterly_panel`
- `fun_bs_accounts_receivable_quarterly_panel`
- `fun_bs_inventories_net_quarterly_panel`
- `fun_bs_short_term_prepayments_quarterly_panel`
- `fun_bs_trade_accounts_payable_quarterly_panel`
- `fun_bs_fixed_assets_quarterly_panel`
- `fun_bs_construction_in_progress_quarterly_panel`
- `fun_bs_good_will_quarterly_panel`
- `fun_bs_undistributed_earnings_quarterly_panel`
- `fun_bs_paid_in_capital_quarterly_panel`
- `fun_bs_capital_surplus_quarterly_panel`
- `fun_bs_short_term_investments_quarterly_panel`

### 4.4. Cash flow và corporate action

- `fun_cf_net_cash_inflows_outflows_from_operating_activities_quarterly_panel`
- `fun_cf_operating_profit_loss_before_changes_in_wc_quarterly_panel`
- `fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_quarterly_panel`
- `fun_cf_proceeds_from_disposal_of_fixed_assets_quarterly_panel`
- `fun_cf_proceeds_from_borrowings_quarterly_panel`
- `fun_cf_repayment_of_borrowings_quarterly_panel`
- `fun_cf_proceeds_from_issue_of_shares_quarterly_panel`
- `fun_cf_dividends_paid_quarterly_panel`
- `fun_cf_payments_for_share_returns_and_repurchases_quarterly_panel`
- `fun_cf_interest_paid_quarterly_panel`
- `fun_cf_increase_decrease_in_receivables_quarterly_panel`
- `fun_cf_increase_decrease_in_inventories_quarterly_panel`
- `fun_cf_increase_decrease_in_payables_quarterly_panel`

### 4.5. Alias dùng trong idea cards

| Alias | Field/definition |
|---|---|
| `MV` | `close * common_shares`; market-value proxy, split-aware |
| `PAT` | net profit/loss after tax |
| `PBT` | net accounting profit/loss before tax |
| `CFO` | net operating cash flow |
| `Assets` | total assets |
| `Equity` | owners equity |
| `Debt` | short-term loans + long-term loans |
| `Capex` | absolute purchases of fixed/long-term assets sau sign probe |
| `WC` | receivables + inventory + prepayments - trade payables |

## 5. Accounting-archetype guard

Factsheet cho thấy financials chiếm 30.72%, nhưng catalog không có sector field. Không được giả một ROE/working-capital ratio có cùng meaning cho ngân hàng, securities, insurer và industrial firm.

Thay vì tự gán sector, pipeline có thể tạo **accounting archetypes** chỉ để mask/diagnose:

1. Operating-asset coverage: inventory, receivables, fixed assets và CFO có dữ liệu material.
2. Finance-like balance sheet: inventory/fixed-assets operating fields sparse, liabilities/assets rất cao, working-capital formula không meaningful.
3. Project/real-asset coverage: construction-in-progress, fixed assets hoặc investment properties material.
4. Sparse reporter: thiếu phần lớn denominator/components; không zero-impute.

Archetype không phải alpha. Nó là comparability guard. Mỗi idea phải báo kết quả pooled và coverage-consistent; nếu pooled alpha chỉ đến từ một archetype, idea được coi là specialized sleeve chứ không phải universal factor.

## 6. Bản đồ 50 idea

| ID | Idea | Tier | Feasibility | Horizon | Cluster |
|---|---|---|---|---:|---|
| V01 | Positive Earnings-to-Price | A-VN | Ready | 3-12 tháng | value |
| V02 | EP-Residual Book Value | B | Ready | 6-18 tháng | value |
| V03 | Free-Cash-Flow Yield | A-INT | Probe | 6-18 tháng | value/cash |
| V04 | Enterprise-Adjusted Earnings Yield | B | Probe | 6-18 tháng | value/leverage |
| V05 | Tangible Book-to-Price | B | Ready | 6-18 tháng | asset value |
| G06 | High ROE with Capital Guard | A-VN | Ready | 1-4 quý | profitability |
| G07 | ROE Improvement | A-INT | Ready | 1-4 quý | profitability change |
| G08 | ROA Improvement | A-INT | Ready | 1-4 quý | asset profitability |
| G09 | Cash-ROA Improvement | A-INT | Probe | 1-4 quý | cash profitability |
| G10 | Persistent Profitability | A-INT | Ready | 2-8 quý | quality persistence |
| S11 | Incremental Return on New Assets | B | Probe | 2-8 quý | scaling efficiency |
| S12 | Cash-Funded Asset Growth | A-INT | Probe | 2-8 quý | funded growth |
| S13 | Fixed-Asset Productivity Improvement | B | Ready | 2-8 quý | operating efficiency |
| S14 | Lagged-Capex Payoff | B | Probe | 2-8 quý | investment payoff |
| S15 | Construction-in-Progress Conversion | C | Probe | 2-8 quý | project completion |
| E16 | Standardized EPS Surprise | A-INT | Probe | 4-12 tuần | earnings event |
| E17 | Asset-Scaled PAT Surprise | B | Probe | 4-16 tuần | earnings event |
| E18 | Operating Cash-Flow Surprise | B | Probe | 4-16 tuần | cash event |
| E19 | Earnings Acceleration | B | Probe | 1-2 quý | fundamental momentum |
| E20 | Multi-Statement Fundamental Breadth | B | Probe | 1-2 quý | confirmation breadth |
| W21 | Cash Earnings Minus Accruals | A-VN/A-INT | Probe | 1-4 quý | accrual |
| W22 | Working-Capital Accrual | A-INT | Probe | 1-4 quý | WC accrual |
| W23 | Net Operating Assets Bloat | A-INT | Probe | 2-8 quý | accumulated accrual |
| W24 | Receivables-to-Cash Divergence | B | Probe | 1-4 quý | collection quality |
| W25 | Inventory-Payables Funding Balance | B | Probe | 1-4 quý | cash-cycle proxy |
| F26 | Anti-Dilution / Share Issuance | A-INT | Probe | 2-8 quý | equity financing |
| F27 | Net Debt Issuance | B | Probe | 1-4 quý | debt financing |
| F28 | Internally Funded Investment | A-INT | Probe | 1-4 quý | funding quality |
| F29 | Net Payout Yield | A-INT | Probe | 2-8 quý | payout |
| F30 | Active Deleveraging | B | Probe | 1-4 quý | debt action |
| B31 | Capital-Ratio Strength | A-VN prior | Ready | 1-4 quý | capitalization |
| B32 | Interest-Bearing Leverage | A-INT | Ready | 1-4 quý | leverage |
| B33 | Short-Term Maturity Pressure | B | Ready | 1-4 quý | refinancing risk |
| B34 | Cash Interest Coverage | A-INT | Probe | 1-4 quý | debt service |
| B35 | Earned-vs-Contributed Capital | B | Ready | 2-8 quý | corporate lifecycle |
| P36 | Idiosyncratic Momentum | A-VN | Experimental | 1-6 tháng | stock-specific trend |
| P37 | 52-Week-High Anchoring | A-VN | Ready | 1-6 tháng | behavioral anchor |
| P38 | Four-Week Momentum | A-VN/B | Ready | 1-4 tuần | short trend |
| P39 | ROE-Confirmed Medium Trend | B | Ready | 1-6 tháng | quality trend |
| P40 | Nominal-Price Re-Rating | A-VN | Ready | 3-12 tháng | nominal-price bias |
| X41 | VN30 Graduation Frontier | B/C | Experimental | 1-6 tháng | index transition |
| X42 | Small-Cap Demotion Risk | B/C | Experimental | 1-6 tháng | index transition |
| X43 | Investor-Recognition Migration | B | Experimental | 1-6 tháng | liquidity migration |
| X44 | Crowded Index-Pressure Reversal | B | Experimental | 1-12 tuần | demand reversal |
| X45 | VN30 Beta Convergence | C | Experimental | 1-6 tháng | institutionalization |
| R46 | Downside-Beta Resilience | B | Experimental | 1-6 tháng | downside risk |
| R47 | Low Residual Volatility with Liquidity Guard | A-VN/B | Experimental | 1-3 tháng | residual risk |
| R48 | Anti-Lottery Maximum Return | A-INT | Ready | 1-3 tháng | lottery demand |
| R49 | High One-Month Abnormal Turnover | A-VN | Probe | 1-4 tuần | attention shock |
| R50 | Low 12-Month Turnover within Capacity Band | A-VN | Probe | 3-12 tháng | speculation level |

## 7. Idea cards chi tiết

### Family V: Valuation có quality guard

#### V01. Positive Earnings-to-Price

- **Cơ chế:** EP là value measure mạnh nhất trong horse race Việt Nam; mid-cap vẫn cần anchor để tránh trả mọi giá cho growth.
- **Prototype:** rank `EPS/close`; robustness bằng `PAT/MV`; chỉ positive earnings.
- **Fields:** EPS, PAT, close, common shares.
- **Mid-cap adaptation:** không dùng standalone; report double-sort với G06/G07 hoặc trend P36/P37.
- **Correlation role:** valuation anchor, thường khác growth-change và event sleeves.
- **Failure:** static cheapness không catalyst, cyclical peak earnings, split/share-count mismatch.

#### V02. EP-Residual Book Value

- **Cơ chế:** BM raw không thắng EP tại Việt Nam, nhưng phần book value không giải thích bởi EP có thể bắt asset-backed recovery.
- **Prototype:** `Equity/MV`, sau đó cross-sectional residualization hoặc orthogonal rank với V01.
- **Fields:** owners equity, close, common shares, PAT/EPS.
- **Guard:** equity dương, goodwill diagnostic, price/value liquidity floor.
- **Correlation role:** challenger của V01; chỉ nhận nếu residual PnL incremental.
- **Failure:** financial/real-estate accounting dominance; book value stale.

#### V03. Free-Cash-Flow Yield

- **Cơ chế:** mid-cap đang scale dễ có earnings nhưng không tạo distributable cash; FCF yield phân biệt growth self-financing và cash-consuming.
- **Prototype:** `(trailing CFO - abs(Capex))/MV` sau sign/YTD probe.
- **Fields:** CFO, purchases of fixed assets, close, common shares.
- **Guard:** operating-asset archetype; cap lumpy quarterly capex; annual anchor.
- **Correlation role:** bridge value-funding, dễ overlap F28/S12.
- **Failure:** phạt growth capex có NPV dương; quarterly timing.

#### V04. Enterprise-Adjusted Earnings Yield

- **Cơ chế:** ROE/growth cao nhờ leverage không đồng nghĩa rẻ; enterprise adjustment tính debt và cash vào price paid.
- **Prototype:** `PAT/(MV + Debt - cash)`; denominator dương/material.
- **Fields:** PAT, common shares, close, short/long loans, cash.
- **Guard:** compare only coverage-consistent observations; PBT variant làm robustness.
- **Correlation role:** value-leverage hybrid, không giữ cùng B32 nếu cluster mạnh.
- **Failure:** debt fields khác meaning ở financial firms; restricted cash.

#### V05. Tangible Book-to-Price

- **Cơ chế:** goodwill có thể là acquisition overpayment; tangible equity cho asset claim bảo thủ hơn raw BM.
- **Prototype:** `(Equity - goodwill)/MV`.
- **Fields:** owners equity, goodwill, close, common shares.
- **Guard:** tangible equity dương; missing goodwill không được tự coi bằng zero nếu coverage không rõ.
- **Correlation role:** asset-quality value, khác EP nhưng có thể gần V02.
- **Failure:** goodwill thực sự có value; intangible-heavy businesses bị phạt quá mức.

### Family G: Profitability level, change và persistence

#### G06. High ROE with Capital Guard

- **Cơ chế:** local mid-cap prior nhấn mạnh ROE; q-factor dùng high ROE như profitability dimension.
- **Prototype:** `PAT/average Equity`, chỉ khi `Equity/Assets` trên floor và Equity dương.
- **Fields:** PAT, owners equity, total assets.
- **Guard:** capital ratio là mask, không cộng tùy ý vào alpha; archetype diagnostics.
- **Correlation role:** core profitability champion.
- **Failure:** denominator equity nhỏ, cyclical peak, bank/non-bank comparability.

#### G07. ROE Improvement

- **Cơ chế:** change in profitability gần cash-flow news hơn static quality và phù hợp doanh nghiệp mid-cap đang chuyển phase.
- **Prototype:** YoY delta của quarterly ROE; annual delta làm slow anchor.
- **Fields:** PAT, owners equity.
- **Guard:** positive equity hai kỳ; cap denominator effects; require no major dilution diagnostic.
- **Correlation role:** profitability-change signal, có thể thấp correlation với V01/G06 level.
- **Failure:** leverage tăng làm ROE cải thiện giả; base effect.

#### G08. ROA Improvement

- **Cơ chế:** đo profit trên toàn capital base; ít bị equity leverage hơn ROE và phù hợp test q-theory.
- **Prototype:** YoY delta `PAT/average Assets`.
- **Fields:** PAT, total assets.
- **Guard:** use within accounting archetype; winsorize.
- **Correlation role:** substitute cho G07 nếu leverage contamination cao.
- **Failure:** financial balance sheets khác operating firms; asset revaluation.

#### G09. Cash-ROA Improvement

- **Cơ chế:** cash-based operating profitability có thể subsume accrual và accounting profitability.
- **Prototype:** YoY delta `trailing CFO/average Assets`.
- **Fields:** CFO, total assets.
- **Guard:** sign/YTD probe; annual anchor; winsorize working-capital release.
- **Correlation role:** cash-quality expression, dễ overlap W21/E18.
- **Failure:** collection/payment timing; financing firms.

#### G10. Persistent Profitability

- **Cơ chế:** QMJ yêu cầu quality phải persistent; ổn định profit làm current profitability đáng tin hơn một quý cao.
- **Prototype:** mean asset-scaled PAT 8 quý trừ rolling variability và fraction negative quarters.
- **Fields:** quarterly PAT, total assets.
- **Guard:** minimum history; no centered windows; report cycle bias.
- **Correlation role:** slow quality state, khác G07/G08 change.
- **Failure:** accounting smoothing; bỏ lỡ turnarounds.

### Family S: Scaling và investment efficiency

#### S11. Incremental Return on New Assets

- **Cơ chế:** cùng asset growth, firm tạo nhiều incremental profit hơn thể hiện scalable growth; tách good growth khỏi empire building.
- **Prototype:** `delta_yoy(PAT)/positive(delta_yoy(Assets))`, chỉ active khi asset growth material; fallback là profit-growth rank trừ asset-growth rank.
- **Fields:** PAT, total assets.
- **Guard:** cap near-zero asset changes; test rank-spread primary để ổn định.
- **Correlation role:** scaling efficiency, khác profitability level và conservative investment.
- **Failure:** profit payoff lag dài hơn asset investment; acquisition base effects.

#### S12. Cash-Funded Asset Growth

- **Cơ chế:** growth được tài trợ từ internal cash ít dilution/refinancing fragility hơn external-financed expansion.
- **Prototype:** asset-growth rank chỉ được thưởng khi trailing CFO đủ cover Capex và net external financing thấp.
- **Fields:** assets, CFO, Capex, borrowings, repayments, share issuance.
- **Guard:** pre-register binary funding gate; không fit nhiều weights.
- **Correlation role:** growth-funding interaction; kiểm tra incremental với F28.
- **Failure:** debt-funded project tốt; CFO timing.

#### S13. Fixed-Asset Productivity Improvement

- **Cơ chế:** mid-cap industrial scaling nên tạo thêm profit trên fixed-asset base; đây là proxy khả dụng khi catalog thiếu generic revenue.
- **Prototype:** YoY delta `PAT/average fixed_assets`.
- **Fields:** PAT, fixed assets.
- **Guard:** chỉ operating-asset coverage; fixed assets dương/material.
- **Correlation role:** operating-efficiency subfactor, khác ROA vì denominator chuyên biệt.
- **Failure:** asset-light firms; newly commissioned assets chưa ramp.

#### S14. Lagged-Capex Payoff

- **Cơ chế:** capex quá khứ chỉ là good investment nếu sau đó profit/CFO cải thiện; dùng lagged capex tránh look-ahead.
- **Prototype:** current YoY `delta PAT` hoặc `delta CFO` chia `Capex` đã công bố 4-8 quý trước.
- **Fields:** PAT, CFO, Capex, assets.
- **Guard:** lag causal; capex material; use sign-consensus PAT/CFO.
- **Correlation role:** payoff realization, khác S12 funding source và S13 level productivity.
- **Failure:** payoff horizon sai; project cycle dài; capex maintenance.

#### S15. Construction-in-Progress Conversion

- **Cơ chế:** CIP giảm đồng thời fixed assets tăng và profit/CFO cải thiện có thể báo project đi vào vận hành; buildup kéo dài báo execution risk.
- **Prototype:** positive score từ `-delta CIP`, `+delta fixed_assets`, `+delta PAT/CFO`, tất cả point-in-time.
- **Fields:** construction in progress, fixed assets, PAT, CFO.
- **Guard:** project/real-asset archetype; pre-register equal-rank composite.
- **Correlation role:** sparse project-completion event, tiềm năng low correlation.
- **Failure:** reclassification kế toán, asset sale, project chưa ramp.

### Family E: Earnings và cash-flow information diffusion

#### E16. Standardized EPS Surprise

- **Cơ chế:** PEAD do delayed reaction; mid-cap có coverage tốt hơn small-cap nhưng vẫn chưa hoàn toàn efficient.
- **Prototype:** `(EPS_q-EPS_q-4)/rolling_std(YoY EPS changes, 8 quarters)`; event memory 20-60 phiên.
- **Fields:** quarterly EPS, close, volume.
- **Guard:** publication-date alignment; delay 0/1/3/5 day; split diagnostics.
- **Correlation role:** core event candidate, khác valuation/profitability level.
- **Failure:** platform backfill; transient earnings.

#### E17. Asset-Scaled PAT Surprise

- **Cơ chế:** PAT surprise tránh per-share distortion và mở rộng coverage khi EPS không ổn định.
- **Prototype:** `(PAT_q-PAT_q-4)/lag Assets`.
- **Fields:** PAT, total assets, EPS.
- **Guard:** seasonal matching, winsorize, sign agreement diagnostic với EPS.
- **Correlation role:** substitute/challenger E16.
- **Failure:** one-off gains; financial-firm scale.

#### E18. Operating Cash-Flow Surprise

- **Cơ chế:** cash news có thể xác nhận hoặc phủ định earnings news; ít chịu accounting estimate hơn PAT.
- **Prototype:** `(CFO_q-CFO_q-4)/lag Assets`, held 20-80 phiên.
- **Fields:** CFO, assets, PAT.
- **Guard:** quarterly YTD-vs-discrete probe; working-capital component diagnostics.
- **Correlation role:** cash event, tiềm năng khác price-only momentum.
- **Failure:** tax/payment seasonality và collection timing.

#### E19. Earnings Acceleration

- **Cơ chế:** second difference bắt tốc độ thay đổi của fundamental growth, phù hợp mid-cap ở phase tăng tốc/chậm lại.
- **Prototype:** current asset-scaled YoY PAT change trừ quarter trước asset-scaled YoY change.
- **Fields:** PAT, EPS, assets.
- **Guard:** scaled differences, không percentage growth quanh zero.
- **Correlation role:** acceleration, khác surprise level E16/E17.
- **Failure:** noisy base effect; low persistence.

#### E20. Multi-Statement Fundamental Breadth

- **Cơ chế:** improvement đồng thời EPS, PAT và CFO ít có khả năng là một accounting artifact; breadth là confirmation, không phải weighted optimizer.
- **Prototype:** count/rank score của positive EPS innovation, PAT/assets innovation và CFO/assets innovation.
- **Fields:** EPS, PAT, CFO, assets.
- **Guard:** require ít nhất hai available components; missing không fail; equal component weights.
- **Correlation role:** composite event quality, có thể giảm tail risk nhưng overlap E16-E18.
- **Failure:** double counting; breadth nhỏ nếu data coverage kém.

### Family W: Accrual và working-capital conversion

#### W21. Cash Earnings Minus Accruals

- **Cơ chế:** cash earnings bền hơn accrual earnings; đặc biệt hữu ích để lọc mid-cap growth chất lượng thấp.
- **Prototype:** `(CFO-PAT)/lag Assets`; rank cao là cash realization tốt.
- **Fields:** CFO, PAT, assets.
- **Guard:** sign/YTD probe; annual anchor; operating-archetype report.
- **Correlation role:** core accounting-quality primitive.
- **Failure:** temporary working-capital release.

#### W22. Working-Capital Accrual

- **Cơ chế:** reliability của WC accrual thấp hơn cash; tách operating estimate khỏi long-term investment.
- **Prototype:** `-(delta receivables + delta inventory + delta prepayments - delta payables)/lag Assets`.
- **Fields:** receivables, inventory, prepayments, trade payables, assets; CF WC changes để cross-check.
- **Guard:** complete component coverage; no zero-imputation.
- **Correlation role:** granular challenger của W21.
- **Failure:** healthy growth làm WC tăng; seasonal cycle.

#### W23. Net Operating Assets Bloat

- **Cơ chế:** stock tích lũy của operating accrual/growth có thể dự báo future profitability thấp hơn.
- **Prototype:** âm `[(Assets-cash-short_investments)-(liabilities-Debt)]/Assets`.
- **Fields:** assets, cash, short investments, liabilities, debt.
- **Guard:** compare within coverage archetype; level là primary, change là robustness.
- **Correlation role:** accumulated stock, khác W21/W22 flow.
- **Failure:** classification không đồng nhất; finance-like firms.

#### W24. Receivables-to-Cash Divergence

- **Cơ chế:** PAT tăng nhưng receivables phình và CFO không theo kịp báo collection/revenue-recognition risk.
- **Prototype:** âm của receivables growth rank trừ CFO-growth rank; primary test component-neutral rank spread.
- **Fields:** accounts receivable, CFO, assets, PAT.
- **Guard:** operating-asset coverage; cap base effects.
- **Correlation role:** collection-specific signal, khác total accrual.
- **Failure:** mở rộng credit sales hợp lý; payment timing.

#### W25. Inventory-Payables Funding Balance

- **Cơ chế:** inventory growth được supplier financing bù đắp ít hút cash hơn inventory buildup phải tài trợ bằng debt.
- **Prototype:** âm `delta(inventory - trade_payables)/lag Assets`; CFO confirmation làm diagnostic.
- **Fields:** inventory net, trade accounts payable, assets, CFO, borrowings.
- **Guard:** inventory-using firms only; seasonal YoY differences.
- **Correlation role:** cash-cycle proxy không cần generic revenue.
- **Failure:** stretching suppliers do distress; commodity stocking.

### Family F: Financing, payout và internally funded growth

#### F26. Anti-Dilution / Share Issuance

- **Cơ chế:** equity issuance có thể phản ánh market timing và giảm per-share participation.
- **Prototype:** âm YoY common-share growth, confirm bằng share-issuance proceeds/assets.
- **Fields:** common shares, proceeds from issue of shares, paid-in capital, assets.
- **Guard:** split detection; distinguish cash issuance from missing.
- **Correlation role:** equity-financing primitive.
- **Failure:** rights issue tài trợ high-return growth.

#### F27. Net Debt Issuance

- **Cơ chế:** borrowing ròng cao báo financing demand/refinancing risk, nhưng literature cho thấy relation có thể bị liquidity confound.
- **Prototype:** `-(borrowings-repayments)/lag Assets`.
- **Fields:** borrowings, repayments, assets.
- **Guard:** horse-race với liquidity/recognition X43/R50; annual anchor.
- **Correlation role:** debt action, khác leverage level B32.
- **Failure:** refinancing rollover, productive debt, sign convention.

#### F28. Internally Funded Investment

- **Cơ chế:** doanh nghiệp cover Capex bằng CFO có growth path bền hơn doanh nghiệp phải vay/issue liên tục.
- **Prototype:** `(CFO-abs(Capex))/Assets - net_external_financing/Assets` hoặc two-stage rank gate.
- **Fields:** CFO, Capex, borrowings, repayments, share issuance, assets.
- **Guard:** two-stage rank preferred để giảm ratio instability; sign probe.
- **Correlation role:** funding-quality champion, gần S12 nhưng F28 nhấn financing gap thay growth outcome.
- **Failure:** early-stage project cần external capital hợp lý.

#### F29. Net Payout Yield

- **Cơ chế:** dividends + repurchases - issuance đo shareholder distribution tốt hơn dividend yield đơn lẻ.
- **Prototype:** `(abs(dividends)+abs(repurchases)-share_issuance)/MV`.
- **Fields:** dividends paid, share returns/repurchases, share issuance, close, common shares.
- **Guard:** trailing annual, sign probe, repurchase coverage report.
- **Correlation role:** payout/capital-return sleeve, có thể đối nghịch S12/F28.
- **Failure:** payout do thiếu growth; repurchases sparse.

#### F30. Active Deleveraging

- **Cơ chế:** repayment vượt new borrowings và debt stock giảm thể hiện management action, khác leverage tĩnh.
- **Prototype:** `(repayments-borrowings)/lag Debt`, require prior Debt material và confirm debt decline.
- **Fields:** repayments, borrowings, short/long loans.
- **Guard:** không thưởng zero-debt firm như active repayment; sign probe.
- **Correlation role:** change/action sleeve, khác B32/B34.
- **Failure:** repayment làm cạn cash; classification changes.

### Family B: Capital structure, debt service và lifecycle

#### B31. Capital-Ratio Strength

- **Cơ chế:** repo local guide ưu tiên Equity/Assets cho mid-cap; vốn chủ dày giảm fragility của cyclical growth.
- **Prototype:** `Equity/Assets`, hoặc improvement làm challenger.
- **Fields:** owners equity, total assets.
- **Guard:** equity/assets meaningful theo archetype; cap range.
- **Correlation role:** capitalization state, có thể làm guard cho G06.
- **Failure:** financial firms có structurally high leverage; excess equity có thể giảm ROE.

#### B32. Interest-Bearing Leverage

- **Cơ chế:** debt dùng để scale tạo convexity nhưng high leverage làm downside lớn; quality portfolio thường ưu tiên low leverage.
- **Prototype:** âm `Debt/Assets`; Debt/Equity làm robustness với positive equity.
- **Fields:** short/long loans, assets, equity.
- **Guard:** level và change pre-registered riêng; archetype diagnostics.
- **Correlation role:** leverage level, khác capital ratio vì liabilities gồm nhiều non-debt claims.
- **Failure:** productive leverage; financial-company debt definition.

#### B33. Short-Term Maturity Pressure

- **Cơ chế:** short debt concentration tạo refinancing wall ngay cả khi total leverage vừa phải.
- **Prototype:** âm `short_term_loans/(short_term_loans+long_term_loans)` nhân material debt/assets gate.
- **Fields:** short/long loans, assets, cash.
- **Guard:** no-debt observations excluded; cash coverage diagnostic.
- **Correlation role:** maturity structure, khác leverage total.
- **Failure:** revolving lines bình thường; maturity classification.

#### B34. Cash Interest Coverage

- **Cơ chế:** CFO/interest paid đo khả năng service debt bằng cash, phù hợp mid-cap cyclical hơn accounting ROE đơn lẻ.
- **Prototype:** `trailing CFO/abs(interest_paid)`; zero interest không được coi là infinite.
- **Fields:** CFO, interest paid, debt.
- **Guard:** interest/debt material; cap ratio; sign/YTD probe.
- **Correlation role:** debt-service quality, có thể complement profitability change.
- **Failure:** payment timing, capitalized interest.

#### B35. Earned-vs-Contributed Capital

- **Cơ chế:** corporate lifecycle theory xem retained earnings share cao là dấu hiệu firm đã tích lũy internal capital, ít phụ thuộc contributed equity.
- **Prototype:** `undistributed_earnings/(paid_in_capital+capital_surplus)` hoặc `/Equity`, denominators dương.
- **Fields:** undistributed earnings, paid-in capital, capital surplus, owners equity.
- **Guard:** test two definitions nhưng chọn một primary; negative retained earnings handled explicitly.
- **Correlation role:** slow lifecycle state, kỳ vọng khác event/momentum.
- **Failure:** mature stagnation; accounting/legal reserve differences.

### Family P: Price behavior và firm-specific momentum

#### P36. Idiosyncratic Momentum

- **Cơ chế:** direct Vietnam study cho thấy residual momentum tồn tại cạnh conventional momentum và phù hợp underreaction.
- **Prototype:** cumulative residual return sau khi loại VN30 beta trên 6-1 hoặc 12-2 tháng.
- **Fields:** stock close, VN30 close.
- **Guard:** shrink beta, sufficient observations, nonsynchronous-trading check.
- **Correlation role:** mid-cap behavioral champion, giảm market-direction contamination.
- **Failure:** beta estimation noise; momentum crash.

#### P37. 52-Week-High Anchoring

- **Cơ chế:** price gần 52-week high đo anchoring/underreaction khác cumulative momentum; có evidence Việt Nam.
- **Prototype:** `close/rolling_max(close,250)`.
- **Fields:** close, high, volume.
- **Guard:** price-limit/volume-exhaustion diagnostic; liquidity floor.
- **Correlation role:** anchor trend, challenger/complement P36.
- **Failure:** regime reversal.

#### P38. Four-Week Momentum

- **Cơ chế:** recent Vietnam study cho thấy formation bốn tuần, holding một tuần mạnh, nhưng long-sample evidence mixed.
- **Prototype:** cumulative 20-day return, hold/rebalance weekly; primary definition fixed trước OOS.
- **Fields:** close, volume.
- **Guard:** high turnover cost stress; skip most recent day variant chỉ là robustness.
- **Correlation role:** short trend, khác medium P36/P37.
- **Failure:** sample dependence; crash và fee erosion.

#### P39. ROE-Confirmed Medium Trend

- **Cơ chế:** local guide đề xuất quality + medium trend; trend có fundamental support ít giống speculative momentum hơn.
- **Prototype:** residual/52-week trend rank chỉ active khi G06/G07 above median; equal two-stage gate.
- **Fields:** close, VN30 close, PAT, equity, assets.
- **Guard:** test component alphas và interaction increment; không optimize weights.
- **Correlation role:** quality-trend composite; có thể là production-friendly champion nhưng overlap G/P.
- **Failure:** confirmation đến muộn; double counting.

#### P40. Nominal-Price Re-Rating

- **Cơ chế:** direct HOSE evidence cho thấy low nominal-price stocks có abnormal return cao hơn sau nhiều controls, được giải thích là mispricing.
- **Prototype:** âm cross-sectional rank của close, residualized/controlled với MV, liquidity, EP và MAX.
- **Fields:** close, common shares, volume.
- **Guard:** split detection; nominal price không được coi là value; liquidity and MAX controls bắt buộc.
- **Correlation role:** Vietnam-specific behavioral sleeve.
- **Failure:** corporate-action artifacts; penny-stock risk; relation có thể yếu trong mid-cap subset.

### Family X: VN30 transition và investor recognition

#### X41. VN30 Graduation Frontier

- **Cơ chế:** VNMIDCAP là 70 mã ngay dưới VN30; top relative MV kèm liquidity mạnh có xác suất tiến gần investor-recognition/index-demand frontier.
- **Prototype:** high cross-sectional `MV` rank + improving trading-value/turnover + positive residual trend.
- **Fields:** close, common shares, volume, VN30 close.
- **Guard:** đây là proxy, không phải reconstructed HOSE eligibility; report performance quanh review và ngoài review riêng nếu timestamp API cho phép.
- **Correlation role:** mid-cap-specific transition sleeve.
- **Failure:** không có exact free float/eligibility; anticipation đã priced; promotion làm future expected return giảm sau recognition.

#### X42. Small-Cap Demotion Risk

- **Cơ chế:** bottom relative MV, deteriorating liquidity và negative residual trend có nguy cơ rời top-70; expected flow/recognition giảm.
- **Prototype:** tránh/short combination low MV rank, declining rolling trading value và negative residual momentum.
- **Fields:** close, common shares, volume, VN30 close.
- **Guard:** market cap proxy split-aware; no exact constituent history; one-sided avoidance test trước long-short.
- **Correlation role:** transition downside, không đơn giản là mirror X41 vì deletion effects bất đối xứng.
- **Failure:** deep recovery sau demotion pressure; free-float mismatch.

#### X43. Investor-Recognition Migration

- **Cơ chế:** Merton recognition và index literature dự báo khi investor base mở rộng, liquidity/coverage tăng và price re-rate; mid-cap là natural migration zone.
- **Prototype:** rising trading value and turnover, falling Amihud, rising residual price informativeness; không yêu cầu high raw return.
- **Fields/features:** close, volume, common shares, `amihud_illiquidity_panel`, VN30 close.
- **Guard:** pre-register equal rank of three primitives; stale/liquidity floor.
- **Correlation role:** liquidity-state change, khác turnover level R50.
- **Failure:** attention burst/pump; recognition tăng có thể làm future required return thấp hơn.

#### X44. Crowded Index-Pressure Reversal

- **Cơ chế:** index demand curves dốc xuống ngắn hạn nhưng nhiều price pressure đảo chiều; Greenwood thấy phần lớn event move reverse sau đó.
- **Prototype:** contrarian residual return sau joint extreme abnormal turnover, high relative MV và large VN30-relative move.
- **Fields:** close, volume, common shares, VN30 close.
- **Guard:** hold 1-12 tuần; exclude fundamental update shock; no calendar mining.
- **Correlation role:** potential negative correlation với X41/P36 trend.
- **Failure:** permanent information/recognition effect; missing exact index event.

#### X45. VN30 Beta Convergence

- **Cơ chế:** institutionalization/index proximity có thể làm correlation/beta với VN30 tăng trong khi own illiquidity giảm.
- **Prototype:** positive change in rolling correlation/beta với VN30 + falling Amihud; test continuation và later compression separately.
- **Fields:** stock/VN30 close, volume.
- **Guard:** liquidity guard, shrink beta; primary direction phải pre-register sau exploratory sample rồi khóa OOS.
- **Correlation role:** systematic-recognition state; may diversify accounting factors.
- **Failure:** chỉ phản ánh market-wide rally; higher commonality reduces portfolio diversification.

### Family R: Downside risk, lottery demand và attention

#### R46. Downside-Beta Resilience

- **Cơ chế:** mid-cap cyclical nhạy market selloff; downside beta khác normal beta và hữu ích cho portfolio drawdown.
- **Prototype:** âm beta chỉ trên ngày VN30 âm/bottom quantile, residualized với normal beta.
- **Fields:** stock/VN30 close.
- **Guard:** long window, minimum downside observations; evaluate as risk sleeve first.
- **Correlation role:** tail-risk diversifier.
- **Failure:** high downside beta có thể earn risk premium; low beta không đảm bảo alpha.

#### R47. Low Residual Volatility with Liquidity Guard

- **Cơ chế:** high IVOL stocks có thể bị lottery preference overprice; evidence Việt Nam tồn tại nhưng VN-4 có thể subsume.
- **Prototype:** âm residual-return std sau VN30 beta.
- **Fields:** stock/VN30 close, volume.
- **Guard:** exclude stale low-vol via trading value/turnover; 60-120 day window.
- **Correlation role:** residual risk, dễ overlap R48/R50.
- **Failure:** replication mixed; low-vol crash.

#### R48. Anti-Lottery Maximum Return

- **Cơ chế:** maximum daily return tháng trước đo lottery demand; high MAX dự báo future return thấp trong paper gốc.
- **Prototype:** âm rolling max daily return 20 phiên; top-3 mean robustness.
- **Fields:** close, high, volume.
- **Guard:** price-limit saturation, stale and corporate-action filters.
- **Correlation role:** tail-shape, khác std nhưng expected cluster với R47.
- **Failure:** large-scale replication không ổn định; IVOL proxy.

#### R49. High One-Month Abnormal Turnover

- **Cơ chế:** Vietnam evidence cho thấy 20-day/250-day turnover ratio cao có positive short-horizon alpha sau VN-4; đây là continuation shock.
- **Prototype:** `mean(turnover,20)/mean(turnover,250)`, long high, hold 1-4 tuần.
- **Fields:** volume, common shares.
- **Guard:** cap extreme issuance/pump events; không đảo dấu nhầm thành reversal.
- **Correlation role:** fast attention event, khác R50 slow level.
- **Failure:** exhaustion; high turnover cost.

#### R50. Low 12-Month Turnover within Capacity Band

- **Cơ chế:** tại Việt Nam high long-horizon turnover gắn speculation/overpricing; mid-cap adaptation tránh đáy illiquid và chỉ chọn low relative turnover trong investable band.
- **Prototype:** âm mean daily `volume/common_shares` 250 ngày, mask middle/high trading-value capacity.
- **Fields:** volume, common shares, close.
- **Guard:** capacity band và max weight; report net fees.
- **Correlation role:** VN-4 exposure control/champion attention level.
- **Failure:** low turnover do neglected deterioration; overlap residual vol.

## 8. Nguồn học thuật theo cơ chế

### Profitability, quality và investment

- Hou, Xue & Zhang: q-factor gồm market, size, investment và ROE; investment/profitability giải thích nhiều anomaly. [Paper](https://global-q.org/uploads/1/2/2/6/122679606/houxuezhang2015rfs.pdf)
- Fama & French: five-factor model bổ sung profitability và investment. [Paper](https://www.aea.ru/data/pdf/fama2015.pdf)
- Asness, Frazzini & Pedersen: quality gồm profitability, growth, safety và payout. [Paper](https://www.aqr.com/-/media/AQR/Documents/Insights/Working-Papers/Quality-Minus-Junk.pdf)
- Ball et al.: cash-based operating profitability có thể subsume accrual và operating profitability có accrual. [Publication](https://www.sciencedirect.com/science/article/pii/S0304405X16300307)
- Lim et al.: profitability growth dự báo returns; magnitude phụ thuộc firm scale. [Publication](https://www.sciencedirect.com/science/article/pii/S0378426623002273)
- Soliman: DuPont components, đặc biệt change in asset turnover, có information về future earnings/returns. Catalog thiếu generic sales nên master chỉ dùng productivity proxies, không gọi nhầm là true asset turnover. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1101981)
- Cooper, Gulen & Schill: total asset growth cao dự báo future abnormal return thấp. [Paper](https://onlinelibrary.wiley.com/doi/pdf/10.1111/j.1540-6261.2008.01370.x)
- Titman, Wei & Xie: abnormal capital investment liên hệ với future underperformance. [Publication](https://ideas.repec.org/a/cup/jfinqa/v39y2004i04p677-700_00.html)
- Mao & Wei: cash-flow news giải thích investment effect và expectation reversal. [Paper](https://pubsonline.informs.org/doi/pdf/10.1287/mnsc.2015.2235)

### Accrual, working capital và financing

- Sloan: cash earnings bền hơn accrual earnings. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2598)
- Richardson et al.: less reliable accruals có persistence thấp hơn và mispricing lớn hơn. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=521062)
- Fairfield, Whisenant & Yohn: accrual và growth in long-term NOA đều dự báo future profitability thấp hơn. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=322520)
- Hirshleifer et al.: high net operating assets dự báo return thấp. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=404120)
- Cash-conversion-cycle effect có international/emerging-market evidence, nhưng catalog thiếu sales nên W25 chỉ là balance-sheet proxy. [Publication](https://www.sciencedirect.com/science/article/pii/S037842662200111X)
- Pontiff & Woodgate: net share issuance dự báo returns. [Publication](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2008.01335.x)
- Bradshaw, Richardson & Sloan: net external financing liên hệ âm với future returns/profitability, nhưng accrual controls quan trọng. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=904226)
- Boudoukh et al.: net payout yield rộng hơn dividend yield. [Publication](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2007.01226.x)
- DeAngelo, DeAngelo & Stulz: retained-earnings share phản ánh corporate lifecycle/payout state. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=766086)

### Information diffusion và behavior

- Hong, Lim & Stein: momentum mạnh hơn ở firms nhỏ/low coverage do gradual information diffusion. [NBER](https://www.nber.org/system/files/working_papers/w6553/w6553.pdf)
- Novy-Marx: recent fundamental performance chứa information khác price momentum. [NBER](https://www.nber.org/papers/w20984.pdf)
- George & Hwang: 52-week high có information khác raw momentum. [Paper](https://onlinelibrary.wiley.com/doi/pdf/10.1111/j.1540-6261.2004.00695.x)
- Da, Gurun & Warachka: continuous small price moves tạo momentum persistence mạnh hơn discrete jumps. [Paper](https://business.uq.edu.au/sites/default/files/events/files/mitch-warachka-paper.pdf)
- Lee & Swaminathan: trading volume giúp phân biệt momentum lifecycle và reversal. [DOI](https://doi.org/10.1111/0022-1082.00280)

### Recognition, index demand và liquidity

- Merton: incomplete investor recognition ảnh hưởng required return và investor base. [Paper](https://dspace.mit.edu/bitstream/handle/1721.1/2166/SWP-1869-18148074.pdf)
- Shleifer: index addition returns phù hợp downward-sloping stock demand curves. [Publication](https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1986.tb04518.x)
- Greenwood: index redefinition tạo price pressure lớn và hơn 70% event return trong case study đảo chiều trong 20 tuần. [Paper](https://www.hbs.edu/ris/download.aspx?name=Short-+and+Long-term+Demand+Curves+for+Stocks.pdf)
- Hegde & McDermott: index additions có sustained liquidity improvement. [Publication](https://www.sciencedirect.com/science/article/pii/S1386418102000460)
- Emerging-market evidence hỗ trợ investor-recognition hypothesis quanh benchmark inclusion/exclusion. [Publication](https://www.sciencedirect.com/science/article/pii/S1566014114000417)
- Hoang & Phan: liquidity được định giá trong Vietnam factor model. [Publication](https://research.monash.edu/en/publications/is-liquidity-priced-in-the-vietnamese-stock-market/)
- Bekaert, Harvey & Lundblad: local liquidity là driver quan trọng của expected returns ở emerging markets. [Publication](https://doi.org/10.1093/rfs/hhm030)

### Risk và robustness

- Ang, Chen & Xing: downside covariance là dimension khác regular beta. [NBER](https://www.nber.org/papers/w11824)
- Ang et al.: high idiosyncratic volatility và low future returns trong paper gốc/international evidence. [Paper](https://www.ruf.rice.edu/~yxing/AHXZ_011906.pdf)
- Bali, Cakici & Whitelaw: maximum daily return proxy lottery preference. [NBER](https://www.nber.org/papers/w14804.pdf)
- Geertsema & Lu: anomaly strategies có thể nén thành số cluster nhỏ hơn nhiều. [Paper](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID3666663_code1315714.pdf?abstractid=3002797&mirid=1)
- DeMiguel, Garlappi & Uppal: optimizer phức tạp thường khó thắng `1/N` ngoài mẫu do estimation error. [Paper](https://www.heisetraining.at/wpblog/wp-content/uploads/2017/10/DeMiguel-et-al.-2009-Optimal-Versus-Naive-Diversification-How-Ineffici.pdf)

## 9. Transferability so với VN-SMALL-CAP

| Loại | Mid-cap IDs | Cách dùng |
|---|---|---|
| Scientific controls chuyển từ small-cap | V01, E16, W21, P37, R47-R50 | So sánh sign, IC, capacity và correlation giữa universe |
| Mid-cap core mới | G06-G10, S11-S15, B31-B35, P36/P39 | Đo quality, scaling, leverage và idiosyncratic trend |
| Mid-cap transition experimental | X41-X45 | Chỉ nhận sau strict OOS và proxy validation |
| Small-cap mechanism bị hạ ưu tiên | extreme Amihud tail, pure low-liquidity premium | Mid-cap có liquidity tốt hơn; tránh kiếm alpha từ non-executable tail |

Không dùng kết quả small-cap để chọn parameter cho mid-cap. Transfer test phải dùng cùng primary definition, sau đó đánh giá heterogeneity; nếu đổi formula để cứu kết quả thì đó là hypothesis mới và phải chịu multiple-testing penalty.

## 10. Substitute và complement map

### Substitutes trước khi data chứng minh ngược lại

| Empirical cluster prior | Champion ban đầu | Challengers |
|---|---|---|
| Value | V01 | V02-V05 |
| Profitability | G06 | G07-G10 |
| Scaling/investment | S11 | S12-S15 |
| Earnings event | E16 | E17-E20 |
| Accrual/WC | W21 | W22-W25 |
| Financing | F28 | F26-F30 |
| Capital/debt | B31 hoặc B34 | B32-B35 |
| Trend | P36 | P37-P39 |
| Index recognition | X43 | X41-X45 |
| Risk/attention | R46 hoặc R49 | R47-R50 |

### Complement priors đáng test

- V01 EP với G07 ROE improvement: cheapness level + profitability change.
- E16 EPS surprise với S14 lagged-capex payoff: report event + long investment cohort.
- W21 cash earnings với P36 idiosyncratic momentum: accounting quality + stock-specific diffusion.
- F28 internally funded investment với X43 recognition migration: fundamental scale + investor-base transition.
- B34 interest coverage với R49 abnormal-turnover continuation: slow debt quality + fast attention shock.
- P36 idiosyncratic momentum với X44 pressure reversal: medium continuation + short correction barbell.

## 11. Pipeline phù hợp universe 70 mã

### 11.1. Signal construction

1. Verify quarterly field là discrete hay YTD; annual dùng làm anchor.
2. Fundamental chỉ sau publication date; delay test 0/1/3/5 ngày.
3. Safe divide; positive/material denominator; missing giữ missing.
4. Report pooled và accounting-archetype coverage.
5. Winsorize cross-section 2%-98%, sau đó rank.
6. Với 70 names, dùng continuous rank weights và `max_abs_weight`; tránh decile portfolio concentration.
7. Liquidity/capacity mask là portfolio control độc lập, không nhét vào mọi alpha score.

### 11.2. Orthogonalization order

Để tìm alpha thật thay vì known-factor repackaging, mỗi candidate phải được test theo thứ tự:

1. Raw signal.
2. Sau V01 EP control.
3. Sau G06/G07 profitability control.
4. Sau P36/P37 trend control.
5. Sau R50 turnover và beta control.

Một signal chỉ được gọi là novel nếu residual PnL/IC còn material. Riêng X41-X45 phải kiểm soát relative MV, trend và turnover vì cả ba có thể tạo false index-transition story.

### 11.3. Evaluation

- Coverage, dispersion và eligible names theo ngày.
- Rank IC, IC t-stat, quintile monotonicity; quintile ưu tiên hơn decile vì breadth.
- Gross và fee-adjusted Sharpe/CAGR/MaxDD/Profit Factor/Calmar.
- Turnover, average holding period, position concentration.
- Bull/bear, high/low VN30 volatility, high/low market liquidity.
- Pearson/Spearman PnL correlation, 63/126-day rolling correlation.
- Downside correlation, co-loss bottom-decile probability.
- Signed holdings overlap và common top/bottom names.
- Untouched OOS, parameter plateau và false-discovery-aware hurdle.

Local readiness target tham khảo trong repo cho `VN-MID-CAP`: Sharpe >= 1.0, CAGR >= 18%, MaxDD >= -40%, Profit Factor >= 1.1, Calmar >= 0.8. Đây là minimum workflow threshold, không thay thế scientific robustness.

## 12. Seed portfolios

### Seed A: eight economic mechanisms

| Slot | Candidate | Vai trò |
|---|---|---|
| 1 | V01 | Vietnam EP anchor |
| 2 | G07 | profitability change |
| 3 | S11 | scaling efficiency |
| 4 | E16 | earnings event |
| 5 | W21 | accrual quality |
| 6 | F28 | internally funded investment |
| 7 | P36 | idiosyncratic momentum |
| 8 | R46 | downside resilience |

### Seed B: mid-cap-specific research portfolio

1. G06 High ROE with Capital Guard.
2. S12 Cash-Funded Asset Growth.
3. S14 Lagged-Capex Payoff.
4. B34 Cash Interest Coverage.
5. P36 Idiosyncratic Momentum.
6. X43 Investor-Recognition Migration.

Seed B có thesis phù hợp mid-cap hơn nhưng X43 là experimental; portfolio production phải có version không chứa X-family làm benchmark.

### Weighting

- Bắt đầu equal risk theo empirical cluster hoặc `1/N` với volatility caps.
- Không optimize sample mean return.
- Covariance optimization chỉ sau shrinkage, weight caps và turnover penalty.
- Một family không được chiếm hơn 25% portfolio risk trước khi OOS evidence đủ mạnh.

## 13. Research waves

### Wave 1: direct/local và highest feasibility

1. G06 High ROE with Capital Guard.
2. G07 ROE Improvement.
3. V01 Positive EP.
4. P36 Idiosyncratic Momentum.
5. P37 52-Week High.
6. R49 One-Month Abnormal Turnover.
7. R50 Low 12-Month Turnover Capacity Band.
8. B31 Capital Ratio.

### Wave 2: scaling và cash quality

9. S11 Incremental Return on New Assets.
10. S12 Cash-Funded Asset Growth.
11. S13 Fixed-Asset Productivity.
12. S14 Lagged-Capex Payoff.
13. W21 Cash Earnings Minus Accruals.
14. W24 Receivables-to-Cash Divergence.
15. F28 Internally Funded Investment.
16. B34 Cash Interest Coverage.

### Wave 3: event và transition

17. E16 EPS Surprise.
18. E18 CFO Surprise.
19. E20 Fundamental Breadth.
20. P38 Four-Week Momentum.
21. P40 Nominal-Price Re-Rating.
22. X41 Graduation Frontier.
23. X43 Recognition Migration.
24. X44 Pressure Reversal.

Các idea còn lại là challengers. Không backtest mọi combination của 50 idea.

## 14. Acceptance checklist

- Primary economic hypothesis và formula được pre-register.
- Mọi field load được trên `VN-MID-CAP` đúng mode.
- Cash-flow sign và quarterly convention đã probe.
- Publication alignment/delay robustness không cho thấy leakage.
- Missing không zero-impute; positive/material denominator.
- Pooled result không chỉ là artifact của finance-heavy accounting archetype.
- Eligible breadth đủ; max single-name weight không quá cao.
- Net-of-fee result sống sót turnover stress.
- Signal giữ sign và shape qua regimes/subperiods.
- Parameter plateau tồn tại, không chỉ một best window.
- Novel signal sống sau EP, profitability, trend, turnover và beta controls.
- PnL/downside/tail correlation qua portfolio gate.
- OOS tăng Sharpe hoặc giảm drawdown so với `1/N` incumbents.
- X-family có proxy validation và benchmark không-index-transition.

## 15. Những gì local workspace chưa cho phép kết luận

Workspace không chứa full Round 2 equity dataset, exact free-float, historical VN30/VNMidcap constituent files, sector labels, institutional ownership hay analyst coverage. Vì vậy:

- Không thể khẳng định coverage của từng accounting field.
- Không thể tính IC/PnL correlation/capacity ngay trong repo.
- X41-X45 chỉ là proxy-based hypotheses, không phải exact index-reconstitution strategies.
- Accounting archetypes phải được xác minh trên observations thực, không được diễn giải như sector ground truth.

Bước tiếp theo là chạy một data probe thống nhất trên XNOQuant, sau đó backtest Wave 1 bằng cùng cost model và cùng OOS split trước khi sinh portfolio.
