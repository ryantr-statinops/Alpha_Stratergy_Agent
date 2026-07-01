# Hypothesis — Thesis 08: Multi-Factor

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 08 — Multi-Factor |
| Timeframes | 15, 30, 60 min |
| Core Indicators | Z-score composite, multi-layer momentum, trend+volume+VN30 |
| Templates | multifactor_zscore, multifactor_momentum, multifactor_trendvol |
| Status | TODO |

---

## HYP-MLT-01: Z-Score Threshold Sensitivity

**Tên:** Z-score threshold nào optimal cho composite signal?

**Null Hypothesis:** Z = 1.5 là optimal (không khác Z = 2.0).

**Alternative Hypothesis:** Z = 1.0 cho Sharpe cao hơn 15% (nhiều tín hiệu hơn), Z = 2.5 cho Win Rate cao hơn 10%.

**Logic test:**
- Template: `multifactor_zscore` — all 8 Z threshold variants
- Đo Sharpe, Win Rate, Signal count

**Metric:** Sharpe, Win Rate, Signal Count, Profit Factor

**Data Range:** 6 tháng, 3 timeframes

**Status:** TODO

---

## HYP-MLT-02: Composite Components Contribution

**Tên:** Component nào đóng góp nhiều nhất vào composite z-score?

**Null Hypothesis:** Tất cả component (price_z, vol_z, mom_z) đóng góp bằng nhau.

**Alternative Hypothesis:** price_z chiếm 50% predictive power, mom_z 30%, vol_z 20%.

**Logic test:**
- So sánh 3 phiên bản:
  1. Full: composite = price_z + mom_z + vol_z
  2. Price only: composite = price_z
  3. Mom only: composite = mom_z
- Đo Sharpe từng phiên bản

**Metric:** Sharpe, Win Rate, Information Coefficient

**Data Range:** 6 tháng

**Status:** TODO

---

## HYP-MLT-03: return_roll with Multi-Factor

**Tên:** Thêm return_roll filter vào multi-factor composite?

**Null Hypothesis:** Composite z-score đã đủ mạnh, return_roll redundant.

**Alternative Hypothesis:** return_roll filter trước composite giúp giảm 30% false signals khi thị trường đi ngang.

**Logic test:**
- Baseline: composite > 1.5
- V1: (composite > 1.5) & (return_roll > 0)
- Đo Win Rate trong ADX < 20 (ranging) environment

**Metric:** Win Rate (ranging), Win Rate (trending), Sharpe

**Data Range:** 6 tháng

**Status:** TODO

---

## HYP-MLT-04: Tiered Sizing for Multi-Factor

**Tên:** Multi-factor strength có nên map thành tiered position không?

**Null Hypothesis:** Single position sizing đủ cho multi-factor.

**Alternative Hypothesis:** Strong composite (|Z| > 2.0) → position 1.0, weak (|Z| 1.0-2.0) → 0.5.

**Logic test:**
- Single: Z > 1.5 → position 1.0
- Tiered: 1.0 < Z < 1.5 → 0.5, Z > 1.5 → 1.0
- Đo Calmar, Sharpe

**Metric:** Calmar Ratio, Sharpe, Max DD

**Data Range:** 6 tháng

**Status:** TODO

---

## Scorecard Target (Multi-Factor Thesis)

| Metric | Target | Pass? |
|--------|--------|-------|
| Sharpe Ratio | ≥ 1.2 | □ |
| Win Rate | ≥ 55% | □ |
| Profit Factor | ≥ 1.7 | □ |
| Max Drawdown | ≤ -25% | □ |
| Calmar Ratio | ≥ 0.9 | □ |
| Signal Count | ≥ 15/tháng | □ |
