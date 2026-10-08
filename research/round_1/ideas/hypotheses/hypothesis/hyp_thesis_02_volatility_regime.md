# Hypothesis — Thesis 02: Volatility Regime

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 02 — Volatility Regime |
| Core Ideas | Volatility Clustering (GARCH proxy), HMM proxy (3-state regime), Adaptive KAMA |
| Timeframes | 5, 15, 30, 60 min |
| Templates | T02-A (Vol Breakout), T02-B (Low Vol MeanRev), T02-C (3-State HMM), T02-D (ATR Trailing), T02-E (NATR Switch), T02-F (KAMA Trend) |
| Est. Variants | ~84 |
| Status | TODO |

---

## HYP-VOL-01: Volatility Regime Detection — ATR vs Rolling Std

**Tên:** ATR hay rolling_std là vol regime detector tốt hơn cho VN30F1M?

**Null Hypothesis:** ATR và rolling_std cho kết quả tương đương — không khác biệt đáng kể.

**Alternative Hypothesis:** ATR robust hơn rolling_std trong gap days (gap tạo rolling_std jump giả). NATR (%) cho cross-TF comparability tốt nhất.

**Logic test:**
- Template T02-A (Vol Breakout) với 3 vol metrics:
  1. `self.feat.atr(high, low, close, timeperiod=14)`
  2. `self.feat.rolling_std(close, window=14)`
  3. `self.feat.natr(high, low, close, timeperiod=14)`
- So sánh số lần false expansion signal (expansion nhưng không có breakout)

**Metric:** Sharpe, False Signal Rate, Signal-to-Noise Ratio
**Data Range:** 6 tháng VN30F1M
**Self-critique:** 🟡 ATR bị ảnh hưởng bởi price level — cùng ATR 100 points ở price 1000 vs 1500 có ý nghĩa khác nhau. NATR giải quyết vấn đề này.

---

## HYP-VOL-02: Volume Expansion Multiplier Threshold

**Tên:** Vol ratio threshold nào optimal để detect volatility expansion?

**Null Hypothesis:** Mọi threshold đều cho kết quả tương tự.

**Alternative Hypothesis:** Threshold 1.5x SMA(ATR) cho Sharpe cao nhất — balance giữa số tín hiệu và độ tin cậy. Threshold > 2.0x quá ít tín hiệu.

**Logic test:**
- Template T02-A
- So sánh expansion multipliers: 1.3x, 1.5x, 2.0x, 2.5x
- Đo số tín hiệu/tháng, Sharpe, Win Rate

**Metric:** Sharpe, Win Rate, Tín hiệu/tháng
**Data Range:** 6 tháng
**Self-critique:** 🟡 Threshold optimization dễ overfit. Cần walk-forward validation để confirm.

---

## HYP-VOL-03: 3-State HMM Proxy vs Simple ADX Filter

**Tên:** Regime classification 3-state (trend/range/vol) có outperform single ADX filter không?

**Null Hypothesis:** 3-state regime không khác binary ADX filter (ADX > 22 = trade, else flat).

**Alternative Hypothesis:** 3-state regime cho phép trade mean reversion trong low vol range, tăng CAGR 15-20% so với chỉ trade trend.

**Logic test:**
- So sánh T02-C (3-state) vs T02-A (single regime)
- Đo CAGR, Sharpe, số tháng dương

**Metric:** CAGR, Sharpe, % tháng dương, Max DD
**Data Range:** 12 tháng
**Self-critique:** 🔴 3-state classification tăng complexity gấp 3. Rủi ro: regime misclassification → trade sai hướng. Cần regime persistence check (regime phải kéo dài ≥ 3 nến trước khi trade).

---

## HYP-VOL-04: Volatility Regime Failure Analysis

**Tên:** Khi nào Volatility Regime thesis fail nặng nhất?

**Null Hypothesis:** Thesis fail đồng đều qua mọi điều kiện.

**Alternative Hypothesis:** Thesis fail nhất khi:
1. Regime change đột ngột (trend → range trong 1 nến): không kịp thích ứng
2. Vol spike do news event: rolling_std jump không báo trước
3. Low vol kéo dài (nén quá lâu): false compression signals

**Logic test:**
- Phân tích các giai đoạn DD > 10%
- Xác định regime ngay trước DD period
- Thống kê nguyên nhân fail

**Metric:** DD Period Frequency by Regime, Recovery Time
**Data Range:** 12 tháng
**Self-critique:** 🔴 Đây là thesis rủi ro nhất vì regime detection luôn lag 1-3 nến. Cần thêm leading indicator (volume slope, basis change) để giảm lag.

---

## Hard Rules Compliance

| Rule | Check | Status |
|------|-------|--------|
| HM-1: Anomaly Filtering | Gap > 10% blocked by vol filter | ✅ |
| HM-2: Liquidity | VN30F1M spread always合格 | ✅ |
| HM-3: Continuity | Session gating handles gaps | ✅ |
| RK-1: Risk ≤ 2% | Position bounds [-1, +1] | ✅ |
| RK-2: Max DD 15-20% | Regime-based position sizing | ✅ |
| RK-3: Consecutive Loss ≤ 5 | Cooldown period | ✅ |
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
| **Normal trending** | Vol breakout hoạt động tốt, PF > 1.5 |
| **Ranging low vol** | Chuyển sang mean reversion mode |
| **Vol spike crash** | ATR tăng đột biến → giảm size 50% |
| **Low vol kéo dài** | False compression signals risk |

## Edge Cases & Failure Scenarios

| Edge Case | Impact | Mitigation |
|-----------|--------|------------|
| **Regime change trong 1 nến** | Trade sai hướng 1-2 nến | Chỉ trade khi regime kéo dài ≥ 3 nến |
| **Vol spike do news** | rolling_std jump không báo trước | Thêm news filter hoặc position_close_ranges |
| **ATR = 0 (do data error)** | Division by zero | `self.op.isfinite(atr)` guard |
| **Low vol quá lâu** | Mean reversion stacked trades | Cooldown giữa các mean reversion trades |
| **Expiry week vol bất thường** | False signals | Adjust ATR mult 1.5x trong expiry week |

*End of Hypothesis — Thesis 02*
