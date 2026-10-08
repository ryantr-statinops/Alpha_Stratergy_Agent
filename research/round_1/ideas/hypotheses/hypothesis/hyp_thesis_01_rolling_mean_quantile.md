# Hypothesis — Thesis 01: Rolling Mean + Quantile

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 01 — Rolling Mean + Quantile |
| Core Ideas | Rolling Mean, Rolling Quantile, Z-Score, KAMA/MAMA |
| Timeframes | 5, 15, 30, 60 min |
| Templates | T01-A (Price vs Mean), T01-B (Crossover), T01-C (Mean+Confirm), T01-D (Quantile Breakout), T01-E (Mean+Quantile Channel), T01-F (Z-Score Reversion), T01-G (KAMA/MAMA) |
| Est. Variants | ~364 |
| Status | TODO |

---

## HYP-RMQ-01: Price vs Rolling Mean — Window Sensitivity

**Tên:** Window nào optimal cho rolling mean trên VN30F1M?

**Null Hypothesis:** Window size không ảnh hưởng đến predictive power — tất cả window đều cho win rate ~50%.

**Alternative Hypothesis:** Window 14 cho Sharpe cao nhất trên 15-30min TF; window 8 cho 5min; window 30-50 cho 60min.

**Logic test:**
- Template T01-A với close làm price source
- So sánh windows: 5, 8, 14, 20, 30, 50, 100
- Đo riêng cho từng TF (5, 15, 30, 60 min)

**Metric:** Sharpe Ratio, Win Rate, Số tín hiệu/tháng
**Data Range:** 6 tháng VN30F1M
**Self-critique:** 🟡 Mean reversion bias — window càng ngắn càng nhiều tín hiệu nhưng nhiễu hơn. Cần check correlation giữa các window để tránh multicollinearity.

---

## HYP-RMQ-02: Quantile Threshold — Breakout vs Mean Reversion

**Tên:** Quantile nào phù hợp cho breakout và quantile nào cho mean reversion?

**Null Hypothesis:** Q80/Q20 không khác Q90/Q10 về risk-adjusted return.

**Alternative Hypothesis:** Q80/Q20 (rộng) cho nhiều tín hiệu hơn 40% với win rate giảm không đáng kể so với Q90/Q10. Q95/Q05 cho extreme moves với PF cao nhất.

**Logic test:**
- Template T01-D (Quantile Breakout) + T01-E (Channel)
- So sánh quantile pairs: (0.75/0.25), (0.80/0.20), (0.90/0.10), (0.95/0.05)
- Đo riêng breakout mode vs reversion mode

**Metric:** Win Rate, Profit Factor, Số tín hiệu/tháng, Avg Win / Avg Loss
**Data Range:** 6 tháng
**Self-critique:** 🔴 Quantile chặt (Q95) → rất ít tín hiệu, khó đánh giá statistical significance. Risk: data snooping với quá ít trade.

---

## HYP-RMQ-03: Confirmation Indicator — Which Adds Most Value?

**Tên:** RSI, ADX, Volume, MACD — confirmation nào hiệu quả nhất khi kết hợp với rolling mean?

**Null Hypothesis:** Thêm confirmation indicator không thay đổi win rate so với chỉ dùng rolling mean đơn thuần.

**Alternative Hypothesis:** ADX > 22 là filter mạnh nhất — giảm 50% tín hiệu nhiễu, tăng Sharpe 0.3-0.5. RSI > 50 tăng win rate 3-5% nhưng giảm số tín hiệu 20%.

**Logic test:**
- Template T01-C với mean window = 14
- So sánh từng confirmation:
  1. Không confirm (baseline)
  2. RSI > 50
  3. ADX > 22
  4. Volume > SMA(20)
  5. RSI + ADX
  6. RSI + ADX + Volume

**Metric:** Sharpe, Win Rate, Signal Reduction %, PF
**Data Range:** 6 tháng
**Self-critique:** 🟡 ADX đã được dùng universal trong inject_filters → cần test cả khi ADX filter đã active để tránh double-counting.

---

## HYP-RMQ-04: Adaptive MA (KAMA/MAMA) vs Fixed SMA

**Tên:** KAMA/MAMA adaptive có outperform SMA truyền thống trên VN30F1M không?

**Null Hypothesis:** Adaptive MA không khác biệt so với SMA cùng window.

**Alternative Hypothesis:** MAMA (MESA Adaptive) detect regime change nhanh hơn SMA 2-3 nến, cho PF cao hơn 10-15% trong thị trường VN retail-dominated (regime change thường xuyên).

**Logic test:**
- So sánh T01-G (KAMA/MAMA) vs T01-A (SMA) cùng effective window
- Đo lag (nến để crossover), win rate, PF

**Metric:** Signal Lag (nến), Win Rate, PF, Sharpe
**Data Range:** 6 tháng
**Self-critique:** 🔴 MAMA có thể unstable trong ranging market (fastlimit/slowlimit params nhạy). Cần test robustness với parameter perturbation.

