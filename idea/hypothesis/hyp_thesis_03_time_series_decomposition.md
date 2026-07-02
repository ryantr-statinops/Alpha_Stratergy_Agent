# Hypothesis — Thesis 03: Time-Series Decomposition

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 03 — Time-Series Decomposition |
| Core Ideas | Hilbert Transform (trendline, sine, trendmode), Linear Regression, Entropy proxy (MAD/STD) |
| Timeframes | 15, 30, 60 min (5min quá nhiễu cho decomposition) |
| Templates | T03-A (Hilbert Trend + Sine Cycle), T03-B (DCPeriod Adaptive Sizing), T03-C (LinReg Slope), T03-D (Sine Crossover), T03-E (Dispersion Entropy Proxy) |
| Est. Variants | ~38 |
| Status | TODO |

---

## HYP-TSD-01: Hilbert Trendline vs SMA — Lag Comparison

**Tên:** Hilbert Transform trendline có lag ít hơn SMA cùng window không?

**Null Hypothesis:** ht_trendline và SMA(close, 14) có lag tương đương.

**Alternative Hypothesis:** ht_trendline lag ít hơn SMA 40-50% — phát hiện trend reversal sớm hơn 2-3 nến trên 15min TF.

**Logic test:**
- So sánh ht_trendline vs SMA(14), SMA(34), KAMA(14)
- Đo lag tại trend reversal points (xác định bằng linearreg_slope đổi dấu)

**Metric:** Lag (nến), Crossover Timing Accuracy, Win Rate
**Data Range:** 6 tháng VN30F1M (15min + 30min)
**Self-critique:** 🟡 ht_trendline dễ bị nhiễu trong ranging market do Hilbert Transform nhạy với cycle component. Cần kết hợp trendmode filter.

---

## HYP-TSD-02: Sine/Leadsine Crossover — Cycle Turning Point Reliability

**Tên:** Sine/Leadsine crossover có đáng tin cậy để detect cycle turning points không?

**Null Hypothesis:** Sine/Leadsine crossover là random — không predictive cho price reversal.

**Alternative Hypothesis:** Sine > Leadsine signal báo bullish reversal với win rate ≥ 55% trên 30min TF, đặc biệt hiệu quả trong cycle mode (trendmode = 0).

**Logic test:**
- Template T03-D (Sine Crossover)
- So sánh sine crossover signal vs actual price reversal trong 3 nến
- Phân riêng cycle mode (trendmode = 0) vs trend mode

**Metric:** Win Rate, Lead (nến trước reversal), PF
**Data Range:** 6 tháng
**Self-critique:** 🔴 Sine/Leadsine crossover có thể false positive liên tục trong strong trend (trendmode = 1). Bắt buộc phải filter bằng trendmode.

---

## HYP-TSD-03: Linear Regression Slope — Trend Strength Measure

**Tên:** Linear regression slope có phải là trend strength indicator tốt không?

**Null Hypothesis:** LinReg slope không khác ROC về predictive power.

**Alternative Hypothesis:** LinReg slope (angle) cho trend strength measurement ổn định hơn ROC vì nó smooth nhiễu qua regression. Slope kết hợp angle filter (angle > 5°) cho PF cao hơn ROC 10%.

**Logic test:**
- Template T03-C
- So sánh: linreg_slope > 0 vs roc > 0 vs angle > 5°
- Đo stability: standard deviation của signal over time

**Metric:** PF, Signal Stability (std dev), Win Rate
**Data Range:** 6 tháng
**Self-critique:** 🟡 LinReg slope tuyến tính — không capture được acceleration. Kết hợp với ROC để có cả trend + momentum.

---

## HYP-TSD-04: Entropy Proxy — MAD/STD Ratio as Market State Filter

**Tên:** MAD/STD ratio có đo được "structured" vs "chaotic" market không?

**Null Hypothesis:** MAD/STD ratio là random noise — không filter được market regime.

**Alternative Hypothesis:** Khi MAD/STD < 0.8 → market structured (trend following hiệu quả). Khi MAD/STD > 1.2 → chaotic (nên flat). Filter này tăng Sharpe 0.3-0.5.

