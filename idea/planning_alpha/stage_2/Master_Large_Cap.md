# VN-LARGE-CAP: 50 Academic Alpha Ideas for an Ultra-Low-Correlation Portfolio

Ngày nghiên cứu: 2026-08-02  
Phạm vi: Round 2, `VN-LARGE-CAP`, daily equity, point-in-time fundamentals  
Vai trò: master hypothesis universe; chưa phải danh sách strategy đã được xác nhận bằng backtest

## 0. Kết luận điều hành

Large-cap là bài toán khó nhất nếu mục tiêu không chỉ là Sharpe mà còn là correlation rất thấp. Factsheet HOSE ngày 30-01-2026 cho thấy VN30 có tương quan 97.25% với VN-Index trong một năm và 97.24% trong ba năm. Một strategy long-only theo trend hoặc một composite value-momentum đơn giản vì thế rất dễ trở thành market beta được đổi tên.

Master này không giả định `VN-LARGE-CAP` của XNOQuant trùng hoàn toàn VN30. VN30 chỉ là proxy chính thức gần nhất để hiểu cấu trúc một large-cap universe Việt Nam; exact membership phải được probe trên platform. Thiết kế 50 hypothesis theo 10 cơ chế:

1. Cash profitability và cash-flow durability.
2. Valuation residual, tránh static value thuần.
3. Payout và financing policy.
4. Balance-sheet resilience.
5. Capital-allocation efficiency.
6. Slow fundamental events.
7. VN30-residual price behavior.
8. Downside defense và tail asymmetry.
9. Index/flow pressure từ daily OHLCV.
10. Orthogonal interactions được pre-register.

Để giảm overlap với hai master trước:

- Không lấy extreme illiquidity, nominal price, lottery demand hoặc speculative turnover làm core như small-cap.
- Không lấy raw ROE growth, scaling, four-week momentum hoặc VN30-graduation proxy làm core như mid-cap.
- Chỉ giữ raw EP, SUE, asset growth và MAX như scientific control legs; production hypotheses dùng persistence, change hoặc residual construction và phải thắng sau residualization.
- Ưu tiên `cross_sectional` market-neutral, continuous ranks và benchmark-residual signals. `time_series` long-only chỉ là challenger vì contract `[0,1]` không thể triệt market beta trực tiếp.

**Quan trọng:** “ultra-low correlation” là thuộc tính phải đo từ daily net PnL của portfolio, không phải thuộc tính có thể suy ra từ tên idea hay từ việc dùng universe khác. Mục tiêu `|corr| <= 0.20` dưới đây là research gate, không phải kết quả đã được chứng minh.

## 1. Official large-cap proxy và hệ quả định lượng

HOSE Index Ground Rules 4.0 định nghĩa VN30 là 30 cổ phiếu đứng đầu VNAllshare theo market capitalization và liquidity sau các eligibility screens. Chỉ số dùng free-float adjusted market capitalization, review constituent bán niên và áp dụng cap 10% cho một cổ phiếu, 15% cho nhóm liên quan và 40% cho một sector trong VN30.

Nguồn: [HOSE Index Ground Rules 4.0](https://staticfile.hsx.vn/Uploads/LocalFiles/ef15ff11e799483abd11677ad0443887/20250114_20241230_QD%20747%20HOSE%20Index%20Ground%20Rules.pdf).

Factsheet ngày 30-01-2026 công bố:

| Thuộc tính | VN30 |
|---|---:|
| Constituents | 30 |
| Raw market capitalization | 5,934,776 tỷ VND |
| Free-float adjusted capitalization | 2,280,056 tỷ VND |
| Median adjusted capitalization | 56,669 tỷ VND |
| Published largest-company concentration | 16.62% |
| Published top-10 concentration | 65.53% |
| 1-year volatility | 22.36% |
| 1-year correlation với VN-Index | 97.25% |
| 3-year correlation với VN-Index | 97.24% |
| 5-year correlation với VN-Index | 97.10% |

Nguồn: [HOSE Index Factsheet 30-01-2026](https://staticfile.hsx.vn/Uploads/UploadDocuments/2438018/Form_Factsheet_MCIndices_VN_T02.2026.pdf). Concentration trong bảng là số factsheet công bố; không diễn giải nó như live post-cap portfolio weight nếu chưa có constituent weight file cùng ngày.

### Hệ quả nghiên cứu

1. Chỉ 30 names: một decile có ba cổ phiếu, không đủ an toàn cho tail portfolio thông thường.
2. Top-10 concentration 65.53% làm cap-weighted benchmark shock lấn át stock-specific information.
3. Correlation gần 97% với VN-Index khiến raw trend, beta và broad risk-on signals khó đa dạng hóa.
4. Large-cap có liquidity/capacity tốt hơn nhưng price discovery hiệu quả hơn; alpha nên đến từ slow accounting information, capital allocation hoặc residual return.
5. Cross-sectional market-neutral không tự động hết sector risk. Catalog không có sector field, vì vậy cần accounting-archetype guard và empirical factor residualization.

## 2. Local prior và bằng chứng Việt Nam

`data/vietnam_market_characteristics.md` mô tả `VN-LARGE-CAP` có institutional/foreign participation cao và được định giá kỹ hơn; ưu tiên operating cash flow, margin stability và value cộng momentum, tránh pure growth. Vì catalog không có generic revenue/margin field đủ rộng, master này chuyển “margin stability” thành cash profitability, PAT/asset stability và cash-conversion stability.

Bằng chứng Việt Nam hỗ trợ nhưng không đủ để tuyên bố alpha:

- Value và operating profitability có marginal contribution lớn trong factor models Việt Nam; paper cũng kiểm định cash profitability và ROE profitability. [Choosing Factors for the Vietnamese Stock Market](https://www.mdpi.com/1911-8074/14/3/96)
- EP là value measure mạnh trong horse race Việt Nam, còn turnover là dimension quan trọng; do đó EP được giữ làm control, turnover phải bị kiểm soát. [Vietnam factor evidence](https://www.pbcsf.tsinghua.edu.cn/__local/7/F5/A9/E0366D36DF73499C8CBFB66C505_4D50779F_1C1EEF.pdf)
- Free cash flow có quan hệ dương với profitability trong mẫu 208 listed non-financial firms Việt Nam 2012-2016. [Vietnam FCF evidence](https://ideas.repec.org/a/ebl/ecbull/eb-17-00746.html)
- Foreign investors tại Việt Nam ưu tiên market cap, liquidity và profitability cao, đồng thời tránh leverage và P/B cao. Điều này làm quality/leverage signal có economic prior ở large-cap, nhưng cũng có nguy cơ crowded. [Foreign-investor preferences](https://vjol.info.vn/js/vi/article/view/67494/)
- Institutional ownership được tìm thấy làm giảm firm-level return volatility trong dữ liệu Việt Nam. [Institutional ownership and volatility](https://ideas.repec.org/a/eee/finana/v45y2016icp54-61.html)

## 3. Correlation architecture trước khi nói về idea

### 3.1. Ba loại correlation phải đo

| Measure | Định nghĩa | Vì sao cần |
|---|---|---|
| Full correlation | Pearson và Spearman của aligned daily net PnL | Đo common linear/rank behavior |
| Downside correlation | Correlation chỉ trên ngày incumbent portfolio hoặc VN30 âm | Diversification thường biến mất khi drawdown |
| Co-loss probability | Xác suất cả hai nằm trong bottom decile rolling PnL cùng ngày/tuần | Bắt tail dependence mà Pearson bỏ sót |

Phải báo thêm 63/126-day rolling correlation, correlation theo bull/bear và high/low-volatility regimes. Correlation của raw signal, rank IC hoặc holdings không thay thế PnL correlation.

### 3.2. Research gates

Đây là target để sàng lọc, phải điều chỉnh nếu sample quá ngắn:

1. Candidate standalone: `max(abs(corr(candidate, each small/mid incumbent))) <= 0.30`.
2. Candidate ưu tiên “ultra-low”: cùng metric `<= 0.20` và downside correlation `<= 0.30`.
3. Final large-cap sleeve với combined small+mid incumbent: full correlation target `<= 0.15`, downside target `<= 0.30`.
4. Không nhận candidate chỉ vì correlation âm trong full sample nếu rolling correlation đổi dấu mạnh hoặc co-loss cao.
5. Candidate correlation cao hơn vẫn có thể nhận nếu marginal expected shortfall và portfolio MaxDD giảm rõ trong untouched OOS; phải ghi là hedge/diversifier, không gọi “ultra-low”.

### 3.3. Residualization ladder

Mỗi candidate phải đi qua cùng thứ tự, dùng rolling estimates chỉ từ quá khứ:

1. Remove VN30 beta khỏi stock return hoặc candidate PnL.
2. Remove large-cap EP control.
3. Remove cash-profitability champion Q01/Q02.
4. Remove residual momentum champion M31.
5. Remove turnover/volume-shock champion F41/F42.
6. Cuối cùng regress candidate PnL lên actual small/mid incumbent PnLs và đánh giá residual alpha OOS.

Residualization là diagnostic trước, production implementation sau. Không dùng full-sample regression coefficient vì sẽ leak tương lai.

## 4. Evidence tier và feasibility

| Tier | Ý nghĩa |
|---|---|
| A-VN | Direct Vietnam evidence hoặc official VN market structure |
| A-INT | International peer-reviewed evidence mạnh, cơ chế rõ |
| B | Literature tốt nhưng sign/specification phụ thuộc market |
| C | Novel low-correlation hypothesis; strict untouched OOS bắt buộc |

| Feasibility | Ý nghĩa |
|---|---|
| Ready | Raw fields và primary direction rõ |
| Probe | Phải xác minh sign, YTD/discrete quarterly convention hoặc coverage |
| Experimental | Estimation, breadth hoặc proxy risk cao |

Với 50 hypotheses, `t > 2` không đủ. Dùng false-discovery-aware hurdle, untouched OOS và parameter plateau theo Harvey-Liu-Zhu và factor-zoo tests. [Multiple testing](https://www.nber.org/papers/w20592), [Taming the Factor Zoo](https://www.nber.org/papers/w25481)

## 5. Field map và construction primitives

Catalog dùng chung ba universe có 496 fields; tất cả field dưới đây tồn tại trong `syntax/data_syntax.md`.

### 5.1. Price, volume và benchmark

- `pv_open_panel`, `pv_high_panel`, `pv_low_panel`, `pv_close_panel`, `pv_volume_panel`
- `pv_vn30_open_panel`, `pv_vn30_high_panel`, `pv_vn30_low_panel`, `pv_vn30_close_panel`, `pv_vn30_volume_panel`

### 5.2. Earnings và balance sheet

- `fun_is_eps_basis_quarterly_panel`
- `fun_is_net_profit_loss_after_tax_quarterly_panel`, `fun_is_net_profit_loss_after_tax_annual_panel`
- `fun_is_net_accounting_profit_loss_before_tax_quarterly_panel`
- `fun_bs_total_assets_quarterly_panel`, `fun_bs_owners_equity_quarterly_panel`
- `fun_bs_common_shares_quarterly_panel`, `fun_bs_liabilities_quarterly_panel`
- `fun_bs_cash_and_cash_equivalents_quarterly_panel`, `fun_bs_short_term_investments_quarterly_panel`
- `fun_bs_current_assets_quarterly_panel`, `fun_bs_current_liabilities_quarterly_panel`
- `fun_bs_short_term_loans_quarterly_panel`, `fun_bs_long_term_loans_quarterly_panel`
- `fun_bs_fixed_assets_quarterly_panel`, `fun_bs_construction_in_progress_quarterly_panel`
- `fun_bs_good_will_quarterly_panel`, `fun_bs_intangible_fixed_assets_quarterly_panel`
- `fun_bs_undistributed_earnings_quarterly_panel`, `fun_bs_paid_in_capital_quarterly_panel`, `fun_bs_capital_surplus_quarterly_panel`

### 5.3. Cash flow và capital actions

- `fun_cf_net_cash_inflows_outflows_from_operating_activities_quarterly_panel` và annual
- `fun_cf_operating_profit_loss_before_changes_in_wc_quarterly_panel`
- `fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_quarterly_panel` và annual
- `fun_cf_proceeds_from_disposal_of_fixed_assets_quarterly_panel` và annual
- `fun_cf_proceeds_from_borrowings_quarterly_panel`, `fun_cf_repayment_of_borrowings_quarterly_panel`
- `fun_cf_proceeds_from_issue_of_shares_quarterly_panel`
- `fun_cf_dividends_paid_quarterly_panel`
- `fun_cf_payments_for_share_returns_and_repurchases_quarterly_panel`
- `fun_cf_interest_paid_quarterly_panel`, `fun_cf_business_income_tax_paid_quarterly_panel`
- `fun_cf_net_cash_inflows_outflows_from_investing_activities_quarterly_panel`
- `fun_cf_net_cash_inflows_outflows_from_financing_activities_quarterly_panel`
- `fun_cf_provisions_quarterly_panel`
- `fun_cf_increase_decrease_in_receivables_quarterly_panel`
- `fun_cf_increase_decrease_in_inventories_quarterly_panel`
- `fun_cf_increase_decrease_in_payables_quarterly_panel`

### 5.4. Alias

| Alias | Definition |
|---|---|
| `MV` | `close * common_shares`; split/share-count diagnostic bắt buộc |
| `PAT` | net profit/loss after tax |
| `PBT` | net accounting profit/loss before tax |
| `CFO` | net operating cash flow |
| `PreWCCash` | operating profit/loss before changes in working capital |
| `Assets` | total assets |
| `Equity` | owners equity |
| `Debt` | short-term loans + long-term loans |
| `LiquidAssets` | cash + short-term investments |
| `Capex` | absolute fixed/long-term asset purchases sau sign probe |
| `FCF` | `CFO - Capex` |
| `r_resid` | stock return trừ rolling beta nhân VN30 return; beta chỉ dùng past window |

## 6. Accounting-archetype guard

Large-cap Việt Nam có finance-heavy risk, nhưng catalog không có sector field. Không được so sánh máy móc CFO, working capital, debt hay tangible book giữa ngân hàng, insurer, securities firm và industrial company.

Tạo archetype chỉ để mask/diagnose, không dùng như alpha:

1. **Operating asset:** CFO, fixed assets, receivables/inventory và Capex có coverage material.
2. **Finance-like:** operating-asset fields sparse, liabilities/assets cao và cash-flow statement không comparable.
3. **Project/real asset:** CIP, fixed assets hoặc investment property material.
4. **Sparse reporter:** thiếu numerator/denominator; giữ missing, không zero-impute.

Mỗi accounting idea phải báo pooled result, coverage-consistent result và leave-one-archetype-out result. Nếu alpha biến mất khi loại một archetype, đó là specialized sleeve.

## 7. Bản đồ 50 idea

| ID | Idea | Tier | Feasibility | Mode prior | Correlation prior |
|---|---|---|---|---|---|
| Q01 | Persistent Positive Cash ROA | A-VN/A-INT | Ready | CS | low-medium |
| Q02 | Stable Cash Profitability | A-INT | Ready | CS | low |
| Q03 | Cash Earnings Spread | A-INT | Probe | CS | low |
| Q04 | Pre-Working-Capital Cash Strength | B | Probe | CS | low |
| Q05 | Multi-Year Free-Cash-Flow Consistency | A-VN/B | Probe | CS | very low |
| V06 | Positive Earnings-to-Price Control | A-VN | Ready | CS | medium-high |
| V07 | Operating-Cash-Flow Yield | A-VN/A-INT | Probe | CS | low-medium |
| V08 | Capex-Cycle-Residual FCF Yield | A-VN/A-INT | Probe | CS | low |
| V09 | Enterprise-Adjusted Cash Yield | B | Probe | CS | low |
| V10 | EP-Residual Tangible Book Value | B | Probe | CS | low |
| P11 | FCF-Covered Dividend Yield | B | Probe | CS | low |
| P12 | Persistent Net Payout Yield | A-INT | Probe | CS | low |
| P13 | Shareholder Yield with Debt Paydown | B | Probe | CS | very low |
| P14 | Cash-Supported Deleveraging | B | Probe | CS | very low |
| P15 | Anti-Dilution / Issuance Restraint | A-INT | Probe | CS | low |
| B16 | Net Liquid-Asset Buffer | A-INT | Ready | CS | low |
| B17 | Improving Cash Interest Coverage | A-INT | Probe | CS | low |
| B18 | Short-Term Refinancing Pressure | B | Ready | CS | very low |
| B19 | Capital-Ratio Resilience | A-VN prior | Ready | CS | low-medium |
| B20 | Earned-to-Contributed Capital | B | Ready | CS | low |
| I21 | Cash-Profitability-Neutral Asset Growth | A-INT | Ready | CS | low |
| I22 | Internally Funded Capex | A-INT | Probe | CS | low |
| I23 | Cash-Realized Lagged-Capex Payoff | B | Probe | CS | very low |
| I24 | Construction-in-Progress Commissioning | C | Probe | CS | very low |
| I25 | Asset-Recycling Discipline | C | Probe | CS | very low |
| E26 | Cash-Orthogonal EPS Surprise | A-INT | Probe | CS | low |
| E27 | Cash-Confirmed PAT Surprise | B | Probe | CS | low |
| E28 | Operating-Cash-Flow Surprise | B | Probe | CS | low |
| E29 | Cash-Conversion Inflection | B | Probe | CS | very low |
| E30 | Payout-and-Deleveraging Inflection | C | Probe | CS | very low |
| M31 | Stable VN30-Residual Momentum | A-INT | Experimental | CS | low |
| M32 | VN30-Residual Short-Term Reversal | A-INT | Experimental | CS | very low |
| M33 | Residual 52-Week-High Anchoring | B | Experimental | CS | low |
| M34 | Continuous Residual Trend | B | Experimental | CS | low |
| M35 | Fundamental News Non-Reaction | B/C | Experimental | CS | very low |
| D36 | Downside-Beta Improvement | A-INT | Experimental | CS | low |
| D37 | Upside/Downside Capture Asymmetry | B | Experimental | CS | very low |
| D38 | Low Residual Volatility | A-INT | Experimental | CS | low |
| D39 | Anti-MAX on Residual Returns | A-INT | Experimental | CS | low |
| D40 | Drawdown-Recovery Efficiency | B | Ready | CS | low |
| F41 | Abnormal-Volume Continuation | A-VN/B | Ready | CS | medium |
| F42 | Stock-vs-VN30 Participation Divergence | C | Experimental | CS | very low |
| F43 | Index-Pressure Reversal | B/C | Experimental | CS | very low |
| F44 | Benchmark-Residual Overnight-Gap Reversal | B | Ready | CS | very low |
| F45 | Close-Dominant Institutional Drift | C | Experimental | CS | very low |
| O46 | Stable Cash Yield Orthogonal to EP/Momentum | C | Experimental | CS | very low |
| O47 | Defensive Shareholder Yield | C | Experimental | CS | very low |
| O48 | Capex Payoff without Price Run-Up | C | Experimental | CS | very low |
| O49 | Balance-Sheet Repair with Price Neglect | C | Experimental | CS | very low |
| O50 | Cash Quality under Temporary Flow Pressure | C | Experimental | CS | very low |

`Correlation prior` chỉ là ex-ante hypothesis so với small/mid masters. Không được dùng cột này thay empirical PnL matrix.

## 8. Idea cards chi tiết

### Family Q: Cash profitability và durability

#### Q01. Persistent Positive Cash ROA

- **Cơ chế:** cash-based profitability loại phần accrual dễ đảo chiều; large-cap chỉ được thưởng khi positive cash profitability lặp lại, không phải nhờ một năm working-capital release.
- **Prototype:** trailing annual `CFO / average Assets` gated bởi positive cash ROA trong ít nhất ba của bốn năm gần nhất; level-only version là control.
- **Fields:** CFO annual/quarterly, total assets.
- **Large-cap adaptation:** rank trong accounting archetype; annual primary để giảm payment timing.
- **Correlation role:** persistence gate làm signal chậm hơn raw cash ROA, ROE và momentum sleeves.
- **Failure:** CFO của finance-like firms không comparable; working-capital release tạm thời.

#### Q02. Stable Cash Profitability

- **Cơ chế:** cash-flow volatility liên hệ với return risk và uncertainty; large-cap institutional ownership làm stability đáng định giá hơn one-quarter growth.
- **Prototype:** rolling mean `CFO/Assets` trừ lambda nhân rolling standard deviation trong 3-5 năm.
- **Fields:** annual CFO, total assets; quarterly làm challenger.
- **Guard:** minimum history; test mean và volatility riêng trước composite.
- **Correlation role:** fundamental-volatility state, khác price low-vol D38.
- **Failure:** survivorship/history filter; accounting smoothing; bỏ lỡ turnaround.

#### Q03. Cash Earnings Spread

- **Cơ chế:** cash earnings bền hơn accrual earnings; spread cao cho thấy PAT đã chuyển thành cash.
- **Prototype:** `(CFO - PAT) / lag Assets`, winsorized theo archetype.
- **Fields:** CFO, PAT, total assets.
- **Guard:** annual primary; quarterly sign/YTD probe; require PAT/CFO coverage đồng thời.
- **Correlation role:** accounting quality primitive, có thể hedge earnings-growth sleeve của mid-cap.
- **Failure:** temporary collection/payment timing hoặc legitimate working-capital investment.

#### Q04. Pre-Working-Capital Cash Strength

- **Cơ chế:** `PreWCCash` tách operating earning power khỏi release/build của working capital; hữu ích khi Q03 bị cash timing chi phối.
- **Prototype:** `PreWCCash/Assets`, residualized against PAT/Assets; positive residual là operating cash strength chưa nằm trong earnings.
- **Fields:** operating profit before changes in WC, PAT, assets.
- **Guard:** probe semantic coverage; only coverage-consistent archetypes.
- **Correlation role:** low-frequency accounting residual, không dùng price/volume.
- **Failure:** field classification khác nhau giữa reporters; tax/interest treatment không đồng nhất.

#### Q05. Multi-Year Free-Cash-Flow Consistency

- **Cơ chế:** distributable cash lặp lại quan trọng hơn một FCF yield cao do capex timing.
- **Prototype:** fraction positive annual `FCF/Assets` trong 4-5 năm trừ variability; level FCF yield chỉ là secondary control.
- **Fields:** annual CFO, annual Capex, assets.
- **Guard:** Capex sign probe; minimum four observations; asset archetype only.
- **Correlation role:** rất chậm và sparse, có khả năng low correlation với event/momentum portfolios.
- **Failure:** phạt firms đang đầu tư NPV dương; capex cycle dài; stale holdings.

### Family V: Valuation residual

#### V06. Positive Earnings-to-Price Control

- **Cơ chế:** EP là value measure mạnh trong evidence Việt Nam; cần làm benchmark để biết các value signal mới có thực sự incremental.
- **Prototype:** positive `EPS/close`; robustness bằng `PAT/MV`.
- **Fields:** EPS, PAT, close, common shares.
- **Large-cap adaptation:** không đưa production seed mặc định; dùng control/residualization trước.
- **Correlation role:** medium-high overlap prior với small/mid value; chỉ nhận nếu PnL correlation thực tế thấp.
- **Failure:** cyclical peak earnings; split/share-count mismatch; cheapness không catalyst.

#### V07. Operating-Cash-Flow Yield

- **Cơ chế:** price paid trên realized operating cash khác earnings yield và ít phụ thuộc accrual estimates.
- **Prototype:** trailing annual `CFO/MV`, positive CFO primary.
- **Fields:** CFO, close, common shares.
- **Guard:** archetype and MV diagnostics; residualize against V06.
- **Correlation role:** cash-value bridge; giữ một champion giữa V07/V08/V09 nếu cluster cao.
- **Failure:** high CFO do working-capital harvest hoặc underinvestment.

#### V08. Capex-Cycle-Residual FCF Yield

- **Cơ chế:** trừ Capex khỏi CFO đo cash sau reinvestment, nhưng raw FCF yield dễ chỉ phản ánh firm đang ở đáy Capex cycle; residual construction giữ phần không giải thích bởi investment intensity và EP.
- **Prototype:** annual `(CFO - Capex)/MV`, sau đó cross-sectional residual/rank-neutralization với `Capex/Assets` và V06 EP.
- **Fields:** CFO, Capex, close, common shares.
- **Guard:** positive FCF không bắt buộc nhưng denominator dương; raw FCF yield và Capex intensity phải được báo như legs.
- **Correlation role:** value + capital-allocation signal, dự kiến thấp hơn EP.
- **Failure:** capex lumpy; maintenance/growth capex không phân biệt.

#### V09. Enterprise-Adjusted Cash Yield

- **Cơ chế:** equity yield có thể cao do leverage; enterprise adjustment phạt cash flow phải phục vụ debt holders.
- **Prototype:** `CFO / (MV + Debt - LiquidAssets)`, denominator positive/material.
- **Fields:** CFO, debt, cash, short-term investments, close, shares.
- **Guard:** finance-like firms excluded; V07 và leverage B16/B17 làm controls.
- **Correlation role:** residual cash valuation, tránh duplicate high-leverage value.
- **Failure:** restricted cash; debt fields không đầy đủ; enterprise value proxy thô.

#### V10. EP-Residual Tangible Book Value

- **Cơ chế:** tangible asset claim có thể chứa information khác earnings; residualization tránh biến thành generic value.
- **Prototype:** `(Equity - goodwill - intangible_assets)/MV`, sau đó cross-sectional residual/rank spread với V06.
- **Fields:** equity, goodwill, intangible assets, MV fields.
- **Guard:** tangible equity dương; missing goodwill/intangible không tự zero-fill.
- **Correlation role:** asset-value sleeve chỉ nhận phần orthogonal với EP.
- **Failure:** intangible-heavy quality firms bị phạt; finance/real-estate accounting dominance.

### Family P: Payout và financing policy

#### P11. FCF-Covered Dividend Yield

- **Cơ chế:** dividend yield đơn lẻ dễ là value trap; payout được FCF cover có tính bền vững hơn.
- **Prototype:** `abs(dividends)/MV` gated bởi trailing `FCF > abs(dividends)` hoặc coverage rank.
- **Fields:** dividends paid, CFO, Capex, close, shares.
- **Guard:** annual primary; sign probe; no payout is not automatically bad.
- **Correlation role:** income/cash-allocation state, khác speculative factors.
- **Failure:** banks dùng capital generation khác CFO; special dividend; underinvestment.

#### P12. Persistent Net Payout Yield

- **Cơ chế:** dividends và repurchases là substitutes; subtract issuance đo distribution kinh tế thật, còn persistence tách policy bền khỏi special payout một lần.
- **Prototype:** rolling 3-year mean net payout yield cộng fraction years positive; current raw net payout chỉ là control.
- **Fields:** dividends, repurchases, proceeds from issue of shares, MV.
- **Guard:** annual only; cash-flow sign and coverage report; minimum three observations; cross-check share-count change.
- **Correlation role:** broad payout factor có literature mạnh và khác EP.
- **Failure:** repurchase field sparse; rights issues; cash issuance value không bằng share-count dilution.

#### P13. Shareholder Yield with Debt Paydown

- **Cơ chế:** mature firm trả cash cho capital providers bằng dividends, repurchases và net debt reduction.
- **Prototype:** net payout yield cộng `(repayments - borrowings)/MV`, với prior debt material.
- **Fields:** P12 fields, borrowings, repayments.
- **Guard:** test payout và debt-paydown legs riêng; equal-rank interaction, không fit weights.
- **Correlation role:** slow capital-allocation composite, prior very low với small/mid speculative sleeves.
- **Failure:** refinancing rollover; repayment làm cạn liquidity; sector comparability.

#### P14. Cash-Supported Deleveraging

- **Cơ chế:** repayment action chỉ là quality khi được internal cash support và không phá liquidity buffer; asset-fire-sale deleveraging có meaning khác.
- **Prototype:** positive `(repayments - borrowings)/lag Debt`, require debt stock giảm, CFO dương và `LiquidAssets/Assets` không giảm mạnh.
- **Fields:** borrowings, repayments, short/long loans.
- **Guard:** zero-debt firms excluded; annual anchor; sign probe.
- **Correlation role:** cash-and-liquidity confirmation làm action sleeve khác raw deleveraging factor.
- **Failure:** classification shift; asset sale để trả nợ do distress; debt rollover.

#### P15. Anti-Dilution / Issuance Restraint

- **Cơ chế:** net equity issuance có thể phản ánh market timing và giảm per-share participation.
- **Prototype:** âm YoY common-share growth, confirm bằng issuance proceeds/assets và paid-in-capital change.
- **Fields:** common shares, share issuance, paid-in capital, capital surplus, assets.
- **Guard:** split/stock-dividend detection; no issuance is neutral, not automatically a positive event.
- **Correlation role:** financing policy primitive, khác profitability/momentum.
- **Failure:** rights issue tài trợ project tốt; corporate actions contaminate share count.

### Family B: Balance-sheet resilience

#### B16. Net Liquid-Asset Buffer

- **Cơ chế:** liquid assets vượt interest-bearing debt giảm refinancing downside và tạo optionality.
- **Prototype:** `(LiquidAssets - Debt)/Assets` hoặc cash/debt gated score.
- **Fields:** cash, short-term investments, debt, assets.
- **Guard:** operating firms primary; distinguish state/regulated cash where possible.
- **Correlation role:** defensive balance state, không dùng price signal.
- **Failure:** idle cash/agency cost; finance-like firms; restricted cash.

#### B17. Improving Cash Interest Coverage

- **Cơ chế:** improvement in ability trả interest bằng realized operating cash chứa change information khác coverage level đã được priced.
- **Prototype:** YoY delta `CFO / abs(interest_paid)`, require current coverage positive/material; PreWCCash change là robustness.
- **Fields:** CFO, interest paid, PreWCCash.
- **Guard:** exclude near-zero denominator; annual primary; negative CFO ranked separately.
- **Correlation role:** debt-service improvement event, chậm và sparse hơn static quality.
- **Failure:** interest capitalized; quarterly timing; finance-company interest semantics.

#### B18. Short-Term Refinancing Pressure

- **Cơ chế:** short-term debt wall tạo convex downside ngay cả khi total leverage chưa extreme.
- **Prototype:** âm `(short_term_loans - LiquidAssets)/Assets`; debt-maturity share làm robustness.
- **Fields:** short/long loans, liquid assets, assets.
- **Guard:** no-debt observations neutral; operating archetype.
- **Correlation role:** specific fragility state, prior very low với broad factor returns.
- **Failure:** revolving credit bình thường; undrawn facilities không quan sát được.

#### B19. Capital-Ratio Resilience

- **Cơ chế:** Equity/Assets cao làm shock absorber; local guide cũng dùng capital ratio cho quality.
- **Prototype:** `Equity/Assets`, ưu tiên multi-year minimum hoặc downside percentile thay current level.
- **Fields:** equity, assets.
- **Guard:** compare within archetype; positive equity; current level là control.
- **Correlation role:** defensive state nhưng có thể overlap mid-cap capital-ratio alpha.
- **Failure:** structural finance-sector leverage; excess capital làm thấp ROE.

#### B20. Earned-to-Contributed Capital

- **Cơ chế:** retained earnings relative to contributed capital phản ánh corporate lifecycle và quality của accumulated profits.
- **Prototype:** `undistributed_earnings / (paid_in_capital + capital_surplus)`; positive denominator.
- **Fields:** undistributed earnings, paid-in capital, capital surplus.
- **Guard:** report negative-retained-earnings cohort separately; accounting reset diagnostics.
- **Correlation role:** very slow lifecycle state, khác current earnings change.
- **Failure:** payout policy, revaluation và accounting history làm cross-firm comparison khó.

### Family I: Capital-allocation efficiency

#### I21. Cash-Profitability-Neutral Asset Growth

- **Cơ chế:** high asset growth dự báo return thấp trong literature và effect còn tồn tại ở large-cap, nhưng growth đi cùng persistent cash productivity không nên bị phạt như empire building.
- **Prototype:** annual asset-growth rank residualized against lagged Q01 cash profitability; rank thấp unexplained asset growth được ưu tiên.
- **Fields:** total assets.
- **Guard:** use annual primary; archetype ranks; distinguish organic growth impossible with current fields.
- **Correlation role:** profitability-neutral investment factor, giảm overlap với raw conservative growth.
- **Failure:** productive expansion; M&A/revaluation; finance balance-sheet growth.

#### I22. Internally Funded Capex

- **Cơ chế:** Capex được CFO cover giảm dependence vào issuance/borrowing và refinancing regimes.
- **Prototype:** `CFO - Capex - max(net_external_financing, 0)`, scaled by Assets; two-stage rank preferred.
- **Fields:** CFO, Capex, borrowings, repayments, share issuance, assets.
- **Guard:** test funding gap và Capex level riêng; sign probe.
- **Correlation role:** funding-quality interaction, low prior.
- **Failure:** debt-funded project tốt; capex/payment timing; underinvestment looks good.

#### I23. Cash-Realized Lagged-Capex Payoff

- **Cơ chế:** capital allocation chỉ tốt nếu past Capex tạo later realized cash; PAT improvement đơn độc chưa đủ.
- **Prototype:** current YoY delta CFO divided by Capex published bốn quarters trước, require PAT improvement cùng dấu; PAT-only payoff là control.
- **Fields:** CFO, PAT, Capex, assets.
- **Guard:** pre-register 4-quarter primary lag; cap denominator; causal lag only.
- **Correlation role:** cash-realization gate giảm overlap với mid-cap earnings payoff/growth.
- **Failure:** project horizon dài; maintenance Capex; macro cycle drives payoff.

#### I24. Construction-in-Progress Commissioning

- **Cơ chế:** CIP giảm, fixed assets tăng và CFO/PAT cải thiện cùng lúc có thể báo project đi vào vận hành.
- **Prototype:** equal-rank composite `-delta CIP + delta fixed_assets + delta CFO/Assets`.
- **Fields:** CIP, fixed assets, CFO, PAT, assets.
- **Guard:** project/real-asset archetype; all components point-in-time; no missing-as-zero.
- **Correlation role:** infrequent project event, prior very low.
- **Failure:** reclassification, asset sale hoặc project chưa ramp.

#### I25. Asset-Recycling Discipline

- **Cơ chế:** disposal proceeds đi cùng lower debt hoặc higher FCF có thể là disciplined recycling; disposal để vá cash burn là xấu.
- **Prototype:** disposal proceeds/assets interacted với subsequent debt reduction or positive CFO, penalize persistent negative investing cash flow without payoff.
- **Fields:** disposal proceeds, investing cash flow, CFO, debt, assets.
- **Guard:** pre-register event window and direction; project archetype only.
- **Correlation role:** special situation, expected very low.
- **Failure:** one-off large sale, related-party transaction hoặc shrinking business.

### Family E: Slow fundamental events

#### E26. Cash-Orthogonal EPS Surprise

- **Cơ chế:** PEAD phản ánh delayed incorporation của earnings news; phần EPS surprise không đồng biến với CFO/PAT surprise có thể chứa accrual-specific information khác cash-event sleeves.
- **Prototype:** standardized YoY EPS surprise residual/rank-neutralized against contemporaneous asset-scaled CFO và PAT surprises; event memory 20-60 sessions.
- **Fields:** quarterly EPS, CFO, PAT, assets, close, volume.
- **Guard:** publication-date alignment; 0/1/3/5-day delay test; split diagnostics.
- **Correlation role:** earnings-news residual, designed to avoid duplicating raw SUE và cash-confirmed E27.
- **Failure:** backfill leakage; thin surprise history; residual accrual surprise may be low quality.

#### E27. Cash-Confirmed PAT Surprise

- **Cơ chế:** PAT surprise đáng tin hơn khi CFO or PreWCCash cùng direction; confirmation reduces one-off accounting gains.
- **Prototype:** asset-scaled YoY PAT innovation gated by non-negative CFO innovation.
- **Fields:** PAT, CFO/PreWCCash, assets.
- **Guard:** equal-direction gate, not optimized blend; annual robustness.
- **Correlation role:** filtered event signal, expected lower than raw SUE.
- **Failure:** cash timing makes valid earnings fail; one-off cash receipts.

#### E28. Operating-Cash-Flow Surprise

- **Cơ chế:** cash-flow news có thể khuếch tán khác earnings news và ít được headline-driven trading chú ý.
- **Prototype:** `(CFO_q - CFO_q-4)/lag Assets`, held 20-80 sessions.
- **Fields:** quarterly CFO, assets, PAT.
- **Guard:** discrete-vs-YTD probe; annual sign check; WC component diagnostics.
- **Correlation role:** cash event with low price-factor loading prior.
- **Failure:** seasonality, tax/payment calendar và collection timing.

#### E29. Cash-Conversion Inflection

- **Cơ chế:** change từ PAT không chuyển thành cash sang cash confirmation báo quality inflection chứ không chỉ earnings growth.
- **Prototype:** YoY change in `(CFO-PAT)/Assets`, require PAT not collapsing.
- **Fields:** CFO, PAT, assets.
- **Guard:** scaled change, annual anchor, winsorize.
- **Correlation role:** second-order accounting event, prior very low.
- **Failure:** working-capital liquidation; low base; noisy quarterly convention.

#### E30. Payout-and-Deleveraging Inflection

- **Cơ chế:** management bắt đầu phân phối cash hoặc giảm debt sau phase reinvestment có thể báo lifecycle shift.
- **Prototype:** positive change in net payout rank or net debt repayment rank, conditioned on positive trailing CFO.
- **Fields:** dividends, repurchases, issuance, borrowings, repayments, CFO.
- **Guard:** primary test payout and deleveraging as OR/breadth, not fitted weights.
- **Correlation role:** rare policy event, expected very low.
- **Failure:** payout due lack of growth; forced debt repayment; sparse corporate-action fields.

### Family M: VN30-residual price behavior

#### M31. Stable VN30-Residual Momentum

- **Cơ chế:** ranking on residual returns reduces dynamic common-factor exposure; requiring agreement across horizons avoids a one-window momentum bet. Paper gốc finds residual momentum remains effective in strict large-cap sample.
- **Prototype:** rolling lagged beta, then equal-rank agreement of 12-1 month and 6-1 month standardized `r_resid`; disagreement shrinks exposure.
- **Fields:** stock close, VN30 close; rolling covariance/std primitives.
- **Guard:** 126/252-day beta windows pre-registered; no full-sample regression; liquidity/history minimum.
- **Correlation role:** benchmark removal plus horizon-stability gate distinguishes it from raw/idiosyncratic momentum controls.
- **Failure:** 30-name sector factors remain; beta instability; momentum crashes.

#### M32. VN30-Residual Short-Term Reversal

- **Cơ chế:** temporary stock-specific pressure can reverse after stripping common market shock.
- **Prototype:** negative 5-20 day cumulative `r_resid`, with volume/liquidity cost guard.
- **Fields:** stock/VN30 close, volume.
- **Guard:** lag one day; compare 5/10/20-day plateau; fee stress.
- **Correlation role:** natural complement to M31 medium-term continuation.
- **Failure:** residual news is permanent; turnover and bid-ask costs.

#### M33. Residual 52-Week-High Anchoring

- **Cơ chế:** distance to a benchmark-relative high captures stock-specific anchoring rather than broad bull market.
- **Prototype:** current cumulative residual price state relative to rolling maximum of residual wealth index.
- **Fields:** stock/VN30 close.
- **Guard:** construct residual wealth using lagged beta; no future normalized high.
- **Correlation role:** behavioral anchor with lower market loading than raw 52-week high.
- **Failure:** residual wealth path estimation; corporate actions; sector trend.

#### M34. Continuous Residual Trend

- **Cơ chế:** momentum from many small residual moves is more persistent than a few jumps and less exposed to event lottery demand.
- **Prototype:** sign consistency or fraction positive daily `r_resid` over 3-12 months, controlling cumulative residual return.
- **Fields:** stock/VN30 close.
- **Guard:** test continuous component against M31; avoid fitted jump thresholds.
- **Correlation role:** residual path-shape signal, potentially lower correlation than total momentum.
- **Failure:** stale prices/artificial smoothness; low dispersion in 30 names.

#### M35. Fundamental News Non-Reaction

- **Cơ chế:** surprise mạnh nhưng residual price response yếu là under-reaction candidate; surprise đã fully priced không nên giữ cùng weight.
- **Prototype:** E27/E28 surprise rank minus same-window residual return rank; hold 20-60 days.
- **Fields:** PAT/CFO/EPS, assets, stock/VN30 close.
- **Guard:** event date/delay grid fixed; interaction and legs reported separately.
- **Correlation role:** explicitly removes event-day momentum, prior very low.
- **Failure:** weak response đúng vì news low quality; publication timestamp uncertainty.

### Family D: Downside defense và tail asymmetry

#### D36. Downside-Beta Improvement

- **Cơ chế:** downside covariance là risk dimension khác regular beta; improving downside beta captures a firm becoming more defensive before its long-run beta fully adjusts.
- **Prototype:** negative change in rolling downside beta versus its prior-window estimate, require regular beta not rising materially.
- **Fields:** stock/VN30 close.
- **Guard:** minimum downside observations; shrink toward regular beta; no in-sample mean fitting.
- **Correlation role:** change-in-defense candidate, distinct from static downside-beta sleeves in prior masters.
- **Failure:** beta estimate noisy; defensive names crowd; upside sacrificed.

#### D37. Upside/Downside Capture Asymmetry

- **Cơ chế:** prefer stocks giữ downside nhưng vẫn tham gia upside, khác simple low beta.
- **Prototype:** upside beta/capture minus downside beta/capture, rolling past window.
- **Fields:** stock/VN30 close.
- **Guard:** equal sample definitions; minimum positive/negative market days; winsorize beta ratios.
- **Correlation role:** asymmetry signal designed for low co-loss probability.
- **Failure:** estimation error; regime switch; ratios unstable near zero.

#### D38. Low Residual Volatility

- **Cơ chế:** high idiosyncratic volatility thường liên hệ future return thấp; use residual volatility để giảm common-beta contamination.
- **Prototype:** negative rolling standard deviation of `r_resid`, with liquidity/history guard.
- **Fields:** stock/VN30 close, volume.
- **Guard:** 63/126-day windows; control M31 and archetype concentration.
- **Correlation role:** stock-specific safety factor, expected lower beta than raw low-vol.
- **Failure:** sector crowding; stale prices; low-vol crash in sharp rebounds.

#### D39. Anti-MAX on Residual Returns

- **Cơ chế:** maximum daily return proxies lottery demand; residual MAX removes market-wide jump.
- **Prototype:** negative rolling maximum daily `r_resid` over 21 sessions.
- **Fields:** stock/VN30 close.
- **Guard:** lag signal; compare raw MAX and residual MAX; price-limit days diagnostic.
- **Correlation role:** tail-demand control, not a small-cap lottery core.
- **Failure:** positive jump contains permanent news; overlap D38.

#### D40. Drawdown-Recovery Efficiency

- **Cơ chế:** quality large-cap may absorb shocks and recover without extreme beta; combines depth and recovery speed rather than volatility alone.
- **Prototype:** shallow residual drawdown plus short recovery time over 6-12 months, continuous rank.
- **Fields:** stock/VN30 close.
- **Guard:** define drawdown only from past residual wealth; report depth and speed legs.
- **Correlation role:** path-dependent defense distinct from D36/D38.
- **Failure:** censored unrecovered drawdowns; bull-market bias; complex state logic.

### Family F: Index và flow pressure

#### F41. Abnormal-Volume Continuation

- **Cơ chế:** abnormal volume can proxy investor recognition/attention and predict continuation; Vietnam factor evidence also values turnover.
- **Prototype:** current 5-20 day volume divided by past 126-day baseline, interacted with same-sign residual return.
- **Fields:** volume, stock/VN30 close.
- **Guard:** price-limit and corporate-event days diagnostic; fee stress.
- **Correlation role:** control for attention exposure in every residual test; standalone may overlap mid-cap.
- **Failure:** ETF rebalance pressure reverses; volume field not value turnover.

#### F42. Stock-vs-VN30 Participation Divergence

- **Cơ chế:** stock volume shock relative to VN30 aggregate volume may isolate firm-specific participation from market-wide risk-on flow.
- **Prototype:** z-score stock volume growth minus z-score VN30 volume growth, neutralize residual return.
- **Fields:** stock volume, VN30 volume, stock/VN30 close.
- **Guard:** compare ratio and rank-spread versions; no claim this identifies foreign flow.
- **Correlation role:** benchmark-relative flow proxy, prior very low.
- **Failure:** units/scaling differ; VN30 volume composition changes; no direct order-flow data.

#### F43. Index-Pressure Reversal

- **Cơ chế:** ETF/index-related demand can create temporary price pressure that later reverses.
- **Prototype:** large residual return plus abnormal volume followed by contrarian 3-10 day position; strongest when fundamentals unchanged.
- **Fields:** stock/VN30 close, volume, slow fundamental state.
- **Guard:** event threshold fixed from rolling history; lag one day; F41 continuation is explicit competing hypothesis.
- **Correlation role:** short-horizon contrarian sleeve, expected very low.
- **Failure:** shock is information, not flow; trading costs; cannot observe actual ETF flows.

#### F44. Benchmark-Residual Overnight-Gap Reversal

- **Cơ chế:** close-to-open pressure may reverse intraday in T+1/auction markets; subtract VN30 gap to isolate stock event.
- **Prototype:** negative `(open_t/close_t-1 - vn30_open_t/vn30_close_t-1)`, held open-to-close or short multi-day proxy only if platform execution permits.
- **Fields:** stock/VN30 open and close.
- **Guard:** confirm order timing avoids trading at known open without implementable fill; limit-up/down diagnostics.
- **Correlation role:** intraday-component signal unlike daily factor sleeves.
- **Failure:** open gap is permanent news; execution model may make alpha non-tradable.

#### F45. Close-Dominant Institutional Drift

- **Cơ chế:** repeated benchmark-residual open-to-close strength with neutral overnight gap may proxy slow institutional accumulation near close.
- **Prototype:** 10-20 day sum of residual intraday returns minus residual overnight returns, controlling total residual momentum.
- **Fields:** stock/VN30 open and close, volume.
- **Guard:** empirical sign is two-sided; control M31 and F42; no claim of observed investor identity.
- **Correlation role:** return-component decomposition, prior very low.
- **Failure:** auction mechanics, stale opens, trend repackaging.

### Family O: Pre-registered orthogonal interactions

#### O46. Stable Cash Yield Orthogonal to EP/Momentum

- **Cơ chế:** high stable cash yield should be valuable even after conventional cheapness and trend are removed.
- **Prototype:** V07 CFO yield residualized cross-sectionally against V06, Q02 and M31 using rolling/rank-neutral construction.
- **Fields:** CFO, Capex, EPS/PAT, MV, stock/VN30 close.
- **Guard:** legs and residual reported; coefficients past-only or sequential ranks; no full-sample optimizer.
- **Correlation role:** explicit candidate for `<=0.20` gate.
- **Failure:** residual has little dispersion; unstable regression in 30 names.

#### O47. Defensive Shareholder Yield

- **Cơ chế:** payout is most useful when not merely compensation for high downside risk or leverage.
- **Prototype:** P13 residualized against D36, B16-B18 and V06; retain high payout with resilient downside.
- **Fields:** payout/debt fields, balance sheet, stock/VN30 close.
- **Guard:** separate-sleeve and interaction versions; one family cannot dominate risk.
- **Correlation role:** cash distribution plus tail defense, expected very low.
- **Failure:** over-composite; financial-sector bias; payout fields sparse.

#### O48. Capex Payoff without Price Run-Up

- **Cơ chế:** realized investment payoff not yet reflected in stock-specific price is stronger under-reaction evidence than payoff alone.
- **Prototype:** high I23/I24 score minus prior 3-6 month M31 residual momentum rank.
- **Fields:** Capex/CIP/fixed assets, PAT/CFO, stock/VN30 close.
- **Guard:** payoff leg must work standalone; fixed lag; no post-event price in signal.
- **Correlation role:** fundamental-price disagreement, prior very low.
- **Failure:** price correctly discounts poor payoff persistence; event dating noise.

#### O49. Balance-Sheet Repair with Price Neglect

- **Cơ chế:** improving liquidity/debt service without residual price response can mark an underfollowed large-cap turnaround.
- **Prototype:** positive change breadth across B16-B18/P14 minus recent residual return rank.
- **Fields:** liquid assets, debt, interest/CFO, borrowings/repayments, stock/VN30 close.
- **Guard:** require at least two independent repair legs; price-neglect window pre-registered.
- **Correlation role:** slow turnaround opposed to momentum crowding.
- **Failure:** price weak because operations deteriorate; repair funded by asset fire sale.

#### O50. Cash Quality under Temporary Flow Pressure

- **Cơ chế:** strong Q01-Q05 firm hit by large negative residual return and abnormal volume without negative fundamental update may mean temporary flow pressure.
- **Prototype:** high cash-quality rank interacted with F43-style negative pressure event; contrarian hold 5-20 days.
- **Fields:** cash-quality fields, stock/VN30 close, volume.
- **Guard:** require no adverse PAT/CFO innovation; lag trade; report quality and reversal legs.
- **Correlation role:** quality-conditioned short reversal, strongest ex-ante low-correlation candidate.
- **Failure:** hidden news not in accounting data; value trap; execution costs.

## 9. Academic source map

### Vietnam và market structure

- HOSE: VN30 methodology, investability, free-float, reviews và caps. [Ground Rules](https://staticfile.hsx.vn/Uploads/LocalFiles/ef15ff11e799483abd11677ad0443887/20250114_20241230_QD%20747%20HOSE%20Index%20Ground%20Rules.pdf)
- HOSE: constituent count, capitalization, concentration, volatility và VN-Index correlation. [Factsheet](https://staticfile.hsx.vn/Uploads/UploadDocuments/2438018/Form_Factsheet_MCIndices_VN_T02.2026.pdf)
- Value, operating profitability, cash profitability và ROE factors ở Việt Nam. [Paper](https://www.mdpi.com/1911-8074/14/3/96)
- EP, size, turnover và institutional ownership trong Vietnamese factor evidence. [Paper](https://www.pbcsf.tsinghua.edu.cn/__local/7/F5/A9/E0366D36DF73499C8CBFB66C505_4D50779F_1C1EEF.pdf)
- Free cash flow và corporate profitability tại Việt Nam. [Publication](https://ideas.repec.org/a/ebl/ecbull/eb-17-00746.html)
- Foreign investor preferences cho size, liquidity, profitability, leverage và P/B. [Article](https://vjol.info.vn/js/vi/article/view/67494/)
- Institutional ownership và volatility tại Việt Nam. [Publication](https://ideas.repec.org/a/eee/finana/v45y2016icp54-61.html)

### Cash quality, profitability và investment

- Ball et al.: cash-based operating profitability subsumes accruals in return prediction. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2587199)
- Huang: historical cash-flow volatility negatively predicts future returns, robust to value, momentum, illiquidity và other controls. [Publication](https://www.sciencedirect.com/science/article/abs/pii/S0927539809000036)
- Asness, Frazzini & Pedersen: QMJ defines quality through profitability, growth, safety và management/payout. [Paper](https://www.aqr.com/-/media/AQR/Documents/Insights/Working-Papers/Quality-Minus-Junk.pdf)
- Fama & French: profitability and investment dimensions in five-factor model. [Paper](https://www.aea.ru/data/pdf/fama2015.pdf)
- Cooper, Gulen & Schill: asset growth predicts returns and remains effective in large-cap stocks. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=760967)
- Hirshleifer et al.: net operating asset bloat predicts lower long-run returns. [Research page](https://sites.uci.edu/dhirshle/abstracts/do-investors-overvalue-firms-with-bloated-balance-sheets/)
- Piotroski: financial statement strength separates winners/losers, with implementability caveat important for point-in-time design. [Original](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=249455), [Revisit](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2428946)

### Payout, issuance và capital structure

- Boudoukh et al.: total/net payout yield improves on dividend yield; net payout subtracts equity issuance. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=480171)
- Pontiff & Woodgate: net share issuance predicts cross-sectional returns. [Publication](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2008.01335.x)
- Bradshaw, Richardson & Sloan: net external financing links to future returns/profitability. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=904226)
- DeAngelo, DeAngelo & Stulz: retained earnings relative to contributed capital captures lifecycle/payout state. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=766086)

### Events, residual momentum và behavior

- Bernard/Thomas literature: standardized earnings surprises and PEAD. [Review paper](https://jkatz.caltech.edu/documents/28622/peads.pdf)
- Blitz, Huij & Martens: residual momentum reduces factor risk; in strict large-cap sample Sharpe is 0.60 versus 0.36 for total momentum at one-month holding. [Paper](https://repub.eur.nl/pub/22252/ResidualMomentum-2011.pdf)
- George & Hwang: 52-week high contains information distinct from raw momentum. [Paper](https://onlinelibrary.wiley.com/doi/pdf/10.1111/j.1540-6261.2004.00695.x)
- Da, Gurun & Warachka: continuous information from small price moves predicts more persistent momentum than discrete jumps. [Paper](https://business.uq.edu.au/sites/default/files/events/files/mitch-warachka-paper.pdf)
- Hong & Stein: gradual information diffusion provides behavioral mechanism for continuation. [NBER paper](https://www.nber.org/system/files/working_papers/w6553/w6553.pdf)

### Risk, flow pressure và portfolio science

- Frazzini & Pedersen: betting-against-beta earns risk-adjusted returns across markets under leverage constraints. [NBER](https://www.nber.org/papers/w16601)
- Ang, Chen & Xing: downside risk is distinct from regular beta, liquidity, size, value and momentum. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=875700)
- Ang et al.: idiosyncratic volatility and future returns. [Paper](https://www.ruf.rice.edu/~yxing/AHXZ_011906.pdf)
- Bali, Cakici & Whitelaw: maximum daily return captures lottery-like demand. [NBER](https://www.nber.org/papers/w14804.pdf)
- Staer: ETF flows create price pressure, with part of shock reversing after several days. [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2158468)
- Zhong et al.: abnormal volume shocks predict returns after many controls but direction can be continuation rather than reversal. [Publication](https://www.sciencedirect.com/science/article/pii/S0927538X16302785)
- Short-term reversal evidence separates intraday and overnight components. [Publication](https://doi.org/10.1142/S2010139219500022)
- Geertsema & Lu: many anomaly strategies compress into fewer empirical correlation clusters. [Paper](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID3666663_code1315714.pdf?abstractid=3002797&mirid=1)
- DeMiguel, Garlappi & Uppal: estimation error often prevents optimizers from beating `1/N` OOS. [Paper](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID911512_code23161.pdf?abstractid=911512)

## 10. Anti-overlap map với small/mid masters

| Existing exposure | Large-cap treatment |
|---|---|
| Small-cap extreme Amihud/illiquidity | Không có standalone idea; liquidity chỉ là execution guard |
| Small-cap low nominal price/lottery | Không dùng nominal price; D39 là anti-MAX residual control |
| Small-cap attention/turnover | F41 là control; core mới dùng stock-vs-VN30 divergence F42 và quality-conditioned reversal O50 |
| Mid-cap ROE/growth/scaling | Thay bằng cash durability, payout, capital allocation payoff và balance repair |
| Mid-cap raw/idiosyncratic momentum | M31 residualizes explicitly to VN30; M32/F43 là short reversal complement |
| Mid-cap VN30 graduation frontier | Không dùng constituent prediction vì exact historical membership/free-float không có |
| EP, SUE, asset growth, 52-week high | Chỉ giữ raw definitions làm diagnostic legs; production ideas dùng residual/persistence/change construction |

Một signal dùng fields khác vẫn có thể chung PnL cluster. Ngược lại, cùng field nhưng dùng change/event/residual construction có thể tạo independent sleeve. Quyết định cuối dựa empirical cluster.

## 11. Pipeline cho universe khoảng 30 names

### 11.1. Data probe bắt buộc

1. Xác minh exact `VN-LARGE-CAP` membership và số eligible names theo ngày.
2. Probe quarterly fields là discrete hay YTD; annual làm slow anchor.
3. Fundamental chỉ active sau publication date; delay robustness 0/1/3/5 sessions.
4. Probe cash-flow signs cho Capex, dividends, repayments, repurchases và taxes.
5. Đo coverage từng field và pairwise coverage; missing không zero-impute.
6. Kiểm tra common shares quanh split/stock dividends trước khi tạo MV.
7. Báo pooled/archetype/leave-one-archetype-out results.

### 11.2. Signal construction

1. Safe divide với positive/material denominator.
2. Winsorize 5%-95% hoặc robust rank vì cross-section chỉ khoảng 30 names; 2%-98% gần như không cắt tail.
3. Dùng continuous rank weights, không dùng deciles.
4. `max_abs_weight` và minimum 12-15 eligible names; dưới ngưỡng thì giảm gross exposure.
5. Fundamental rebalance theo event hoặc 20-60 sessions; không daily churn vì dữ liệu không đổi.
6. Beta/residual estimates rolling, lagged và shrinked; không estimate bằng toàn sample.
7. Tách alpha score khỏi liquidity mask, capacity cap và risk controls.

### 11.3. Evaluation stack

- Coverage, dispersion, rank IC, IC t-stat và top-vs-bottom continuous portfolio.
- Gross/net Sharpe, CAGR, MaxDD, Profit Factor, Calmar và turnover.
- Local readiness target: Sharpe >= 1.2, CAGR >= 15%, MaxDD >= -35%, PF >= 1.2, Calmar >= 1.1.
- Bull/bear, high/low VN30 volatility, index-review months và crisis/rebound regimes.
- Pearson/Spearman PnL correlation, downside correlation, co-loss probability.
- Signed holdings overlap, common top/bottom names và empirical cluster.
- Residual alpha after VN30, V06, Q01/Q02, M31, F41/F42 and actual small/mid PnLs.
- Untouched OOS, walk-forward, parameter plateau và fee stress.

## 12. Substitute và complement map

### Substitutes: chỉ giữ một champion mỗi empirical cluster

| Cluster prior | Champion đầu tiên | Challengers |
|---|---|---|
| Cash profitability | Q02 | Q01, Q03-Q05 |
| Cash/value | V08 | V06-V10 |
| Payout/financing | P13 | P11-P15 |
| Balance resilience | B17 hoặc B18 | B16-B20 |
| Capital allocation | I23 | I21-I25 |
| Fundamental event | E28 hoặc E29 | E26-E30 |
| Residual trend | M31 | M33-M35 |
| Defensive price | D36 hoặc D37 | D38-D40 |
| Flow/pressure | F42 hoặc F43 | F41-F45 |
| Orthogonal interactions | O46 hoặc O50 | O47-O49 |

### Complement priors đáng test

- Q02 stable cash profitability + M32 residual reversal: slow quality plus short contrarian.
- P13 shareholder yield + E28 CFO surprise: capital return plus cash event.
- B18 refinancing resilience + M31 residual momentum: balance defense plus firm-specific diffusion.
- I23 lagged-Capex payoff + D36 downside resilience: investment realization plus tail control.
- E29 cash-conversion inflection + F42 participation divergence: accounting event plus relative flow.
- M31 residual momentum + F43 pressure reversal as separate sleeves, không cộng score trực tiếp.
- O46 stable cash yield + O50 temporary pressure: slow valuation and short event barbell.

## 13. Seed portfolios

### Seed A: eight independent mechanisms

| Slot | Candidate | Vai trò |
|---|---|---|
| 1 | Q02 | stable cash quality |
| 2 | V08 | FCF valuation |
| 3 | P13 | shareholder yield |
| 4 | B18 | refinancing resilience |
| 5 | I23 | capital-allocation payoff |
| 6 | E29 | cash-conversion event |
| 7 | M31 | benchmark-residual diffusion |
| 8 | F43 | short pressure reversal |

### Seed B: low-tail-correlation research sleeve

1. Q05 Multi-Year FCF Consistency.
2. P14 Cash-Supported Deleveraging.
3. I24 CIP Commissioning.
4. D37 Upside/Downside Capture Asymmetry.
5. F42 Stock-vs-VN30 Participation Divergence.
6. O50 Cash Quality under Temporary Flow Pressure.

Seed B có prior correlation thấp hơn nhưng nhiều C/Experimental; phải so với Seed A và một simple `1/N` champion portfolio trong untouched OOS.

### Weighting protocol

- Start `1/N` theo empirical cluster, không theo 50 raw ideas.
- Max một champion mỗi cluster; max 20% ex-ante risk cho một family.
- Volatility scaling chỉ dùng lagged/shrunk estimate và caps.
- Covariance optimization chỉ sau shrinkage, weight bounds và turnover penalty.
- Không optimize mean return hoặc pairwise correlation bằng full sample.
- Candidate chỉ được thêm nếu cải thiện OOS Sharpe hoặc expected shortfall và qua correlation gates.

## 14. Research waves

### Wave 1: direct evidence và field feasibility cao

1. Q01 Persistent Positive Cash ROA.
2. Q02 Stable Cash Profitability.
3. Q03 Cash Earnings Spread.
4. V06 EP control.
5. V07 CFO Yield.
6. B16 Net Liquid-Asset Buffer.
7. B19 Capital-Ratio Resilience.
8. I21 Cash-Profitability-Neutral Asset Growth.
9. M31 Stable VN30-Residual Momentum.
10. D38 Low Residual Volatility.

### Wave 2: payout, event và capital allocation

11. V08 Capex-Cycle-Residual FCF Yield.
12. P12 Persistent Net Payout Yield.
13. P13 Shareholder Yield.
14. P14 Cash-Supported Deleveraging.
15. B17 Improving Cash Interest Coverage.
16. I22 Internally Funded Capex.
17. I23 Cash-Realized Lagged-Capex Payoff.
18. E27 Cash-Confirmed PAT Surprise.
19. E28 CFO Surprise.
20. E29 Cash-Conversion Inflection.

### Wave 3: explicit low-correlation experiments

21. M32 Residual Reversal.
22. D36 Downside-Beta Improvement.
23. D37 Capture Asymmetry.
24. F42 Participation Divergence.
25. F43 Index-Pressure Reversal.
26. F44 Residual Gap Reversal.
27. O46 Stable Cash Yield Orthogonal.
28. O48 Capex Payoff without Run-Up.
29. O49 Balance Repair with Neglect.
30. O50 Quality under Flow Pressure.

Các idea còn lại là challengers. Không backtest mọi composite/permutation của 50 ideas.

## 15. Acceptance checklist

- Economic hypothesis, primary formula, direction, lag và holding period pre-registered.
- Exact field load được trên `VN-LARGE-CAP` đúng mode.
- Publication alignment và delay tests không cho thấy leakage.
- Quarterly convention và cash-flow signs đã probe.
- Missing giữ missing; denominator positive/material.
- Pooled result không chỉ do một accounting archetype.
- Eligible breadth đủ; no decile concentration; max weight bounded.
- Net-of-fee result sống qua turnover/slippage stress.
- Signal giữ sign/shape qua subperiods và market regimes.
- Parameter plateau tồn tại; no single best window dependence.
- Candidate sống sau VN30 beta, EP, cash-quality, residual momentum và volume controls.
- Full/downside/rolling correlation và co-loss qua gate với actual small/mid incumbents.
- O-family interaction thắng hoặc cải thiện risk so với từng leg; nếu không thì loại composite.
- OOS portfolio cải thiện Sharpe hoặc tail risk so với simple cluster `1/N`.
- Multiple-testing/FDR được ghi nhận; không cứu failed idea bằng formula mới mà không reset hypothesis.

## 16. Những gì local workspace chưa cho phép kết luận

Workspace không chứa full Round 2 equity dataset, historical universe membership, exact free-float/sector labels, corporate-action calendar, institutional/foreign flow, ETF creations/redemptions hoặc actual PnLs của small/mid masters. Vì vậy hiện chưa thể:

- Khẳng định exact overlap giữa `VN-LARGE-CAP` và VN30.
- Tính coverage, IC, capacity hoặc correlation thật của bất kỳ idea nào.
- Xác nhận F42-F45 quan sát institutional/index flow; chúng chỉ là OHLCV proxies.
- Đảm bảo một idea có `corr <= 0.20` trước backtest.
- Chọn final champions hoặc portfolio weights.

Bước tiếp theo đúng khoa học là chạy một unified data probe trên XNOQuant, implement Wave 1 với cùng OOS split/cost model như small và mid-cap, rồi dùng actual daily PnL matrix để chọn Wave 2-3 theo marginal diversification.


