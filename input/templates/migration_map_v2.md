# migration_map_v2 — Template Migration Map (cũ → mới)

> **Mục đích:** Bảng ánh xạ giữa data model vòng 1 (cũ) và vòng 2 (mới). Dùng để tự động hoá migrate file cũ.
> File này là cầu nối giữa 3 file template kia và code generator.
> **Tham chiếu:** [`agent/migration_plan_v2.md`](../../agent/migration_plan_v2.md) — Phase B.

## Cách điền

- Điền **đầy đủ** cho từng entry cũ đã dùng trong `output/` (xem `tools/INDEX.md` để biết field nào đang dùng).
- Cột `Trạng thái`: `giữ nguyên` / `đổi tên` / `xoá` / `thay bằng` / `mới (không có bản cũ)`.
- Nếu đổi tên, ghi tên mới chính xác vào cột `Field/Func mới`.

---

## 1. Data Fields (`self.data.*`)

| Field cũ (vòng 1) | Field mới (vòng 2) | Trạng thái | Ghi chú |
|-------------------|--------------------|------------|---------|
| `pv_open` | | | |
| `pv_high` | | | |
| `pv_low` | | | |
| `pv_close` | | | |
| `pv_volume` | | | |
| `pv_vn30_open` | | | |
| `pv_vn30_high` | | | |
| `pv_vn30_low` | | | |
| `pv_vn30_close` | | | |
| `pv_vn30_volume` | | | |
| `pv_dji_open` | | | |
| `pv_dji_high` | | | |
| `pv_dji_low` | | | |
| `pv_dji_close` | | | |
| `pv_dji_volume` | | | |
| `fut_matched_volume_vn30f1m_1d` | | | |
| `fut_matched_value_vn30f1m_1d` | | | |
| `fut_agreed_volume_vn30f1m_1d` | | | |
| `fut_agreed_value_vn30f1m_1d` | | | |
| `fut_total_volume_vn30f1m_1d` | | | |
| `fut_total_value_vn30f1m_1d` | | | |
| `fut_open_interest_vn30f1m_1d` | | | |
| `vn_interbank_interest_rate_1w_daily` | | | |
| `vn_usd_vnd_sbv_central_daily` | | | |

---

## 2. Feature Functions (`self.feat.*`)

| Function cũ (vòng 1) | Function mới (vòng 2) | Trạng thái | Ghi chú |
|----------------------|-----------------------|------------|---------|
| `sma` | | | |
| `ema` | | | |
| `wma` | | | |
| `kama` | | | |
| `mama` | | | |
| `tema` | | | |
| `trima` | | | |
| `t3` | | | |
| `adx` | | | |
| `dx` | | | |
| `rsi` | | | |
| `stoch` | | | |
| `stochf` | | | |
| `stochrsi` | | | |
| `cci` | | | |
| `cmo` | | | |
| `willr` | | | |
| `macd` | | | |
| `macdfix` | | | |
| `macdext` | | | |
| `ppo` | | | |
| `apo` | | | |
| `trix` | | | |
| `roc` | | | |
| `rocr100` | | | |
| `mom` | | | |
| `atr` | | | |
| `natr` | | | |
| `bbands` | | | |
| `ad` | | | |
| `adosc` | | | |
| `obv` | | | |
| `cmf` | | | |
| `mfi` | | | |
| `bop` | | | |
| `sar` | | | |
| `sarext` | | | |
| `ht_trendline` | | | |
| `dcperiod` | | | |
| `sine` | | | |
| `trendmode` | | | |
| `mavp` | | | |
| `tsf` | | | |
| `linearreg` | | | |
| `linearreg_slope` | | | |
| `linearreg_angle` | | | |
| `linearreg_intercept` | | | |
| `rolling_mean` | | | |
| `rolling_std` | | | |
| `rolling_zscore` | | | |
| `rolling_quantile` | | | |
| `rolling_max` | | | |
| `rolling_min` | | | |
| `rolling_rank` | | | |
| `rolling_vwap` | | | |
| `rolling_corr` / `correl` | | | |
| `rolling_beta` / `beta` | | | |
| `typprice` | | | |
| `wclprice` | | | |
| `medprice` | | | |
| `avgprice` | | | |
| `ohlc4` | | | |
| `midprice` | | | |
| `midpoint` | | | |
| `vwap` | | | |
| candlestick patterns (60) | | | *(liệt kê riêng nếu cần)* |

---

## 3. Operators (`self.op.*`)

| Operator cũ (vòng 1) | Operator mới (vòng 2) | Trạng thái | Ghi chú |
|----------------------|-----------------------|------------|---------|
| `crossed` | | | |
| `crossed_above` | | | |
| `crossed_below` | | | |
| `current` | | | |
| `previous` | | | |
| `shift` | | | |
| `diff` | | | |
| `pct_change` | | | |
| `rising` | | | |
| `falling` | | | |
| `fillna` | | | |
| `ffill` | | | |
| `abs` | | | |
| `clip` | | | |
| `isna` | | | |
| `notna` | | | |
| `isfinite` | | | |
| `zero_ifna` | | | |
| `sign` | | | |
| `replace` | | | |
| `between` | | | |
| `where` | | | |
| `value_when` | | | |
| `bars_since` | | | |
| `hold_for` | | | |
| `crossed_above_value` | | | |
| `crossed_below_value` | | | |
| `and_` | | | |
| `or_` | | | |
| `not_` | | | |

---

## 4. Session Gate Parameters

| Parameter cũ | Parameter mới | Trạng thái | Ghi chú |
|--------------|---------------|------------|---------|
| `position_open_ranges` | | | |
| `position_close_ranges` | | | |
| `position_open_times` | | | |
| `position_close_times` | | | |
| `position_close_after_n_candles` | | | |

---

## Ghi chú thêm (nếu có)

- Field/func mới **không có bản cũ** (chỉ tồn tại ở vòng 2) — liệt kê ở đây:
- Những thay đổi không phải rename (vd đổi return type, đổi số tham số):
- Edge case / cảnh báo khi migrate:
