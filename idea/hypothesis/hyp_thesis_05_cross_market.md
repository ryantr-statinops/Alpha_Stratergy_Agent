# Hypothesis — Thesis 05: Cross-Market

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 05 — Cross-Market |
| Timeframes | 15, 30, 60 min |
| Core Indicators | ROC of ratio, DJI spillover, 3-market consensus, gap detection |
| Templates | cross_relative, cross_dji, cross_consensus, cross_gap |
| Status | TODO |

---

## HYP-CRS-01: DJI vs VN30 Predictive Power

**Tên:** DJI hay VN30 có predictive power mạnh hơn cho VN30F1M?

**Null Hypothesis:** DJI và VN30 có cùng mức độ ảnh hưởng.

**Alternative Hypothesis:** VN30 có correlation cao hơn DJI với VN30F1M (0.7 vs 0.3).

**Logic test:**
- So sánh `cross_dji` (DJI + future) vs `momentum_vn30` (VN30 + future)
- Cùng window, cùng timeframe

**Metric:** Sharpe, Win Rate, Correlation with signal

**Data Range:** 6 tháng

**Status:** TODO

---

## HYP-CRS-02: 3-Market Consensus Threshold

**Tên:** Consensus signal (cả 3 market cùng hướng) có mạnh hơn 2-market không?

**Null Hypothesis:** 3-market consensus không khác 2-market về Win Rate.

**Alternative Hypothesis:** 3-market consensus cho Win Rate ≥ 60% nhưng chỉ 1/3 số tín hiệu của 2-market.

**Logic test:**
- So sánh `cross_consensus` (3-market) vs `cross_dji` (2-market)
- Cùng timeframe, cùng window

**Metric:** Win Rate, Signal Count, Profit Factor

**Data Range:** 6 tháng

**Status:** TODO

---

## HYP-CRS-03: return_roll with Cross-Market Signals

**Tên:** Thêm return_roll filter vào cross-market strategies?

**Null Hypothesis:** return_roll không tương thích với cross-market logic (đã có multi-asset filter).

**Alternative Hypothesis:** return_roll > 0 giảm 20% tín hiệu ngược chiều cross-market consensus.

**Logic test:**
- Baseline: consensus = (fut_roc > 0) & (vn30_roc > 0) & (dji_roc > 0)
- V1: + return_roll > 0

**Metric:** Win Rate, Sharpe, Max DD

**Data Range:** 6 tháng

**Status:** TODO

---

## Scorecard Target (Cross-Market Thesis)

| Metric | Target | Pass? |
|--------|--------|-------|
| Sharpe Ratio | ≥ 0.9 | □ |
| Win Rate | ≥ 55% | □ |
| Profit Factor | ≥ 1.5 | □ |
| Max Drawdown | ≤ -25% | □ |
| Signal Count | ≥ 15/tháng | □ |
| VN30 Correlation | ≥ 0.6 | □ |
