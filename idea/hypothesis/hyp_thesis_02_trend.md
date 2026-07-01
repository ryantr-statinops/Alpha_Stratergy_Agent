# Hypothesis — Thesis 02: Trend Following

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 02 — Trend |
| Timeframes | 5, 15, 30, 60 min |
| Core Indicators | MA cross, MACD, ADX, EMA, Aroon, quantile channel |
| Templates | trend_ma_cross, trend_macd, trend_quantile, trend_ema_adx, trend_aroon |
| Status | TODO |

---

## HYP-TRN-01: ADX Threshold Sensitivity

**Tên:** ADX threshold nào optimal cho trend-following strategies?

**Null Hypothesis:** ADX threshold không ảnh hưởng đáng kể — signal quality giống nhau.

**Alternative Hypothesis:** ADX > 25 cho win rate cao hơn 8% so với ADX > 20, dù số tín hiệu giảm 35%.

**Logic test:**
- Template: `trend_macd` — all 6 ADX variants (Std=20, Strict=25, Mild=15, Aggr=30, Med=18, XAggr=35)
- Đo Sharpe, Win Rate, Signal count cho từng variant

**Metric:** Sharpe, Win Rate, Signal count, Profit Factor

**Data Range:** 6 tháng, 4 timeframes

**Status:** TODO

---

## HYP-TRN-02: MA Crossover Window Selection

**Tên:** Cặp window nào cho MA cross tốt nhất trên từng timeframe?

**Null Hypothesis:** Tất cả cặp window đều cho kết quả tương tự.

**Alternative Hypothesis:** Fast/Slow ratio 1:2 đến 1:4 cho Sharpe cao nhất.

**Logic test:**
- Template: `trend_ma_cross` — compare MA13x26 vs MA13x68 vs MA6x13 vs MA26x68

**Metric:** Sharpe, Win Rate, Avg Trade Duration

**Data Range:** 6 tháng

**Status:** TODO

---

## HYP-TRN-03: return_roll + Trend Confirmation

**Tên:** Thêm return_roll filter vào trend strategies có hiệu quả không?

**Null Hypothesis:** return_roll không thêm giá trị khi đã có ADX filter.

**Alternative Hypothesis:** return_roll > 0 kết hợp ADX > 20 giảm 20% false signals.

**Logic test:**
- Baseline: EMA(20) + ADX(14) > 20
- V1: + return_roll > 0
- V2: + return_roll > 0 & volume > SMA(20)

**Metric:** Sharpe, Win Rate, Profit Factor, Max Consecutive Losses

**Data Range:** 6 tháng

**Status:** TODO

---

## HYP-TRN-04: Trend Exit Optimization

**Tên:** Exit strategy nào cho trend-following tốt nhất?

**Null Hypothesis:** Tất cả exit cho profit factor tương tự.

**Alternative Hypothesis:** Kết hợp ADX < 14 + return_roll < 0 cho PF cao hơn 20% so với ADX < 14 đơn thuần.

**Logic test:**
- Baseline exit: ADX < 14
- V1 exit: ADX < 14 | return_roll < 0
- V2 exit: ADX < 14 | price crosses below EMA

**Metric:** Profit Factor, Avg Win/Avg Loss, Max DD

**Data Range:** 6 tháng

**Status:** TODO

---

## Scorecard Target (Trend Thesis)

| Metric | Target | Pass? |
|--------|--------|-------|
| Sharpe Ratio | ≥ 1.1 | □ |
| Win Rate | ≥ 55% | □ |
| Profit Factor | ≥ 1.6 | □ |
| Max Drawdown | ≤ -25% | □ |
| Avg Trade Duration | 4-12 bars | □ |
| Calmar Ratio | ≥ 0.9 | □ |
