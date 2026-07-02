# Hypothesis — Thesis 05: Cross-Market Correlation

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 05 — Cross-Market Correlation |
| Core Ideas | Correlation (Pearson), Cointegration proxy (Spread Z-score), Beta, Relative Strength, DJI Spillover |
| Timeframes | 15, 30, 60 min |
| Templates | T05-A (Spread Z-score), T05-B (VN30 Confirm), T05-C (Basis Extreme), T05-D (DJI Consensus), T05-E (Rolling Correl Filter), T05-F (RS Ratio), T05-G (Correlation Breakdown) |
| Est. Variants | ~51 |
| Status | TODO |

---

## HYP-CRO-01: Spread Z-Score — Cointegration Proxy Effectiveness

**Tên:** Futures-VN30 spread z-score có predict được basis reversion không?

**Null Hypothesis:** Spread = close - beta * vn30_close là random walk — z-score không có mean reversion.

**Alternative Hypothesis:** Khi spread z-score > 2.5 (hoặc < -2.5), basis reversion về [-1, 1] xảy ra trong 5-10 nến với xác suất ≥ 65%. Hiệu quả nhất trên 30-60min TF.

**Logic test:**
- Template T05-A
- So sánh z-score entry thresholds: 1.5, 2.0, 2.5, 3.0
- Đo: thời gian reversion, % reversion thành công

**Metric:** Reversion Rate (%), Avg Time to Revert, PF
**Data Range:** 12 tháng VN30F1M + VN30 Index
**Self-critique:** 🔴 Cointegration proxy bằng beta có hạn chế: beta thay đổi theo thời gian. spread z-score không phải cointegration test thực sự. Có thể spread không mean-revert trong regime change.

---

## HYP-CRO-02: DJI Consensus — Global Spillover Impact

**Tên:** DJI direction có thực sự ảnh hưởng VN30F1M intraday không?

**Null Hypothesis:** DJI overnight change không có correlation với VN30F1M next-day direction.

**Alternative Hypothesis:** Khi DJI > 0 và VN30 Index > 0 và VN30F1M > 0 (3-way consensus), win rate cho long position ≥ 62%. Khi consensus negative, win rate short ≥ 60%.

**Logic test:**
- Template T05-D
- So sánh:
  1. Single: fut_roc > 0
  2. Dual: fut_roc > 0 & vn30_roc > 0
  3. Triple: fut_roc > 0 & vn30_roc > 0 & dji_roc > 0
- Đo win rate cho từng combination

**Metric:** Win Rate, PF, Signal Count
**Data Range:** 12 tháng
**Self-critique:** 🟡 DJI data có timezone khác — DJI close = VN morning. Cần dùng `self.op.previous(dji_close)` để align timeline. Không look-ahead.

---

## HYP-CRO-03: Rolling Correlation as Regime Filter

**Tên:** Khi nào correlation giữa VN30F1M và VN30 Index breakdown?

**Null Hypothesis:** Correlation luôn ổn định — không cần filter.

**Alternative Hypothesis:** Khi rolling correlation < 0.5, thị trường đang có disconnection (arbitrage, manipulation, data issue) — nên flat. Khi correlation > 0.7, trend signals đáng tin cậy hơn.

**Logic test:**
- Template T05-E
- So sánh: correlation filter thresholds: 0.3, 0.5, 0.7
- Đo win rate khi correl cao vs thấp

**Metric:** Sharpe với correl filter vs không filter
**Data Range:** 12 tháng
**Self-critique:** 🟡 Correlation window 20 có lag → correlation breakdown được phát hiện sau 5-10 nến. Cần thêm correlation velocity (correl - correl_lag) để detect sớm hơn.

---

## HYP-CRO-04: Relative Strength Rotation

**Tên:** Futures/VN30 relative strength có dẫn dắt price direction không?

**Null Hypothesis:** Tỷ lệ close/vn30_close là mean-reverting noise.

**Alternative Hypothesis:** Khi ratio > SMA(20) và ratio_roc > 0 và slope > 0, futures đang outperform → long futures. Khi ratio < SMA và ratio_roc < 0 → short.

**Logic test:**
- Template T05-F
- So sánh: ratio vs ratio_sma (level) vs ratio + roc + slope (trend)

**Metric:** Win Rate, PF, Signal Count
**Data Range:** 6 tháng
**Self-critique:** 🟡 Relative strength có thể kéo dài nhiều ngày (trend) — exit bằng mean reversion có thể quá sớm. Cần trailing stop cho trend exit.

---

## HYP-CRO-05: Basis Extreme + Volume Fading

**Tên:** Basis extreme kết hợp volume thấp có phải là reversal signal không?

**Null Hypothesis:** Basis extreme là random — không báo hiệu reversal.

**Alternative Hypothesis:** Khi basis > 2σ và matched volume < SMA(20) (volume fading), reversal xảy ra trong 3-5 nến với win rate ≥ 60%. Basis extreme + volume high lại là trend continuation.

**Logic test:**
- Template T05-C
- So sánh: basis extreme + low vol vs basis extreme + high vol
- Đo hướng price sau 5 nến

**Metric:** Reversal Rate, Continuation Rate, PF
**Data Range:** 12 tháng
**Self-critique:** 🔴 Basis extreme detection cần z-score window phù hợp. Nếu window quá ngắn, basis biến động hàng ngày sẽ tạo false extremes.

---

## Hard Rules Compliance

| Rule | Check | Status |
|------|-------|--------|
| HM-1: Anomaly | Spread > 5% là anomaly | ✅ basis_z > 5 → không trade |
| HM-2: Liquidity | VN30F1M + Index | ✅ |
| HM-3: Continuity | DJI data alignment | ⚠️ Cần previous() cho DJI |
| RK-1: Risk ≤ 2% | Position bounds | ✅ |
| RK-2: Max DD | ADX filter + spread exit | ✅ |
| RK-3: Consecutive Loss | Cooldown | ✅ |
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
| **Normal correlation** | DJI + VN30 consensus, PF > 1.5 |
| **Correlation breakdown** | Flat — không trade, bảo toàn vốn |
| **Basis extreme** | Reversion trade hiệu quả |
| **Global shock (DJI -3%)** | VN30 gap down, cần chờ 30min |

## Edge Cases & Failure Scenarios

| Edge Case | Impact | Mitigation |
|-----------|--------|------------|
| **DJI data timezone misalignment** | Look-ahead bias | Dùng `self.op.previous(dji_close, 1)` |
| **Beta thay đổi đột ngột** | Spread z-score sai | Rolling beta window 20, detect beta change |
| **Basis extreme kéo dài** | Short squeeze | Thêm trailing stop, không hodl |
| **Correlation = NaN (new data)** | Filter không hoạt động | Fallback: bỏ correl filter |
| **Expiry week basis manipulation** | False basis extreme | Adjust z-score threshold 1.5x |

*End of Hypothesis — Thesis 05*
