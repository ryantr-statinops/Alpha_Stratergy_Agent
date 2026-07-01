# Hypothesis — Thesis 01: Momentum

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 01 — Momentum |
| Timeframes | 5, 15, 30, 60 min |
| Core Indicators | ROC, CMO, cascading RO, VN30 confirmation |
| Templates | momentum_pure, momentum_vol, momentum_vn30, momentum_cascade, momentum_cmo |
| Status | TODO |

---

## HYP-MOM-01: Return Roll Filter Impact

**Tên:** Thêm `return_roll` filter có cải thiện Sharpe và giảm số tín hiệu nhiễu không?

**Null Hypothesis:** `return_roll` filter không có tác dụng — signal vẫn giống baseline.

**Alternative Hypothesis:** `return_roll > 0` filter giảm 25% số tín hiệu nhưng tăng Sharpe từ ~0.7 lên ~1.0.

**Logic test:**
- Template: `momentum_pure` — Fast variant
- So sánh 3 phiên bản:
  1. Baseline: ROC(8) > 0 (hiện tại)
  2. V1: (ROC(8) > 0) & (return_roll > 0)
  3. V2: (ROC(8) > 0) & (ROC(8) > ROC(8)_lag) & (return_roll > 0)

**Metric:** Sharpe Ratio, Win Rate, Số tín hiệu/tháng, Max Drawdown

**Data Range:** 6 tháng VN30F1M trên 4 timeframes

**Status:** TODO

---

## HYP-MOM-02: Volume Confirmation Effectiveness

**Tên:** Volume filter (SMA vs quantile) có cải thiện momentum signal không?

**Null Hypothesis:** Volume filter không thêm giá trị cho momentum signal.

**Alternative Hypothesis:** Volume quantile (Q80) filter cho Sharpe > volume SMA filter, cả 2 đều > không filter.

**Logic test:**
- Template: `momentum_vol`
- So sánh:
  1. `momentum_pure` (no vol)
  2. `momentum_vol` (SMA vol)
  3. `momentum_volq` (quantile vol)

**Metric:** Sharpe, Win Rate, Profit Factor, Drawdown

**Data Range:** 6 tháng

**Status:** TODO

---

## HYP-MOM-03: Cascade vs Single ROC

**Tên:** ROC cascade (3-layer) có tốt hơn single ROC không?

**Null Hypothesis:** ROC(F) > ROC(M) > ROC(S) không khác ROC(F) > 0.

**Alternative Hypothesis:** Cascade filter giảm 40% tín hiệu, tăng Win Rate 5-8%.

**Logic test:**
- So sánh `MomFast` (ROC fast) vs `MomCascF8M14S20` (same fast window)
- Đo: Signal count, Win Rate, Profit Factor

**Metric:** Win Rate, Signal Reduction %, Profit Factor

**Data Range:** 6 tháng

**Status:** TODO

---

## HYP-MOM-04: Tiered Sizing Impact

**Tên:** Weak (0.5) / Strong (1.0) sizing có cải thiện Calmar không?

**Null Hypothesis:** Tiered sizing không ảnh hưởng Calmar ratio so với single sizing.

**Alternative Hypothesis:** Tiered sizing giảm 15% drawdown, Calmar tăng 0.2.

**Logic test:**
- Single: position=1.0 khi ROC > 0
- Tiered: weak=0.5 khi ROC>0&ADX>18, strong=1.0 khi ROC>0&ADX>22&vol>base

**Metric:** Calmar Ratio, Max DD, Sharpe

**Data Range:** 6 tháng

**Status:** TODO

---

## Scorecard Target (Momentum Thesis)

| Metric | Target | Pass? |
|--------|--------|-------|
| Sharpe Ratio | ≥ 1.0 | □ |
| Win Rate | ≥ 52% | □ |
| Profit Factor | ≥ 1.5 | □ |
| Max Drawdown | ≤ -30% | □ |
| Calmar Ratio | ≥ 0.8 | □ |
| Signal Reduction | ≤ 40% vs baseline | □ |