**Logic test:**
- Template T03-E
- So sánh: có filter vs không filter
- Phân tích phân phối của MAD/STD ratio theo regime (ADX)

**Metric:** Sharpe với filter vs không filter, % time flat
**Data Range:** 12 tháng
**Self-critique:** 🔴 MAD/STD ratio cần window đủ lớn (≥ 20) để ổn định — trên 5min TF sẽ lag quá nhiều. Chỉ phù hợp 30-60min.

---

## HYP-TSD-05: Dominant Cycle Period — Adaptive Sizing Logic

**Tên:** DCPeriod có đáng tin cậy để điều chỉnh position size không?

**Null Hypothesis:** DCPeriod là random — không nên dùng để scale position.

**Alternative Hypothesis:** Khi cycle period ngắn (< 10 nến) → market noisy → giảm size 50%. Khi cycle period dài (> 30 nến) → strong trend → full size. Adaptive sizing tăng Sharpe 0.2.

**Logic test:**
- Template T03-B
- Compare fixed size (1.0) vs adaptive size (clamp(dcperiod/30, 0.3, 1.0))

**Metric:** Sharpe, Max DD, CAGR
**Data Range:** 6 tháng
**Self-critique:** 🟡 DCPeriod có thể unstable — cần smooth bằng SMA(10) trước khi dùng. Nếu cycle_period = NaN (Hilbert không hội tụ), fallback về default size 0.5.

---

## Hard Rules Compliance

| Rule | Check | Status |
|------|-------|--------|
| HM-1: Anomaly | Hilbert Transform robust với gap | ✅ ht_trendline xử lý gap tốt hơn SMA |
| HM-2: Liquidity | VN30F1M spread ổn định | ✅ |
| HM-3: Continuity | Cycle calculation cần đủ data | ✅ Warm-up period required |
| RK-1: Risk ≤ 2% | Position bounds [-1, +1] | ✅ |
| RK-2: Max DD | Trendmode + ADX filter | ✅ |
| RK-3: Consecutive Loss | Cooldown period | ✅ |
| RK-4: Max 3 concurrent | Single position | ✅ |

## Scorecard Targets

| Metric | Weight | Target | Must-pass |
|--------|:------:|--------|:---------:|
| Sharpe Ratio | High | ≥ 2.0 | ✅ |
| CAGR | High | > 20% | ✅ |
| Max Drawdown | High | > -20% | ✅ |
| Sortino Ratio | Medium | ≥ 1.5 | |
| Calmar Ratio | Medium | ≥ 1.1 | |
| Profit Factor | Medium | ≥ 1.3 | |
| VaR 95% | Medium | ≥ -5% | |
| CVaR 95% | Low | ≥ -6% | |
| Ulcer Index | Low | ≤ 12 | |
| Cost | Low | ≤ 1% | |
| Correlation | Low | ≤ 0.8 | |

## Backtest Scenarios

| Scenario | Expectation |
|----------|-------------|
| **Strong trend** | HT trendline bám trend tốt, PF > 1.5 |
| **Cycle market** | Sine/Leadsine turning points hiệu quả |
| **Ranging** | trendmode = 0 → cycle trading hoặc flat |
| **Gap day** | ht_trendline ít bị distorted hơn SMA |

## Edge Cases & Failure Scenarios

| Edge Case | Impact | Mitigation |
|-----------|--------|------------|
| **Hilbert không hội tụ** | trendmode = NaN, sine = NaN | `self.op.isfinite()` guard, fallback SMA |
| **DCPeriod = 0** | Division by zero trong vol_scale | Clip min 0.3 |
| **Trendmode liên tục flip** | Chuyển trend/cycle liên tục | Chỉ trade khi trendmode ổn định ≥ 3 nến |
| **Sine/Leadsine trong strong trend** | False cycle signals | Filter bằng trendmode == 0 |
| **MAD/STD ratio NaN** | Entropy filter không hoạt động | Fallback: bỏ qua entropy filter |

*End of Hypothesis — Thesis 03*
