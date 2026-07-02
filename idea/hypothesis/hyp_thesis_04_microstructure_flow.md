# Hypothesis — Thesis 04: Microstructure Flow

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 04 — Microstructure Flow |
| Core Ideas | Balance of Power (OBI proxy), Chaikin Money Flow, OI+Volume Cascade (Margin Call), Whale Footprint, AD Oscillator Divergence, OBV, Volume Flow Imbalance |
| Timeframes | 5, 15, 30 min |
| Templates | T04-A (BOP+CMF), T04-B (MFI Reversal), T04-C (OI Cascade), T04-D (Whale Footprint), T04-E (AD Osc Divergence), T04-F (OBV Trend), T04-G (Volume Imbalance) |
| Est. Variants | ~71 |
| Status | TODO |

---

## HYP-MIC-01: BOP + CMF — Institutional Flow Detection

**Tên:** BOP và CMF có detect được institutional accumulation/distribution không?

**Null Hypothesis:** BOP > 0 và CMF > 0 không predictive cho price tăng — là random noise.

**Alternative Hypothesis:** Khi BOP > 0 và CMF > 0 đồng thời (buying pressure confirmed), xác suất price tăng trong 3 nến là ≥ 58%. Hiệu quả nhất trên 15-30min TF.

**Logic test:**
- Template T04-A
- So sánh:
  1. BOP > 0 (single)
  2. CMF > 0 (single)
  3. BOP > 0 & CMF > 0 (dual confirm)
  4. Dual confirm + ADX > 22

**Metric:** Win Rate (1-3 nến forward), PF, số tín hiệu/tháng
**Data Range:** 6 tháng VN30F1M
**Self-critique:** 🟡 BOP và CMF đều dùng price-volume → correlation cao giữa 2 indicators. Dual confirm có thể không thêm nhiều value so với single. Cần check correlation matrix.

---

## HYP-MIC-02: OI Cascade — Optimal Thresholds for VN30F1M

**Tên:** OI drop + volume spike threshold nào optimal cho margin call cascade detection?

**Null Hypothesis:** OI drop không có predictive power — cascade signal là random.

**Alternative Hypothesis:** OI drop > 1% + matched volume > 2x SMA + price drop > 0.5% cho short cascade với win rate ≥ 60%. Threshold cần điều chỉnh theo thời gian trong ngày (morning cascade mạnh hơn afternoon).

**Logic test:**
- Template T04-C
- Grid search OI drop: 0.5%, 1%, 2%, 3%
- Grid search vol spike: 1.5x, 2x, 3x
- Phân riêng morning (02:00-04:30 UTC) vs afternoon (06:00-07:30)

**Metric:** Win Rate, PF, Signal Count
**Data Range:** 12 tháng
**Self-critique:** 🔴 OI data daily (suffix _1d) → cùng giá trị cho mọi nến trong ngày. Trên 5-15min TF, OI drop signal chỉ thay đổi 1 lần/ngày → không phù hợp. Thesis này hiệu quả nhất trên 30-60min.

---

## HYP-MIC-03: Whale Footprint — Avg Trade Size Surge Reliability

**Tên:** Average trade size surge có báo hiệu smart money accumulation không?

**Null Hypothesis:** Avg trade size (matched_value / matched_volume) surge là random — không predictive.

**Alternative Hypothesis:** Khi avg_trade > SMA(20) + 2σ và price đang nén (range < 1%), breakout xảy ra trong 5 nến với xác suất ≥ 62%. Hiệu quả nhất 15-30min.

**Logic test:**
- Template T04-D
- Test sigma thresholds: 1.5, 2.0, 2.5
- Test compression windows: 5, 10, 14 nến
- Đo: breakout thành công trong 5 nến?

**Metric:** Breakout Success Rate, Avg Time to Breakout, PF
**Data Range:** 6 tháng
**Self-critique:** 🟡 avg_trade = matched_value / matched_volume có thể bị divide-by-zero nếu matched_volume = 0. Cần `self.op.isfinite()` guard. Whale signal hiếm (2-5 lần/tháng) → khó đạt statistical significance.

---

## HYP-MIC-04: MFI Reversal vs RSI Reversal

**Tên:** MFI (volume-weighted) có outperform RSI trong reversal detection không?

**Null Hypothesis:** MFI < 30 và RSI < 30 cho kết quả tương đương.

**Alternative Hypothesis:** MFI < 30 cho win rate cao hơn RSI < 30 5-8% vì MFI tính cả volume — phù hợp VN market retail-dominated (volume spike at extremes).

**Logic test:**
- Template T04-B vs meanrev_rsi template (legacy)
- Same threshold (30/70), same timeframe 15min
- Đo win rate cho long (oversold) và short (overbought) riêng biệt

**Metric:** Win Rate, PF, Avg Win / Avg Loss
**Data Range:** 6 tháng
**Self-critique:** 🟡 MFI cần high + low + close + volume — nếu volume data có vấn đề, MFI sai. Cần data quality check trước khi dùng.

---

## HYP-MIC-05: AD Oscillator Divergence — Detection Reliability

**Tên:** A/D Oscillator divergence có đáng tin cậy để detect reversal không?

**Null Hypothesis:** AD Osc divergence là random pattern — không predictive.

**Alternative Hypothesis:** Bullish divergence (price down, adosc up) + RSI < 40 cho long signal với win rate ≥ 55%. Hiệu quả nhất khi divergence kéo dài 3-5 nến.

**Logic test:**
- Template T04-E
- So sánh: divergence detection với các độ dài khác nhau (3, 5, 7 nến)
- Đo: time từ divergence signal đến actual reversal

**Metric:** Win Rate, Lead Time (nến), PF
**Data Range:** 6 tháng
**Self-critique:** 🔴 Divergence detection trên thị trường VN (retail 80%) có thể false positive do panic sell kéo dài. Cần thêm return_roll filter để tránh falling knife.

---

## Hard Rules Compliance

| Rule | Check | Status |
|------|-------|--------|
| HM-1: Anomaly | Volume spike check | ✅ vol_spike có threshold guard |
| HM-2: Liquidity | VN30F1M futures | ✅ |
| HM-3: Continuity | OI daily data có hạn chế | ⚠️ OI chỉ đổi 1 lần/ngày — không dùng cho 5min |
| RK-1: Risk ≤ 2% | Position bounds | ✅ |
| RK-2: Max DD | ADX filter + trailing stop | ✅ |
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
| **Cascade crash** | OI cascade short rất hiệu quả, PF > 2.0 |
| **Accumulation phase** | BOP+CMF detect sớm, whale footprint confirm |
| **Retail panic sell** | MFI oversold + AD divergence → reversal |
| **Low vol no flow** | Volume quá thấp → không có signal, flat |

## Edge Cases & Failure Scenarios

| Edge Case | Impact | Mitigation |
|-----------|--------|------------|
| **OI daily data trên 5min** | OI_drop chỉ đổi 1x/ngày | Không dùng OI cascade cho TF < 15min |
| **matched_volume = 0** | avg_trade divide by zero | `self.op.where(matched_vol > 0, avg_trade, 0)` |
| **BOP = 0 liên tục** | Không có buying/selling pressure | Flat — chờ BOP != 0 |
| **Expiry week OI jump** | False OI_drop signal | Adjust OI threshold 2x |
| **Whale signal quá hiếm** | Không đủ trade để đánh giá | Kết hợp với OI cascade để tăng signal count |

*End of Hypothesis — Thesis 04*
