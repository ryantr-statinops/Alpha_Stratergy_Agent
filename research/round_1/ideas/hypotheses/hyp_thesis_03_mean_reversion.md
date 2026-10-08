# Hypothesis — Thesis 03: Mean Reversion

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 03 — Mean Reversion |
| Timeframes | 5, 15, 30, 60 min |
| Core Indicators | Rolling quantile, RSI, BBands, CCI, volume climax |
| Templates | meanrev_quantile, meanrev_rsi, meanrev_bbands, meanrev_volclimax, meanrev_cci |
| Status | TODO |

---

## HYP-MRV-01: Quantile Threshold Sensitivity

**Tên:** Ngưỡng quantile nào optimal cho mean reversion entry?

**Null Hypothesis:** q=0.90/0.10 và q=0.95/0.05 cho win rate tương tự.

**Alternative Hypothesis:** q=0.95/0.05 cho win rate cao hơn 10% nhưng số tín hiệu giảm 60%.

**Logic test:**
- Template: `meanrev_quantile` — all 8 quantile variants
- Đo Win Rate, Signal count, Profit Factor cho từng q

**Metric:** Win Rate, Signal Count/month, Profit Factor

**Data Range:** 6 tháng

**Status:** TODO

---

## HYP-MRV-02: RSI Threshold Optimization

**Tên:** RSI threshold nào optimal cho mean reversion?

**Null Hypothesis:** RSI(30/70) là optimal.

**Alternative Hypothesis:** RSI(25/75) cho PF cao hơn 15% dù số tín hiệu giảm 30%.

**Logic test:**
- Template: `meanrev_rsi` — all 7 RSI threshold variants
- Compare Sharpe, Win Rate, PF across variants

**Metric:** Sharpe, Win Rate, Profit Factor, Max DD

**Data Range:** 6 tháng

**Status:** TODO

---

## HYP-MRV-03: return_roll Filter for Reversion

**Tên:** return_roll có giúp mean reversion tránh trend days không?

**Null Hypothesis:** return_roll không phân biệt được reversion vs trend.

**Alternative Hypothesis:** Thêm `abs(return_roll) < threshold` filter giảm 30% false signals trong trend days.

**Logic test:**
- Baseline: close < quantile(0.10) → long
- V1: + abs(return_roll) < 0.001 (chỉ reversion khi momentum yếu)

**Metric:** Win Rate (trend days), Win Rate (range days), Sharpe

**Data Range:** 6 tháng, phân loại ADX > 25 (trend) vs ADX < 20 (range)

**Status:** TODO

---

## HYP-MRV-04: Exit Strategy Comparison

**Tên:** Exit nào tốt nhất cho mean reversion: về median hay RSI 50?

**Null Hypothesis:** Tất cả exit cho kết quả tương tự.

**Alternative Hypothesis:** Exit về rolling median cho PF cao hơn 20% so với exit RSI 50.

**Logic test:**
- Entry: close < quantile(0.10) (oversold)
- So sánh 3 exit:
  1. crossed_above(close, rolling_quantile(close, 14, 0.50))
  2. crossed_above(rsi, 50)
  3. crossed_above(close, rolling_mean(close, 14))

**Metric:** Profit Factor, Avg Win/Avg Loss, Max DD

**Data Range:** 6 tháng

**Status:** TODO

---

## Scorecard Target (Mean Reversion Thesis)

| Metric | Target | Pass? |
|--------|--------|-------|
| Sharpe Ratio | ≥ 0.9 | □ |
| Win Rate | ≥ 50% | □ |
| Profit Factor | ≥ 1.4 | □ |
| Max Drawdown | ≤ -25% | □ |
| Avg Win/Avg Loss | ≥ 1.3 | □ |
| False Signal Rate (trend) | ≤ 40% | □ |
