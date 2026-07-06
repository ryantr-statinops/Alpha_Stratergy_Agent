# Hypothesis — Thesis 08: Order Book Shadowing (Institutional Footprint Proxy)

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 08 — Order Book Shadowing |
| Timeframes | 15, 30, 60 min |
| Core Data | `fut_open_interest`, `fut_matched_volume`, `fut_matched_value`, `fut_agreed_volume`, `pv_close`, `pv_volume` |
| Key Indicators | `rolling_zscore`, `atr`, `adx`, `roc`, `sma`, `rolling_max/min` |
| Templates | T08-A (OI Wall), T08-B (Absorption), T08-C (Agreed Volume), T08-D (Large Lot Ratio), T08-E (Composite Shadow) |
| Total Variants | ~27 |
| Status | TODO |

---

## HYP-OBS-01: OI Divergence Predictive Power

**Tên:** OI giảm tại key level có dự báo breakout không?

**Null Hypothesis:** OI decrease tại resistance/support là random noise, không có predictive power.

**Alternative Hypothesis:** OI z-score < -1.0 tại resistance/support giúp tăng Win Rate ≥ 55% và Sharpe ≥ 1.2.

**Logic test:**
- T08-A variants với oi_window ∈ [14, 20, 34]
- Measure Win Rate, Sharpe khi OI divergence + price at key level
- So sánh với control: random entry tại key level (không có OI filter)

**Metric:** Sharpe, Win Rate, Profit Factor

**Data Range:** 12 tháng daily futures data

**Status:** TODO

---

## HYP-OBS-02: Volume Absorption Confirmation

**Tên:** Volume spike + range hẹp có phải absorption signal?

**Null Hypothesis:** Volume spike + range hẹp là coincidence, không báo hiệu breakout.

**Alternative Hypothesis:** Absorption pattern (volume > SMA * 1.5 + range < 0.7 × SMA(range)) có Win Rate ≥ 52%.

**Logic test:**
- T08-B variants
- Measure success rate của breakout sau absorption pattern
- Compare với volume spike không có range filter

**Metric:** Win Rate, Sharpe, Avg Breakout Distance

**Data Range:** 12 tháng

**Status:** TODO

---

## HYP-OBS-03: Agreed Volume as Institutional Flow

**Tên:** Surge trong agreed volume có dự báo price move không?

**Null Hypothesis:** Khối lượng thỏa thuận là giao dịch ngẫu nhiên, không ảnh hưởng price direction.

**Alternative Hypothesis:** Agreed volume z-score > 1.5 dự báo price move cùng hướng với 60% accuracy.

**Logic test:**
- T08-C variants với agree_entry ∈ [1.5, 2.0]
- Measure direction accuracy của price sau agreed volume spike
- Check latency: signal → price move trong bao nhiêu bar?

**Metric:** Direction Accuracy, Sharpe, Avg Time-to-Move

**Data Range:** 12 tháng

**Status:** TODO

---

## HYP-OBS-04: Large Lot Ratio vs Retail Dominance

**Tên:** matched_value/matched_volume ratio có detect được institutional flow?

**Null Hypothesis:** Ratio matched_value/matched_volume không khác biệt giữa institutional và retail.

**Alternative Hypothesis:** Ratio z-score > 1.5 xác định institutional dominance với accuracy > 55%.

**Logic test:**
- T08-D variants
- Compare ratio_z > 1.5 vs ratio_z < 0 (retail dominance) performance
- Kết hợp basis premium để confirm direction

**Metric:** Sharpe, Win Rate, Profit Factor

**Data Range:** 12 tháng

**Status:** TODO

---

## HYP-OBS-05: Composite Shadow vs Single Proxy

**Tên:** Kết hợp 4 proxy có tốt hơn dùng từng proxy riêng lẻ?

**Null Hypothesis:** Composite (T08-E) không outperform single proxy templates (T08-A through T08-D).

**Alternative Hypothesis:** Composite shadow với 4 proxies có Sharpe ≥ 20% higher và Win Rate ≥ 5% higher.

**Logic test:**
- T08-E vs weighted average của T08-A, B, C, D
- Kolmogorov-Smirnov test trên equity curves
- Out-of-sample stability comparison

**Metric:** Sharpe, Win Rate, Max DD, Calmar, Overfitting Score (IS/OOS ratio)

**Data Range:** 12 tháng (70% train, 30% test)

**Status:** TODO

---

## Scorecard Target (Thesis 08)

| Metric | Target (User) | Target (Competition) | Pass? |
|--------|:-------------:|:--------------------:|:-----:|
| Sharpe Ratio | ≥ 2.0 | ≥ 1.2 | □ |
| CAGR | ≥ 20% | ≥ 25% | □ |
| Max Drawdown | ≥ -20% | ≥ -40% | □ |
| Sortino Ratio | ≥ 1.5 | ≥ 1.5 | □ |
| Calmar Ratio | ≥ 1.1 | ≥ 0.9 | □ |
| Profit Factor | ≥ 1.3 | ≥ 1.7 | □ |
| Win Rate | ≥ 45% | ≥ 45% | □ |
| Signal Count | ≥ 10/tháng | ≥ 15/tháng | □ |
