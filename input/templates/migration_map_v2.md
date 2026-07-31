# migration_map_v2 — Migration Map (cũ → mới)

> **Mục đích:** Bảng ánh xạ giữa data model vòng 1 (cũ, intraday futures VNFuture) và vòng 2
> (mới, daily equity fundamentals). Dùng để tự động hoá migrate file cũ.
> **Nguồn:** `agent/stage_2_guideline.md` + `template_example/VN-*/` + `syntax/*_v2.md`.
> **Mode contract:** `time_series` field không suffix (`pv_close`); `cross_sectional` field
> luôn có `_panel` suffix (`pv_close_panel`). Không trộn 2 mode trong 1 strategy.

## Tóm tắt thay đổi lớn

| Hạng mục | Vòng 1 (VNFuture) | Vòng 2 (Equity) |
|----------|-------------------|------------------|
| Sản phẩm | Hợp đồng tương lai VN30 | Cổ phiếu VN (small/mid/large-cap) |
| Khung thời gian | 5/15/30/60 phút | **Daily** |
| Direction | Long + Short | **Long-only** (`[0, +1]`) |
| Session gates | Có (`position_open_ranges`, ...) | **Không còn** |
| Fundamental data | Không có | Có (`fun_is_*`, `fun_bs_*`, `fun_cf_*`) |
| Position API | `self.set_positions(...)` | `self.set_positions(...)` (time_series) / `self.set_portfolio_positions(...)` (cross_sectional) |

---

## 1. Data Fields (`self.data.*`)

| Field cũ (vòng 1) | Field mới (vòng 2) | Trạng thái | Ghi chú |
|-------------------|--------------------|------------|---------|
| `pv_open` | `pv_open` / `pv_open_panel` | giữ nguyên | time_series: `pv_open`; cross_sectional: `pv_open_panel` |
| `pv_high` | `pv_high` / `pv_high_panel` | giữ nguyên | |
| `pv_low` | `pv_low` / `pv_low_panel` | giữ nguyên | |
| `pv_close` | `pv_close` / `pv_close_panel` | giữ nguyên | field chính mọi strategy |
| `pv_volume` | `pv_volume` / `pv_volume_panel` | giữ nguyên | |
| `pv_vn30_open` | `pv_vn30_open` / `pv_vn30_open_panel` | giữ nguyên | |
| `pv_vn30_high` | `pv_vn30_high` / `pv_vn30_high_panel` | giữ nguyên | |
| `pv_vn30_low` | `pv_vn30_low` / `pv_vn30_low_panel` | giữ nguyên | |
| `pv_vn30_close` | `pv_vn30_close` / `pv_vn30_close_panel` | giữ nguyên | |
| `pv_vn30_volume` | `pv_vn30_volume` / `pv_vn30_volume_panel` | giữ nguyên | |
| `pv_dji_open` | — | xoá | không có trong vòng 2 |
| `pv_dji_high` | — | xoá | |
| `pv_dji_low` | — | xoá | |
| `pv_dji_close` | — | xoá | |
| `pv_dji_volume` | — | xoá | |
| `fut_matched_volume_vn30f1m_1d` | — | xoá | futures không còn trong vòng 2 |
| `fut_matched_value_vn30f1m_1d` | — | xoá | |
| `fut_agreed_volume_vn30f1m_1d` | — | xoá | |
| `fut_agreed_value_vn30f1m_1d` | — | xoá | |
| `fut_total_volume_vn30f1m_1d` | — | xoá | |
| `fut_total_value_vn30f1m_1d` | — | xoá | |
| `fut_open_interest_vn30f1m_1d` | — | xoá | |
| `vn_interbank_interest_rate_1w_daily` | — | xoá | |
| `vn_usd_vnd_sbv_central_daily` | — | xoá | |

### Field MỚI (không có bản cũ) — liệt kê đại diện

