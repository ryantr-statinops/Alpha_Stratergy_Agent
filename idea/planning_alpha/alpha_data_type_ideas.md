# Alpha Ideas — Leveraging All Data Types

## Mục tiêu
Tận dụng các data type chưa được khai thác từ `syntax/data_syntax.md`:
- **Dow Jones (DJI)**: gần như chưa dùng
- **Futures Daily**: gần như chưa dùng (chỉ T09)
- **VN30 Index**: đã dùng 1 phần (MF_CROSS_MARKET_*, T05, T32) nhưng còn nhiều hướng

---

## Nhóm 1: Dow Jones (global spillover) — 5 ideas

### 1. NC_DJI_GAP_VN30_DRIFT
- **Data**: `pv_dji_close` (T-1), `pv_vn30_open`, `pv_vn30_close`
- **Logic**: Tính DJI overnight return = (dji_close_today - dji_close_yesterday) / dji_close_yesterday. Tính VN30 open drift = (vn30_open - vn30_close_yesterday) / vn30_close_yesterday. Long khi cả 2 cùng dương, short khi cả 2 cùng âm.
- **Exit**: Crossed below/above zero

### 2. DJI Regime Gate
- **Data**: `pv_dji_close`, `pv_close`
- **Logic**: Chỉ long khi DJI > SMA(20), chỉ short khi DJI < SMA(20). Kết hợp với stock price vs SMA(10) để entry.
- **Exit**: DJI crosses SMA(20)

### 3. DJI Divergence
- **Data**: `pv_dji_close`, `pv_close`
- **Logic**: Tính ROC(5) của stock và ROC(5) của DJI. Long khi stock ROC > 0 && DJI ROC < 0 (stock mạnh hơn global). Short khi stock ROC < 0 && DJI ROC > 0.
- **Exit**: ROC đảo chiều

### 4. DJI Volatility Regime
- **Data**: `pv_dji_close`, `pv_dji_high`, `pv_dji_low`
- **Logic**: Tính DJI ATR(10) và DJI ATR SMA(10). Chỉ trade khi DJI ATR < DJI ATR SMA (vol thấp). Kết hợp stock price vs SMA(10).
- **Exit**: DJI ATR > DJI ATR SMA

### 5. DJI-VN30 Spread
- **Data**: `pv_dji_close`, `pv_vn30_close`
- **Logic**: Tính spread = dji_close - vn30_close (normalized). Long khi spread quá thấp (VN30 yếu hơn DJI, kỳ vọng catch-up), short khi spread quá cao.
- **Exit**: Spread về mean

### Nhóm 2: VN30 Index (cross-market)

### 6. VN30 Relative Strength
- **Data**: `pv_vn30_close`, `pv_close`
- **Logic**: Tính ROC(5) của stock và ROC(5) của VN30. Long khi stock ROC > VN30 ROC (outperformance). Short khi stock ROC < VN30 ROC.
- **Exit**: ROC đảo chiều

### 7. VN30 Breakout Confirmation
- **Data**: `pv_vn30_close`, `pv_vn30_high`, `pv_vn30_low`, `pv_close`, `pv_high`, `pv_low`
- **Logic**: Long khi stock close > SMA(10) && VN30 close > SMA(10) (cả 2 cùng uptrend). Short khi cả 2 cùng downtrend.
- **Exit**: Một trong 2 đảo chiều

### 8. VN30 Divergence
- **Data**: `pv_vn30_close`, `pv_close`
- **Logic**: Tính ROC(5) của stock và ROC(5) của VN30. Long khi stock ROC > 0 && VN30 ROC < 0 (stock mạnh hơn thị trường). Short khi stock ROC < 0 && VN30 ROC > 0.
- **Exit**: ROC đảo chiều

### 9. VN30 Volume Surge
- **Data**: `pv_vn30_volume`, `pv_close`
- **Logic**: Tính VN30 volume SMA(10). Long khi VN30 volume > VN30 volume SMA && stock price > SMA(10). Short khi VN30 volume > VN30 volume SMA && stock price < SMA(10).
- **Exit**: VN30 volume < VN30 volume SMA

### 10. VN30 Trend Strength
- **Data**: `pv_vn30_close`, `pv_vn30_high`, `pv_vn30_low`, `pv_close`
- **Logic**: Tính VN30 ADX(10). Chỉ long khi VN30 ADX > 22 && stock price > SMA(10). Chỉ short khi VN30 ADX > 22 && stock price < SMA(10).
- **Exit**: VN30 ADX < 18

### Nhóm 3: Futures Daily (chưa từng dùng)

### 11. Open Interest Trend
- **Data**: `fut_open_interest_vn30f1m_1d`, `pv_close`
- **Logic**: Tính OI change % và price ROC(5). Long khi OI tăng && price ROC > 0 (trend confirmed). Short khi OI tăng && price ROC < 0.
- **Exit**: OI giảm (trend yếu đi)

