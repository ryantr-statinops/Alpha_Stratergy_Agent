# Hypothesis — Thesis 06: Multi-Factor Composite

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 06 — Multi-Factor Composite |
| Core Ideas | Z-score composite (3-factor, 4-factor), Multi-layer confirmation, Candlestick + Z-score, Regime-weighted composite |
| Timeframes | 15, 30, 60 min |
| Templates | T06-A (3-Factor Z), T06-B (4-Factor Z), T06-C (Multi-Layer), T06-D (Candlestick+Z), T06-E (Regime-Weighted) |
| Est. Variants | ~69 |
| Status | TODO |

---

## HYP-MFC-01: Z-Score Composite — Number of Factors

**Tên:** 3-factor hay 4-factor composite cho risk-adjusted return tốt hơn?

**Null Hypothesis:** Thêm factor không cải thiện Sharpe — chỉ tăng complexity.

**Alternative Hypothesis:** 4-factor (price + volume + volatility + cross-market) cho Sharpe cao hơn 3-factor 0.2-0.3 nhờ diversification benefit, dù số tín hiệu giảm 15%.

**Logic test:**
- So sánh T06-A (3F: price + mom + vol) vs T06-B (4F: + cross-market)
- Cùng z-threshold, cùng TF
- Đo Sharpe, diversification ratio

**Metric:** Sharpe, Diversification Ratio, Signal Count, Max DD
**Data Range:** 12 tháng VN30F1M
**Self-critique:** 🟡 Multicollinearity giữa các factors: price_z và mom_z đều từ close → correlation cao. Cần check correlation matrix giữa các factors và loại bỏ factor có correl > 0.7.

---

## HYP-MFC-02: Z-Score Threshold Optimization

**Tên:** Z-score threshold nào optimal cho composite signal?

**Null Hypothesis:** Mọi threshold đều cho kết quả như nhau.

**Alternative Hypothesis:** Threshold 2.0 cho Sharpe cao nhất — balance giữa signal quality và frequency. Threshold 3.0 quá ít tín hiệu (0-2/tháng trên 60min). Threshold 1.0 quá nhiễu.

**Logic test:**
- Template T06-A với 3 factors
- Grid search thresholds: 1.0, 1.5, 2.0, 2.5, 3.0
- Đo Sharpe, signal count, win rate cho từng threshold

**Metric:** Sharpe, Signal Count, Win Rate
**Data Range:** 12 tháng
**Self-critique:** 🔴 Z-score threshold tuning rất dễ overfit. Cần walk-forward validation: tối ưu trên 6 tháng đầu, test trên 6 tháng sau.

---

## HYP-MFC-03: Tiered Sizing — Strong vs Weak Confirmation

**Tên:** Tiered sizing (strong 1.0 / weak 0.5) có cải thiện risk-adjusted return không?

**Null Hypothesis:** Position size không ảnh hưởng đến Sharpe (full size 1.0 cho mọi signal).

**Alternative Hypothesis:** Tiered sizing tăng Sharpe 0.3-0.5 vì strong signals (ADX > 25 + vol_z > 0) được full size, weak signals (ADX 18-22) chỉ 0.5 size — giảm drawdown từ weak signals.

**Logic test:**
- Template T06-A với tiered sizing vs fixed size 1.0
- Đo Sharpe, Max DD, CAGR riêng cho strong vs weak signals

**Metric:** Sharpe (tiered vs fixed), Max DD reduction, CAGR
**Data Range:** 12 tháng
**Self-critique:** 🟡 Weak signals có thể vẫn profitable nhưng bị underweight → mất cơ hội. Cần check PF riêng của weak signals trước khi quyết định underweight.

---

## HYP-MFC-04: Regime-Weighted Composite

**Tên:** Regime-weighted factors có outperform equal-weighted không?

**Null Hypothesis:** Equal-weighted và regime-weighted cho Sharpe tương đương.

**Alternative Hypothesis:** Regime-weighting (trend mode: price+mom nặng; high vol: vol nặng) tăng Sharpe 0.2-0.4 so với equal-weight.

**Logic test:**
- So sánh T06-E (regime-weighted) vs T06-A (equal-weighted 3-factor)
- Cùng threshold, cùng TF
- Đo Sharpe trong từng regime riêng biệt

**Metric:** Sharpe (per regime), Sharpe (overall), Signal Count
**Data Range:** 12 tháng
**Self-critique:** 🔴 Regime detection (ADX, ATR) có lag 1-3 nến → regime-weighted composite có thể dùng sai weights trong regime transition. Cần regime persistence check (≥ 3 nến).

---

## HYP-MFC-05: Candlestick Confirmation Added Value

**Tên:** Candlestick patterns có thêm value cho z-score composite không?

**Null Hypothesis:** Candlestick patterns (hammer, engulfing) không thêm predictive power cho z-score composite.

**Alternative Hypothesis:** Khi composite z-score > 1.5 + bullish candlestick (hammer/engulfing), win rate tăng 8-12% so với chỉ dùng composite. Hiệu quả nhất ở cycle turning points.

**Logic test:**
- Template T06-D: composite vs composite + candlestick
- Test từng pattern riêng biệt: hammer, engulfing, morning_star
- Đo win rate add-on của mỗi pattern

**Metric:** Win Rate Lift, PF Lift, Signal Count
**Data Range:** 12 tháng
**Self-critique:** 🟡 Candlestick patterns hiếm (2-5 lần/tháng trên 60min) → combination với composite còn hiếm hơn. Có thể không đủ statistical power.

---

## Hard Rules Compliance

| Rule | Check | Status |
|------|-------|--------|
| HM-1: Anomaly | Multiple factor guard | ✅ Nhiều factors giảm anomaly impact |
| HM-2: Liquidity | VN30F1M | ✅ |
| HM-3: Continuity | Z-score cần đủ warm-up | ✅ Required |
| RK-1: Risk ≤ 2% | Tiered sizing ≤ 1.0 | ✅ |
| RK-2: Max DD | Weak/strong split giảm DD | ✅ |
| RK-3: Consecutive Loss | Cooldown | ✅ |
| RK-4: Max 3 concurrent | Single position | ✅ |

## Scorecard Targets

| Metric | Weight | Target | Must-pass |
|--------|:------:|--------|:---------:|
| Sharpe Ratio | High | ≥ 2.5 | ✅ (highest target) |
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
| **Strong trend** | Multiple factors confirm, strong size 1.0 |
| **Mixed signals** | Weak size 0.5, bảo vệ drawdown |
| **Regime change** | Regime-weighted adapts, lag 3 nến |
| **Low vol range** | Composite gần 0 → flat, không trade |

## Edge Cases & Failure Scenarios

| Edge Case | Impact | Mitigation |
|-----------|--------|------------|
| **All factors cùng dấu mạnh** | Composite > 5 → overbought? | Clip composite ở [-5, 5] |
| **Factor conflict (price_z > 0, mom_z < 0)** | Composite gần 0 | Flat — chờ đồng thuận |
| **Regime misclassification** | Sai weights cho factors | Regime persistence check ≥ 3 nến |
| **Z-score NaN (new instrument)** | Composite không tính được | Warm-up period, không trade |
| **Threshold quá cao** | 0 tín hiệu trong tháng | Dynamic threshold: nếu 0 signal trong 20 nến → giảm threshold 0.5 |

*End of Hypothesis — Thesis 06*