| Field mới (vòng 2) | Nhóm | Ghi chú |
|--------------------|------|---------|
| `fun_is_net_profit_loss_after_tax_quarterly(_panel)` | IS | lợi nhuận sau thuế |
| `fun_is_net_accounting_profit_loss_before_tax_quarterly(_panel)` | IS | lợi nhuận trước thuế |
| `fun_is_eps_basis_quarterly(_panel)` | IS | EPS cơ bản |
| `fun_is_total_operating_income_quarterly(_panel)` | IS | doanh thu thuần |
| `fun_is_financial_expenses_quarterly(_panel)` | IS | chi phí tài chính |
| `fun_is_financial_income_quarterly(_panel)` | IS | thu nhập tài chính |
| `fun_is_selling_expenses_quarterly(_panel)` | IS | chi phí bán hàng |
| `fun_is_general_and_admin_expenses_quarterly(_panel)` | IS | chi phí QLDN |
| `fun_is_minority_interests_quarterly(_panel)` | IS | lợi ích cổ đông thiểu số |
| `fun_is_net_profit_loss_after_tax_annual(_panel)` | IS | lợi nhuận sau thuế (năm) |
| `fun_bs_total_assets_quarterly(_panel)` | BS | tổng tài sản |
| `fun_bs_owners_equity_quarterly(_panel)` | BS | vốn chủ sở hữu |
| `fun_bs_shareholders_equity_quarterly(_panel)` | BS | vốn CSH (dùng trong example) |
| `fun_bs_current_assets_quarterly(_panel)` | BS | tài sản ngắn hạn |
| `fun_bs_current_liabilities_quarterly(_panel)` | BS | nợ ngắn hạn |
| `fun_bs_total_liabilities_quarterly(_panel)` | BS | tổng nợ |
| `fun_bs_cash_and_cash_equivalents_quarterly(_panel)` | BS | tiền & tương đương tiền |
| `fun_bs_inventories_quarterly(_panel)` | BS | hàng tồn kho |
| `fun_bs_trade_accounts_receivable_quarterly(_panel)` | BS | phải thu khách hàng |
| `fun_bs_total_assets_annual(_panel)` | BS | tổng tài sản (năm) |
| `fun_cf_net_cash_inflows_outflows_from_operating_activities_quarterly(_panel)` | CF | dòng tiền HĐKD |
| `fun_cf_net_cash_inflows_outflows_from_investing_activities_quarterly(_panel)` | CF | dòng tiền đầu tư |
| `fun_cf_net_cash_inflows_outflows_from_financing_activities_quarterly(_panel)` | CF | dòng tiền tài chính |
| `fun_cf_net_cash_inflows_outflows_from_operating_activities_annual(_panel)` | CF | dòng tiền HĐKD (năm) — dùng trong example |
| `fun_cf_depreciation_and_amortisation_quarterly(_panel)` | CF | khấu hao |

> Danh sách đầy đủ 496 fields (10 PV + 130 IS + 271 BS + 85 CF) tại `syntax/data_syntax.md`.

---

## 2. Feature Functions (`self.feat.*`)

> Vòng 1 có 183 features; vòng 2 có 36 panel features (`syntax/feature_syntax.md`) + giữ nguyên
> bản time-series (không `_panel`, có `timeperiod`). Cột "Function mới" ghi cả 2 dạng.

| Function cũ (vòng 1) | Function mới (vòng 2) | Trạng thái | Ghi chú |
|----------------------|-----------------------|------------|---------|
| `sma` | `sma` / `sma_panel` | giữ nguyên | time_series: `sma(close, timeperiod=)`; panel: `sma_panel(close)` |
| `ema` | `ema` / `ema_panel` | giữ nguyên | `ema(close, timeperiod=8)` dùng nhiều trong example |
| `rsi` | `rsi` / `rsi_panel` | giữ nguyên | `rsi(close, timeperiod=7)` trong example |
| `atr` | `atr` / `atr_panel` | giữ nguyên | `atr(high, low, close, timeperiod=14)` trong example |
| `macd` | `macd` / `macd_panel(close, output='macd')` | giữ nguyên | panel trả từng output riêng |
| `bbands` | `bbands` / `bbands_panel(close, output='upper')` | giữ nguyên | panel trả từng band riêng |
| `rolling_mean` | `rolling_mean` / `rolling_mean_panel` | giữ nguyên | |
| `rolling_std` | `rolling_std` / `rolling_std_panel` | giữ nguyên | |
| `rolling_zscore` | `rolling_zscore` / `rolling_zscore_panel` | giữ nguyên | guideline bảo đảm có |
| `rolling_max` | `rolling_max` / `rolling_max_panel` | giữ nguyên | |
| `rolling_min` | `rolling_min` / `rolling_min_panel` | giữ nguyên | |
| `rolling_rank` | `rolling_rank` / `rolling_rank_panel` | giữ nguyên | |
| `rolling_vwap` | `rolling_vwap` / `rolling_vwap_panel` | giữ nguyên | |
| `typprice` | `typprice` / `typprice_panel` | giữ nguyên | |
| `wclprice` | `wclprice` / `wclprice_panel` | giữ nguyên | |
| `medprice` | `medprice` / `medprice_panel` | giữ nguyên | |
| `ohlc4` | `ohlc4` / `ohlc4_panel` | giữ nguyên | |
| `vwap` | `vwap` / `vwap_panel` | giữ nguyên | |
| `cmf` | `cmf` / `cmf_panel` | giữ nguyên | |
| `adx` | — | chưa rõ | không có panel tương đương trong danh sách 36 |
| `dx` | — | chưa rõ | |
| `stoch` | — | chưa rõ | |
| `stochrsi` | — | chưa rõ | |
| `cci` | — | chưa rõ | |
| `cmo` | — | chưa rõ | |
| `willr` | — | chưa rõ | |
| `mom` | — | chưa rõ | |
| `roc` | — | chưa rõ | |
| `obv` | — | chưa rõ | |
| `mfi` | — | chưa rõ | |
| `sar` | — | chưa rõ | |
| `ht_trendline` | — | chưa rõ | |
| candlestick patterns (60) | — | chưa rõ | |

### Feature MỚI (không có bản cũ)

| Function mới (vòng 2) | Ghi chú |
|----------------------|---------|
| `safe_divide_panel` | chia an toàn (denominator dương) — guideline bảo đảm có |
| `returns_panel` | lợi suất panel |
| `log_returns_panel` | log-lợi suất panel |
| `delta_panel` | chênh lệch panel |
| `rolling_sum_panel` | tổng rolling panel |
| `rolling_percentile_rank_panel` | percentile rank rolling panel |
| `rolling_correlation_panel` | tương quan rolling panel |
| `rolling_covariance_panel` | hiệp phương sai rolling panel |
| `hlc3_panel`, `close_location_panel`, `range_pct_panel` | price transforms panel |
| `natr_panel`, `volume_z_panel`, `rolling_value_panel` | volatility/volume panel |
| `amihud_illiquidity_panel` | illiquidity Amihud panel |
| `donchian_upper_panel`, `donchian_lower_panel` | Donchian panel |

---

## 3. Operators (`self.op.*`)

| Operator cũ (vòng 1) | Operator mới (vòng 2) | Trạng thái | Ghi chú |
|----------------------|-----------------------|------------|---------|
| `crossed` | `crossed` | giữ nguyên (time_series) | |
| `crossed_above` | `crossed_above` | giữ nguyên (time_series) | |
| `crossed_below` | `crossed_below` | giữ nguyên (time_series) | |
| `current` | `current` | giữ nguyên (time_series) | |
| `previous` | `previous` | giữ nguyên (time_series) | |
| `shift` | `shift` | giữ nguyên (time_series) | |
| `diff` | `diff` | giữ nguyên (time_series) | |
| `pct_change` | `pct_change` | giữ nguyên (time_series) | dùng nhiều trong example: `pct_change(series, periods=1)` |
| `rising` | `rising` | giữ nguyên (time_series) | |
| `falling` | `falling` | giữ nguyên (time_series) | |
| `fillna` | `fillna` | giữ nguyên (time_series) | dùng nhiều trong example: `fillna(x, value=0)` |
| `ffill` | `ffill` | giữ nguyên (time_series) | |
| `abs` | `abs` | giữ nguyên (time_series) | |
| `clip` | `clip` | giữ nguyên (time_series) | |
| `isna` | `isna` | giữ nguyên (time_series) | |
| `notna` | `notna` | giữ nguyên (time_series) | guideline yêu cầu dùng `.notna()` cho missing fundamentals |
| `isfinite` | `isfinite` | giữ nguyên (time_series) | |
| `zero_ifna` | `zero_ifna` | giữ nguyên (time_series) | |
| `sign` | `sign` | giữ nguyên (time_series) | |
| `replace` | `replace` | giữ nguyên (time_series) | |
| `between` | `between` | giữ nguyên (time_series) | |
| `where` | `where` | giữ nguyên (time_series) | |
| `value_when` | `value_when` | giữ nguyên (time_series) | |
| `bars_since` | `bars_since` | giữ nguyên (time_series) | |
| `hold_for` | `hold_for` | giữ nguyên (time_series) | |
| `crossed_above_value` | `crossed_above_value` | giữ nguyên (time_series) | |
| `crossed_below_value` | `crossed_below_value` | giữ nguyên (time_series) | |
| `and_` | `and_` | giữ nguyên (time_series) | |
| `or_` | `or_` | giữ nguyên (time_series) | |
| `not_` | `not_` | giữ nguyên (time_series) | |

### Operator MỚI (cross_sectional — không có bản cũ)

| Operator mới (vòng 2) | Syntax | Ghi chú |
|----------------------|--------|---------|
| `rank_cs_panel` | `self.op.rank_cs_panel(panel, mask=None, method='average')` | percentile rank mỗi timestamp |
| `demean_cs_panel` | `self.op.demean_cs_panel(panel, mask=None, winsorize=None)` | trừ cross-sectional mean |
| `normalize_l1_cs_panel` | `self.op.normalize_l1_cs_panel(panel, mask=None, eps=1e-12)` | chuẩn hoá L1 exposure = 1 |
| `winsorize_cs_panel` | `self.op.winsorize_cs_panel(panel, mask=None, lower=0.02, upper=0.98)` | clip theo quantile |
| `zscore_cs_panel` | `self.op.zscore_cs_panel(panel, mask=None, ddof=1)` | z-score cross-section |
| `portfolio_weights_panel` | `self.op.portfolio_weights_panel(signal, method='rank_demean_l1', mask=None, ...)` | weight market-neutral |

---

## 4. Session Gate Parameters

| Parameter cũ | Parameter mới | Trạng thái | Ghi chú |
|--------------|---------------|------------|---------|
| `position_open_ranges` | — | xoá | Round 2 là daily equity, không có phiên intraday |
| `position_close_ranges` | — | xoá | |
| `position_open_times` | — | xoá | |
| `position_close_times` | — | xoá | |
| `position_close_after_n_candles` | — | xoá | |

---

## Ghi chú thêm (migrate code cũ → mới)

- **Chiến lược futures vòng 1 không migrate tự động được** — sản phẩm khác (VN30 futures → equity),
  khung khác (intraday → daily), direction khác (long/short → long-only). Cần viết lại từ đầu theo
  `template_example/VN-*/`.
- **`self.set_positions()` giữ nguyên** cho time_series mode (bounds `[0, +1]`).
- **`self.set_portfolio_positions()` là API mới** cho cross_sectional mode.
- **Fundamental fields (`fun_*`) chưa từng tồn tại ở vòng 1** — migrate phải thêm tầng dữ liệu này.
- Khi migrate, thay tham số thời gian session (ranges/times) bằng **daily logic** (trend/fundamental gates).
- Các feature chưa rõ panel tương đương (adx, stoch, ...) cần xác minh trên platform trước khi dùng.
