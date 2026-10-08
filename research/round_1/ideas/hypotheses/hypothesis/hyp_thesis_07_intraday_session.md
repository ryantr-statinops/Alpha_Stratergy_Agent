# Hypothesis — Thesis 07: Intraday Session Microstructure

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 07 — Intraday Session |
| Timeframes | 5, 15 min |
| Core Indicators | SMA, ROC, volume, RSI, BBands, rolling_vwap, ADX |
| Templates | T07-A Open Drive, T07-B Lunch Revert, T07-C Close Squeeze, T07-D Pre-ATC Rev, T07-E VWAP Bounce |
| Total Variants | 64 |
| Status | READY FOR GENERATION |

---

## HYP-SES-01: Session Window Optimality

**Tên:** Cửa sổ session nào optimal cho từng template?

**Null Hypothesis:** Session windows như thiết kế là optimal.

**Alternative Hypothesis:** Mở rộng/cắt ngắn window 15 phút có thể cải thiện Sharpe 10-15%.

**Logic test:**
- So sánh 3 phiên bản window cho mỗi template
- Đo Sharpe, Win Rate riêng

**Metric:** Sharpe, Win Rate, Signal Count

**Status:** TODO

---

## HYP-SES-02: Volume Threshold Sensitivity

**Tên:** Volume multiplier nào optimal cho T07-C Close Squeeze?

**Null Hypothesis:** vol_mult = 1.5 là optimal.

**Alternative Hypothesis:** vol_mult = 2.0 cho Win Rate cao hơn 12%, vol_mult = 1.2 cho nhiều tín hiệu hơn 40%.

**Logic test:**
- Template T07-C — thay đổi vol_mult [1.2, 1.5, 2.0, 3.0]
- Đo Sharpe, Win Rate, Signal Count

**Metric:** Sharpe, Win Rate, Signal Count

**Status:** TODO

---

## HYP-SES-03: BBands Width Impact on T07-D

**Tên:** BBands multiplier nào optimal cho Pre-ATC mean reversion?

**Null Hypothesis:** BBands 2.0 là optimal.

**Alternative Hypothesis:** BBands 2.5 cho ít tín hiệu hơn 40% nhưng Win Rate cao hơn 15%.

**Logic test:**
- Template T07-D — thay đổi bb_mult [1.5, 2.0, 2.5, 3.0]
- Đo Sharpe, Win Rate

**Metric:** Sharpe, Win Rate, Max DD

**Status:** TODO

---

## HYP-SES-04: VWAP Z-score Entry

**Tên:** Z-score nào optimal cho VWAP bounce?

**Null Hypothesis:** z = 1.0% là optimal.

**Alternative Hypothesis:** z = 1.5% cho Sharpe cao hơn 20% (tránh noise), z = 2.0% cho Win Rate > 65%.

**Logic test:**
- Template T07-E — thay đổi z_entry [0.5, 1.0, 1.5, 2.0, 3.0]
- Đo Sharpe, Win Rate

**Metric:** Sharpe, Win Rate, Signal Count

**Status:** TODO

---

## Acceptance Criteria

| Metric | Target | Must-pass |
|--------|:------:|:---------:|
| Sharpe Ratio | ≥ 2.0 | ✅ |
| CAGR | ≥ 20% | ✅ |
| Max Drawdown | ≥ -20% | ✅ |
| Sortino Ratio | ≥ 1.5 | |
| Calmar Ratio | ≥ 1.1 | |
| Profit Factor | ≥ 1.3 | |
| Win Rate | ≥ 55% | |
| Signal Count | ≥ 30/năm | |
