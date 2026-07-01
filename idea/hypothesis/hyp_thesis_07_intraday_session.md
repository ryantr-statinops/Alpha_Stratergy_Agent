# Hypothesis — Thesis 07: Intraday Session

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 07 — Intraday Session |
| Timeframes | 5, 15 min |
| Core Indicators | Open drive, lunch revert, close squeeze, gap fill |
| Templates | intraday_open_drive, intraday_revert, intraday_close, intraday_gapfill |
| Status | TODO |

---

## HYP-SES-01: Session Window Selection

**Tên:** Cửa sổ giao dịch nào optimal cho từng session strategy?

**Null Hypothesis:** Window size không ảnh hưởng.

**Alternative Hypothesis:** Short window (RSI=7) cho open drive, medium (RSI=14) cho close squeeze.

**Logic test:**
- Compare 6 RSI window variants cho từng template
- Đo Sharpe, Win Rate riêng cho từng variant

**Metric:** Sharpe, Win Rate, Signal Count

**Data Range:** 6 tháng, 5min và 15min

**Status:** TODO

---

## HYP-SES-02: Open Drive Threshold Sensitivity

**Tên:** Ngưỡng open_range nào optimal cho open drive strategy?

**Null Hypothesis:** open_range > 0.3% là optimal.

**Alternative Hypothesis:** open_range > 0.5% cho Win Rate cao hơn 8%, open_range > 0.2% cho nhiều tín hiệu hơn 60%.

**Logic test:**
- Template: `intraday_open_drive` — thay đổi open_range threshold
- So sánh 0.2%, 0.3%, 0.5%, 0.7%

**Metric:** Win Rate, Signal Count, Profit Factor

**Data Range:** 6 tháng

**Status:** TODO

---

## HYP-SES-03: position_close_ranges Impact

**Tên:** Thêm position_close_ranges có giảm drawdown không?

**Null Hypothesis:** position_close_ranges không ảnh hưởng.

**Alternative Hypothesis:** position_close_ranges ["04:20-04:30", "07:30-07:45"] giảm 20% Max DD.

**Logic test:**
- Baseline: intraday session strategy không có close range
- V1: + position_close_ranges (lunch + end forced flat)
- Đo Max DD, Sharpe

**Metric:** Max DD, Sharpe, Win Rate

**Data Range:** 6 tháng

**Status:** TODO

---

## HYP-SES-04: Gap Fill Success Rate

**Tên:** Gap fill strategy có thành công trong thị trường VN30F1M không?

**Null Hypothesis:** Gap không được fill trong intraday, strategy không có alpha.

**Alternative Hypothesis:** Gap fill thành công ≥ 55% intraday, đặc biệt gap < 0.5%.

**Logic test:**
- Template: `intraday_gapfill` — measure gap fill rate
- Phân loại gap size: < 0.3%, 0.3-0.5%, > 0.5%

**Metric:** Gap Fill Rate, Win Rate, Profit Factor

**Data Range:** 6 tháng

**Status:** TODO

---

## Scorecard Target (Intraday Session Thesis)

| Metric | Target | Pass? |
|--------|--------|-------|
| Sharpe Ratio | ≥ 1.0 | □ |
| Win Rate | ≥ 55% | □ |
| Profit Factor | ≥ 1.5 | □ |
| Max Drawdown | ≤ -20% | □ |
| Gap Fill Rate | ≥ 55% | □ |
| Open Drive Success | ≥ 58% | □ |