---

## HYP-RMQ-05: Multi-Timeframe Alignment

**Tên:** Kết hợp tín hiệu từ nhiều window có cải thiện độ tin cậy không?

**Null Hypothesis:** Multi-window alignment (fast > mid > slow) không khác single window.

**Alternative Hypothesis:** Align 3 windows (fast > mid > slow) giảm 60% tín hiệu nhưng tăng win rate 8-12%.

**Logic test:**
- So sánh:
  1. Single: close > mean(14)
  2. Dual: close > mean(14) & mean(14) > mean(50)
  3. Triple: close > mean(14) & mean(14) > mean(50) & mean(50) > mean(200)

**Metric:** Win Rate, Signal Count, PF, Max DD
**Data Range:** 6 tháng
**Self-critique:** 🟡 Triple alignment rất an toàn nhưng gần như không có tín hiệu trên 5min. Nguy cơ overfitting khi chọn bộ 3 window cụ thể.

---

## HYP-RMQ-06: VN Market Regime — When Does This Thesis Fail?

**Tên:** Rolling Mean + Quantile hoạt động kém nhất khi nào?

**Null Hypothesis:** Thesis hoạt động đồng đều qua mọi điều kiện thị trường.

**Alternative Hypothesis:** Thesis hoạt động kém (Sharpe < 0.5) trong:
1. Ranging market (ADX < 20) — false signals from quantile whipsaw
2. High vol gap days — mean bị distorted
3. Lunch dead zone — volume quá thấp, quantile không có ý nghĩa

**Logic test:**
- Phân loại thị trường bằng ADX + ATR
- Đo Sharpe riêng cho từng regime:
  - Trending mạnh (ADX > 25)
  - Trending yếu (ADX 20-25)
  - Ranging (ADX < 20)
  - High vol (ATR > 1.5x SMA)
  - Low vol (ATR < 0.5x SMA)

**Metric:** Sharpe theo regime, Win Rate theo regime
**Data Range:** 12 tháng
**Self-critique:** 🔴 Nếu thesis chỉ hoạt động trong 1 regime → không robust. Cần có fallback mechanism khi regime chuyển.

---

## Hard Rules Compliance

| Rule | Check | Status |
|------|-------|--------|
| HM-1: Anomaly Filtering | Không trade nếu gap > 10% | ✅ ADX filter blocks anomaly zones |
| HM-2: Liquidity Validation | Spread < 0.2% on VN30F1M | ✅ Luôn true cho VN30F1M |
| HM-3: Continuity Check | Skip illiquid periods | ✅ Session gating (lunch, ATC) |
| RK-1: Risk per trade ≤ 2% | Position bounds [-1, +1] | ✅ |
| RK-2: Max DD 15-20% | Cooldown + ADX exit + trailing stop | ✅ |
| RK-3: Consecutive Loss ≤ 5 | recent_exit + cooldown_period | ✅ |
| RK-4: Max 3 concurrent positions | Single position per strategy | ✅ |

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

**Pass threshold:** ≥ 8.0/13pts (Sharpe + CAGR + Max DD must-pass)

## Backtest Scenarios

| Scenario | Expectation |
|----------|-------------|
| **Normal trending** (ADX > 25) | Quantile breakout hiệu quả, PF > 1.5 |
| **Ranging** (ADX < 20) | Hạn chế trade, nếu forced thì Mean Reversion mode (T01-F) |
| **High volatility** (gap > 2%) | Rolling mean bị distorted, cần vol filter |
| **Low liquidity** (holiday) | Quantile không có ý nghĩa, volume filter block |

## Test Plan

**Data split:** Train 70% → Test 30% (chronological)
**Validation steps:**
1. Test T01-A (basic) trên 4 TFs → chọn optimal window
2. Test T01-D (quantile) → chọn optimal quantile pair
3. Test T01-C (confirm) → chọn optimal confirmation
4. Full grid search trên train set
5. Best params → test set → scorecard

## Edge Cases & Failure Scenarios

| Edge Case | Impact | Mitigation |
|-----------|--------|------------|
| **Mean reversion trong strong trend** | False short khi close < mean nhưng trend bull | Kết hợp ADX > 22 + return_roll > 0 để confirm hướng |
| **Quantile breakout trong ranging** | Whipsaw liên tục, cháy tài khoản | ADX < 20 → không trade (hard rule) |
| **KAMA unstable** | MAMA fastlimit/slowlimit nhạy | Clamp params, test với perturbation ±20% |
| **Multi-window alignment quá strict** | 0 tín hiệu trong tháng | Fallback: dual alignment nếu triple cho 0 signal |
| **Expiry week OI distortion** | Quantile shifted | Adjust window hoặc skip expiry week |

*End of Hypothesis — Thesis 01*
