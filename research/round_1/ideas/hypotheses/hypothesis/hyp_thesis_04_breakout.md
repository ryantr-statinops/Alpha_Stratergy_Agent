# Hypothesis — Thesis 04: Breakout

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 04 — Breakout |
| Timeframes | 5, 15, 30, 60 min |
| Core Indicators | Rolling quantile, Donchian, range expansion, VN30 confirmation |
| Templates | breakout_quantile, breakout_donchian, breakout_range, breakout_vn30 |
| Status | TODO |

---

## HYP-BRK-01: Quantile Breakout vs Donchian Breakout

**Tên:** Loại breakout nào hiệu quả hơn: quantile hay Donchian?

**Null Hypothesis:** Quantile và Donchian breakout không khác biệt về Win Rate.

**Alternative Hypothesis:** Quantile breakout (Q80) cho Win Rate cao hơn 5% nhưng Donchian cho nhiều tín hiệu hơn 40%.

**Logic test:**
- So sánh `breakout_quantile` vs `breakout_donchian` trên cùng timeframe
- Đo: Win Rate, Signal Count, Profit Factor

**Metric:** Win Rate, Signal Count, Profit Factor

**Data Range:** 6 tháng, 4 timeframes

**Status:** TODO

---

## HYP-BRK-02: Range Expansion Multiplier

**Tên:** Range multiplier nào optimal cho breakout confirmation?

**Null Hypothesis:** range_mult = 1.5 là optimal cho mọi timeframe.

**Alternative Hypothesis:** Range_mult = 2.0 cho Win Rate cao hơn 8% trên 5min; range_mult = 1.3 tốt hơn trên 60min.

**Logic test:**
- Template: `breakout_range` — compare all 7 multiplier variants
- Đo riêng cho từng timeframe

**Metric:** Win Rate, Profit Factor, Sharpe

**Data Range:** 6 tháng

**Status:** TODO

---

## HYP-BRK-03: return_roll + Volume Confirmation

**Tên:** return_roll có cải thiện breakout signal quality không?

**Null Hypothesis:** Volume filter đã đủ, return_roll không thêm giá trị.

**Alternative Hypothesis:** Kết hợp volume + return_roll > 0 giảm 25% false breakout.

**Logic test:**
- Baseline: (close > Q80) & (volume > SMA(vol))
- V1: + return_roll > 0
- V2: + return_roll > 0 + ADX > 20

**Metric:** Win Rate, False Breakout Rate, Sharpe

**Data Range:** 6 tháng

**Status:** TODO

---

## HYP-BRK-04: VN30 Dual Confirmation

**Tên:** Xác nhận từ VN30 có cải thiện breakout signal không?

**Null Hypothesis:** VN30 confirmation không thêm giá trị cho breakout strategy.

**Alternative Hypothesis:** Dual-market breakout (futures + VN30 cùng break) cho Win Rate cao hơn 10% so với single-market.

**Logic test:**
- So sánh `breakout_quantile` (single) vs `breakout_vn30` (dual)
- Đo Win Rate, Profit Factor từng loại

**Metric:** Win Rate, Profit Factor, Max DD

**Data Range:** 6 tháng

**Status:** TODO

---

## Scorecard Target (Breakout Thesis)

| Metric | Target | Pass? |
|--------|--------|-------|
| Sharpe Ratio | ≥ 1.0 | □ |
| Win Rate | ≥ 53% | □ |
| Profit Factor | ≥ 1.5 | □ |
| Max Drawdown | ≤ -30% | □ |
| False Breakout Rate | ≤ 35% | □ |
| Avg Win/Avg Loss | ≥ 1.4 | □ |
