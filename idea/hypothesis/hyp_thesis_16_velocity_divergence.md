# Hypothesis — Thesis 16: Price-Volume Velocity Divergence

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 16 — Price-Volume Velocity Divergence |
| Core Idea | Compare price velocity (self.feat.roc) vs volume velocity (self.feat.volume_z). If price accelerates but volume decelerates = fake effort. If volume accelerates but price stagnates = accumulation. |
| Data Fields | `pv_close`, `pv_high`, `pv_low`, `pv_volume` |
| Timeframes | 15, 30, 60 min |
| Templates | T16-A (Velocity Divergence Breakout) |
| Est. Variants | ~3 (3 TFs x 1 params) |
| Status | TODO |

---

## HYP-VEL-01: Price-Volume Velocity Divergence

**Tên:** So sánh ROC (giá) và volume_z. Khi giá tăng tốc nhưng volume giảm tốc → fake breakout. Khi volume tăng tốc nhưng giá chưa phản ứng → accumulation sắp nổ.

**Null Hypothesis:** Price-volume velocity divergence không predictive — ROC và volume_z không tương quan đủ để tạo tín hiệu trade.

**Alternative Hypothesis:** Khi volume_z > 1.5 (volume tăng tốc) nhưng price_z < 0.5 (giá chưa kịp phản ứng), xác suất price breakout trong 3 nến ≥ 60%.

**Logic test:**
- Template T16-A
- Long: `volume_z > 1.5 & price_z < 0.5 & close > bb_mid`
- Short: `volume_z < -1.5 & price_z > -0.5 & close < bb_mid`
- Exit: ADX fade + ATR stop + trailing

**Metric:** Win Rate, PF, Sharpe
**Data Range:** 12 tháng VN30F1M
**Self-critique:** volume_z dùng rolling z-score (window=14) — nếu volume tăng đột biến liên tục, z-score có thể bão hòa. Cần thêm reset mechanism.

---

## Hard Rules Compliance

| Rule | Check | Status |
|------|-------|--------|
| HM-1: Anomaly | Gap filter | ✅ |
| HM-2: Liquidity | VN30F1M futures | ✅ |
| HM-3: Continuity | Daily data continuity | ✅ |
| RK-1: Risk ≤ 2% | Position bounds | ✅ |
| RK-2: Max DD | ADX + ATR stop | ✅ |
| RK-3: Consecutive Loss | Cooldown | ✅ |
| RK-4: Max 3 concurrent | Single position | ✅ |

## Scorecard Targets

| Metric | Weight | Target | Must-pass |
|--------|:----:|:------:|:---------:|
| Sharpe Ratio | High | ≥ 1.2 | ✅ |
| CAGR | High | ≥ 20% | ✅ |
| Max Drawdown | High | > -25% | ✅ |
| Sortino Ratio | Medium | ≥ 1.5 | |
| Calmar Ratio | Medium | ≥ 1.0 | |
| Profit Factor | Medium | ≥ 1.5 | |
| VaR 95% | Medium | ≥ -5% | |
| CVaR 95% | Low | ≥ -6% | |
| Ulcer Index | Low | ≤ 12 | |
| Cost | Low | ≤ 1% | |

## Backtest Scenarios

| Scenario | Expectation |
|----------|-----------|
| Volume surge leading price | High win rate — accumulation detected early |
| Price surge on declining volume | Low win rate — fake breakout, exit fast |
| Choppy low vol | Flat — no velocity divergence signal |

## Next Steps

- [ ] Code T16-A template trong generate_strategies.py
- [ ] Gen + validate
- [ ] Upload lên XNOQuant