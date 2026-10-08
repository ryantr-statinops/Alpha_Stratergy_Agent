# Hypothesis — Thesis 12: Kalman Filter Regime Switching

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 12 — Kalman Filter Regime Switching |
| Core Ideas | Kalman proxy via adaptive SMA, residual z-score, regime classification by deviation from state, directional exit per position |
| Timeframes | 15, 30, 60 min |
| Templates | T12-A (KF Dip/Rally), T12-B (KF Mean Reversion), T12-C (KF + ADX Confirmed), T12-D (KF + Z Combo) |
| Est. Variants | ~9 |
| Status | TODO |

---

## HYP-KAL-01: KF Dip/Rally — Trend Following via Kalman State

**Tên:** Giá lệch khỏi Kalman state trong xu hướng có quay về không?

**Null Hypothesis:** `kf_z` là random walk — overshoot trong trend không có mean reversion.

**Alternative Hypothesis:** Khi `kf_trend_up & kf_z < -1.5` (bull trend, giá tạm rớt dưới state), giá hồi về state trong 5-10 nến với win rate ≥ 60%. Tương tự cho bear.

**Logic test:**
- Template T12-A
- Entry: `kf_trend_up & kf_z < -kf_z_entry & adx > adx_entry` (Long)
- Exit: `crossed_below(kf_z, -0.2) | adx < adx_exit | atr_stop_long`
- So sánh kf_z_entry thresholds: 0.5, 1.0, 1.5, 2.0

**Metric:** Win Rate, Profit Factor, Avg Hold Time
**Data Range:** 12 tháng VN30F1M
**Self-critique:** 🟡 Kalman proxy (SMA 10) có lag — overshoot detection chậm hơn Kalman thật. Cần đo latency impact.

---

## HYP-KAL-02: KF Mean Reversion — Overshoot trong Sideways

**Tên:** Overshoot khỏi Kalman band trong sideways có đảo chiều?

**Null hypothesis:** Khi `kf_sideways`, overshoot > 2 sigma là random.

**Alternative hypothesis:** Khi `kf_sideways & kf_z < -2.0`, giá quay về state trong 3-5 nến với win rate ≥ 65%.

**Logic test:**
- Template T12-B (MR variant)
- So sánh mr_entry thresholds: 1.5, 2.0, 2.5, 3.0
- Đo thời gian revert, % revert thành công

**Metric:** Reversion Rate, Avg Time to Revert, PF
**Data Range:** 12 tháng
**Self-critique:** 🔴 SMA(10) proxy kém nhạy cho overshoot ngắn. Overshoot > 2.5 sigma mới đáng tin.

---

## HYP-KAL-03: ADX Confirmation Filter cho KF Signals

**Tên:** ADX > 20 có tăng chất lượng KF entries?

**Hypothesis:** KF entries (cả trend và MR) không cần ADX filter vì KF đã tự xác định regime.

**Logic test:**
- T12-C vs T12-A (cùng entry threshold)
- Có ADX filter vs không ADX filter

**Metric:** Sharpe, Win Rate, Signal Count
**Data Range:** 12 tháng
**Self-critique:** 🟡 Nếu KF state và ADX cùng correlation → redundant filter.

---

## HYP-KAL-04: Residual Z-Score as Entry Booster

**Tên:** `kf_z` kết hợp residual z-score có tăng chất lượng?

**Hypothesis:** Long khi cả `kf_z < -1.5` và `residual_z < -1.0` mạnh hơn chỉ dùng `kf_z`.

**Logic test:**
- T12-D vs T12-A
- So sánh combo vs single

**Metric:** Sharpe, Win Rate, Risk per Trade
**Data Range:** 12 tháng
**Self-critique:** 🟡 Combo càng nhiều điều kiện → signal count càng ít.

---

## Hard Rules Compliance

| Rule | Check | Status |
|------|-------|--------|
| HM-1: Anomaly | kf_z > 5 → không trade | ✅ |
| HM-2: Liquidity | VN30F1M | ✅ |
| HM-3: Continuity | SMA(10) proxy — no lookahead | ✅ |
| RK-1: Risk ≤ 2% | Position bounds | ✅ |
| RK-2: Max DD | ATR stop + adx exit | ✅ |
| RK-3: Consecutive Loss | Cooldown | ✅ |
| RK-4: Max 3 concurrent | Single position | ✅ |
| 5.6: Directional exit | Long exit `crossed_below(kf_z, -0.2)` (downward event), Short exit `crossed_above(kf_z, +0.2)` (upward event) | ✅ |
| 5.8: Entry không block | Entry không nhân chéo ATR stop | ✅ |
| 5.10: Priority exit | `set_positions(exit_long, 0)` → `set_positions(exit_short, 0)` → `set_positions(long, 1)` → `set_positions(short, -1)` | ✅ |

## Scorecard Targets

| Metric | Weight | Target | Must-pass |
|--------|:------:|--------|:---------:|
| Sharpe Ratio | High | ≥ 1.5 | ✅ |
| CAGR | High | > 20% | ✅ |
| Max Drawdown | High | > -25% | ✅ |
| Sortino Ratio | Medium | ≥ 1.5 | |
| Calmar Ratio | Medium | ≥ 0.9 | |
| Profit Factor | Medium | ≥ 1.5 | |
| VaR 95% | Medium | ≥ -5% | |
| CVaR 95% | Low | ≥ -6% | |
| Ulcer Index | Low | ≤ 12 | |
| Cost | Low | ≤ 0.5% | |

## Backtest Scenarios

| Scenario | Expectation |
|----------|-------------|
| **Strong uptrend** | Dip_long bắt được pullback, exit khi trend yếu |
| **Sideways range** | MR vào overshoot, exit khi revert |
| **Volatile breakdown** | KF state lag nhiều → flat, tránh đánh |
| **Expiry week** | Tăng kf_z_entry threshold để tránh noise |

## Edge Cases & Failure Scenarios

| Edge Case | Impact | Mitigation |
|-----------|--------|------------|
| **SMA(10) proxy lag trong gap** | State sai lệch vài nến | Thêm kalman_state clip ±5% close |
| **KF residual std = 0 (flat market)** | kf_z infinite | `fillna(std, 1e-5)` |
| **Regime biên (kf_dev ≈ 0.02)** | Trend/Sideways nhấp nháy | Histogram buffer 5 nến |
| **Expiry week basis distorition** | KF state lệch do giá expiry | Tăng adx_entry threshold |

*End of Hypothesis — Thesis 12*