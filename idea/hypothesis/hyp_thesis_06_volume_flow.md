# Hypothesis — Thesis 06: Volume & Flow

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 06 — Volume & Flow |
| Timeframes | 15, 30, 60 min |
| Core Data | fut_matched_volume, fut_matched_value, fut_open_interest, fut_total_volume |
| Templates | volume_oi, volume_matched_surge, volume_value, volume_obv, volume_mfi |
| Status | TODO |

---

## HYP-VOL-01: Surge Multiplier Sensitivity

**Tên:** Volume surge multiplier nào optimal cho matched volume?

**Null Hypothesis:** Multiplier không ảnh hưởng — tín hiệu volume surge luôn giống nhau.

**Alternative Hypothesis:** Mult=2.0 cho Win Rate cao hơn 10% so với mult=1.5, dù số tín hiệu giảm 50%.

**Logic test:**
- Template: `volume_matched_surge` — all 7 multiplier variants
- Đo Sharpe, Win Rate, Signal count

**Metric:** Sharpe, Win Rate, Signal Count

**Data Range:** 6 tháng

**Status:** TODO

---

## HYP-VOL-02: OI Trend vs Volume Surge

**Tên:** Tín hiệu nào mạnh hơn: OI tăng hay volume surge?

**Null Hypothesis:** OI trend và volume surge tương đương nhau.

**Alternative Hypothesis:** OI trend cho ít tín hiệu hơn 60% nhưng Win Rate cao hơn 12%.

**Logic test:**
- So sánh `volume_oi` vs `volume_matched_surge`
- Cùng timeframe

**Metric:** Win Rate, Signal Count, Profit Factor

**Data Range:** 6 tháng

**Status:** TODO

---

## HYP-VOL-03: return_roll + Volume Flow

**Tên:** Thêm return_roll filter vào volume strategies?

**Null Hypothesis:** Volume flow độc lập với price momentum, return_roll không liên quan.

**Alternative Hypothesis:** Kết hợp volume surge + return_roll > 0 cho Sharpe ≥ 1.0.

**Logic test:**
- Baseline: (matched_vol > vol_sma * mult) & (matched_vol > vol_q80)
- V1: + return_roll > 0

**Metric:** Sharpe, Win Rate, Profit Factor

**Data Range:** 6 tháng

**Status:** TODO

---

## Scorecard Target (Volume & Flow Thesis)

| Metric | Target | Pass? |
|--------|--------|-------|
| Sharpe Ratio | ≥ 0.8 | □ |
| Win Rate | ≥ 52% | □ |
| Profit Factor | ≥ 1.4 | □ |
| Max Drawdown | ≤ -30% | □ |
| Signal Count | ≥ 10/tháng | □ |
| OI/Price Divergence | Detectable | □ |