### 12. Open Interest Divergence
- **Data**: `fut_open_interest_vn30f1m_1d`, `pv_close`
- **Logic**: Long khi price ROC(5) > 0 && OI change < 0 (price tăng nhưng OI giảm = short reversal). Short khi price ROC(5) < 0 && OI change > 0 (price giảm nhưng OI tăng = long reversal).
- **Exit**: OI và price cùng chiều trở lại

### 13. Matched Volume Surge
- **Data**: `fut_matched_volume_vn30f1m_1d`, `pv_close`
- **Logic**: Tính matched volume change % và price ROC(5). Long khi matched volume tăng đột biến && price ROC > 0. Short khi matched volume tăng && price ROC < 0.
- **Exit**: Matched volume giảm về SMA

### 14. Agreed/Matched Ratio
- **Data**: `fut_agreed_volume_vn30f1m_1d`, `fut_matched_volume_vn30f1m_1d`, `pv_close`
- **Logic**: Tính ratio = agreed_volume / matched_volume. Ratio cao = institutional flow. Long khi ratio > SMA(ratio) && price ROC > 0. Short khi ratio > SMA(ratio) && price ROC < 0.
- **Exit**: Ratio < SMA(ratio)

### 15. Total Value Momentum
- **Data**: `fut_total_value_vn30f1m_1d`, `pv_close`
- **Logic**: Tính total value ROC(5) và price ROC(5). Long khi total value ROC > 0 && price ROC > 0. Short khi total value ROC < 0 && price ROC < 0.
- **Exit**: Total value ROC đảo chiều

### Nhóm 4: Cross-data combinations

### 16. VN30 + DJI Spread Mean-Reversion
- **Data**: `pv_vn30_close`, `pv_dji_close`, `pv_close`
- **Logic**: Tính spread = VN30 ROC(5) - DJI ROC(5). Long khi spread quá thấp (VN30 yếu hơn DJI, kỳ vọng catch-up). Short khi spread quá cao.
- **Exit**: Spread về 0

### 17. Futures OI + VN30 Volume
- **Data**: `fut_open_interest_vn30f1m_1d`, `pv_vn30_volume`, `pv_close`
- **Logic**: Long khi OI tăng && VN30 volume > SMA(10) && price ROC(5) > 0. Short khi OI tăng && VN30 volume > SMA(10) && price ROC(5) < 0.
- **Exit**: OI giảm || VN30 volume < SMA(10)

### 18. DJI Gap + VN30 Open Drift
- **Data**: `pv_dji_close`, `pv_vn30_open`, `pv_vn30_close`, `pv_close`
- **Logic**: Tính DJI overnight return = (dji_close_today - dji_close_yesterday) / dji_close_yesterday. Tính VN30 open drift = (vn30_open - vn30_close_yesterday) / vn30_close_yesterday. Long khi cả 2 cùng dương. Short khi cả 2 cùng âm.
- **Exit**: Crossed below/above zero

### 19. Futures Matched Volume + Stock Volume
- **Data**: `fut_matched_volume_vn30f1m_1d`, `pv_volume`, `pv_close`
- **Logic**: Tính matched volume change % và stock volume SMA(10). Long khi matched volume tăng && stock volume > SMA(10) && price ROC(5) > 0. Short khi matched volume tăng && stock volume > SMA(10) && price ROC(5) < 0.
- **Exit**: Matched volume giảm || stock volume < SMA(10)

### 20. VN30 + DJI + Futures Triple Confirmation
- **Data**: `pv_vn30_close`, `pv_dji_close`, `fut_open_interest_vn30f1m_1d`, `pv_close`
- **Logic**: Long khi cả 3 điều kiện đúng: (1) stock ROC(5) > 0, (2) VN30 ROC(5) > 0, (3) DJI ROC(5) > 0, (4) OI tăng. Short khi cả 4 điều kiện ngược lại.
- **Exit**: Bất kỳ 1 trong 4 điều kiện fail

---

## File naming convention

Tất cả file đặt theo pattern: `NC_{DATA_TYPE}_{CONCEPT}_ADX_15min.py`
- NC = Niche Alpha
- DATA_TYPE = DJI, VN30, FUT (futures), CROSS (cross-data)
- CONCEPT = tên ngắn gọn

Ví dụ: `NC_DJI_GAP_VN30_DRIFT_ADX_15min.py`, `NC_VN30_RELATIVE_STRENGTH_ADX_15min.py`, `NC_FUT_OI_TREND_ADX_15min.py`

---

## Implementation notes

- Tất cả dùng tham số 15m chuẩn từ `syntax/parameters.md`
- Tất cả follow framework từ `template_example/strategy_framework.md` (return_roll, session gating, tiered sizing nếu ADX)
- File đặt trong `output/niche_alpha/` với prefix `NC_`
- Không overlap với các file MF_* hiện có trong `output/multi_feat_alpha/`
