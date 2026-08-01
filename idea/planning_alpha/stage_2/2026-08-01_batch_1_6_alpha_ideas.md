# Alpha Ideas — Batch 1 (Round 2, 6 alphas)

> **Session:** 2026-08-01
> **Trạng thái:** ✅ Đã gen code + validate 0 lỗi (file ở `output/stage_2/`, index ở `output/index.csv`)
> **Mục đích:** Test workflow IDEA → ghi file (stage_2/) → duyệt → gen
> **Universe:** VN-SMALL-CAP / VN-MID-CAP / VN-LARGE-CAP (daily)

---

## Idea 1: VnSmallEpsGrowthMomentum

- **Universe:** VN-SMALL-CAP | **Mode:** time_series | **Level:** 1
- **Thesis:** Small cap ít được phân tích bao phủ → khi EPS quý cải thiện, thị trường định giá lại chậm. Bắt đầu bán khi EPS q/q dương + giá trên trend 20d + volume xác nhận.
- **Fields:** `pv_close`, `pv_volume`, `fun_is_eps_basis_quarterly`, `fun_is_net_profit_loss_after_tax_quarterly`
- **Logic:** `eps_growth > 0` + `profit_growth > 0` + `close > sma20` + `volume > sma20` → full long; exit khi `close < sma20` hoặc `eps_growth < -0.20`.
- **Risk:** fundamentals daily-aligned phẳng giữa các ngày công bố; ngưỡng lỏng chấp nhận false entry.

## Idea 2: VnMidTrendQuality

- **Universe:** VN-MID-CAP | **Mode:** time_series | **Level:** 2
- **Thesis:** Mid cap thưởng cho chất lượng khi xu hướng giữa chu kỳ — ROE cải thiện + cơ cấu vốn lành mạnh lọc bớt momentum thuần.
- **Fields:** `pv_close`, `fun_is_net_profit_loss_after_tax_quarterly`, `fun_is_eps_basis_quarterly`, `fun_bs_owners_equity_quarterly`, `fun_bs_total_assets_quarterly`
- **Logic:** `close > ema54` + `roe > 0.02` + `capital_ratio > 0.10` + profit/eps không suy giảm → 0.5; thêm `ema18 > ema54` + `roe > 0.04` → 1.0; exit khi `close < ema54` hoặc `capital_ratio < 0.06`.
- **Risk:** ROE tĩnh giữa 2 kỳ báo cáo; cần trend filter để không giữ khi giá phá vỡ.

## Idea 3: VnLargeRevenueStability

- **Universe:** VN-LARGE-CAP | **Mode:** time_series | **Level:** 2
- **Thesis:** Large cap được định giá theo độ ổn định — operating cash flow dương + margin ổn định + giá trên trend dài hạn phản ánh mô hình doanh thu lặp lại.
- **Fields:** `pv_close`, `fun_is_net_profit_loss_after_tax_quarterly`, `fun_cf_net_cash_inflows_outflows_from_operating_activities_annual`, `fun_bs_total_assets_quarterly`
- **Logic:** `close > sma60` + `cfo > 0` + `profit_margin > 0.005` → 0.5; thêm `close > ema54` + `profit_margin > 0.01` → 1.0; exit khi `close < sma60` hoặc `cfo < 0`.
- **Risk:** dùng CFO annual (chậm); margin/asset proxy cho stability do catalog không có revenue field tổng quát.

## Idea 4: VnSmallCsEpsRank

- **Universe:** VN-SMALL-CAP | **Mode:** cross_sectional | **Level:** 4
- **Thesis:** Earnings acceleration có thông tin nhất ở small cap (coverage mỏng) — rank cross-section theo delta EPS quý, market-neutral để không đặt cược hướng thị trường.
- **Fields:** `pv_close_panel`, `fun_is_eps_basis_quarterly_panel`
- **Logic:** `eps_growth = safe_divide_panel(delta_panel(eps), eps)`; `eligible = notna(eps) & (eps > 0)`; `weights = portfolio_weights_panel(eps_growth, method='rank_demean_l1', mask=eligible)`.
- **Risk:** nếu ít symbol đủ điều kiện, gross exposure thấp; delta eps nhiễu quanh report date.

## Idea 5: VnMidCsRoERank

- **Universe:** VN-MID-CAP | **Mode:** cross_sectional | **Level:** 4
- **Thesis:** Mid cap tăng trưởng bền khi ROE cao và ổn định — phân bổ vốn theo ROE cross-section, overweight hiệu quả nhất.
- **Fields:** `pv_close_panel`, `fun_is_net_profit_loss_after_tax_quarterly_panel`, `fun_bs_owners_equity_quarterly_panel`
- **Logic:** `roe = safe_divide_panel(net_profit, equity)`; `eligible = notna(net_profit) & (equity > 0)`; `weights = portfolio_weights_panel(roe, method='rank_demean_l1', mask=eligible)`.
- **Risk:** ROE so sánh chéo ngành có quy ước kế toán khác (ngân hàng/bảo hiểm) — caveat của guideline.

## Idea 6: VnLargeCsValueMomentum

- **Universe:** VN-LARGE-CAP | **Mode:** cross_sectional | **Level:** 4
- **Thesis:** Large cap định giá khá hiệu quả — blend earnings yield + price momentum vẫn tách được cổ phiếu vừa rẻ vừa đang được re-rate; hai z-score không để cái nào lấn át.
- **Fields:** `pv_close_panel`, `fun_is_eps_basis_quarterly_panel`
- **Logic:** `ey = safe_divide_panel(eps, close)`; `mom = rolling_zscore_panel(close)`; `signal = zscore_cs_panel(ey) + zscore_cs_panel(mom)`; `weights = portfolio_weights_panel(signal, method='rank_demean_l1', mask=notna(eps) & (close>0))`.
- **Risk:** value + momentum cùng chiều trong regime nhất định → cần theo dõi stability out-of-sample.

---

## Ghi chú chung

- **Mode contract:** time_series long-only `[0,+1]`; cross_sectional market-neutral (`rank_demean_l1`: net≈0, gross=1).
- **Field verified:** chỉ dùng field có trong `syntax/data_syntax.md` (`fun_bs_owners_equity_*`, không có `shareholders_equity`/`total_operating_income`).
- **Point-in-time:** fundamentals chỉ dùng sau ngày công bố; missing = `.notna()`, không zero-fill tỷ số.
