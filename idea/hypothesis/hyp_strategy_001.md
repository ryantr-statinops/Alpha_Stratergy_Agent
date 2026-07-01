# Hypothesis — Strategy #001: Mean + Quantile + RSI

## Thông tin chung

| Field | Value |
|-------|-------|
| Strategy ID | STR-001 |
| Alpha Components | I-001 (Mean+Quantile), C-001 (Mean+RSI) |
| Market | VnFuture (VN30F1M) |
| Timeframe | 1D |
| Status | TODO |

---

## Hypothesis HYP-STR-001-01: Quantile Breakout Confirmation

**Tên:** Giá break upper quantile kết hợp RSI có cải thiện win rate không?

**Null Hypothesis:** Close > quantile(0.8) không có giá trị dự đoán, win rate = 50% (random).

**Alternative Hypothesis:** Close > quantile(0.8) & close > mean(14) & RSI > 50 sẽ đạt win rate ≥ 52%.

**Logic test:**
- Backtest 3 tháng dữ liệu VN30F1M 1D
- So sánh 3 phiên bản:
  1. Baseline: chỉ dùng close > mean(14)
  2. V1: close > mean(14) + RSI > 50
  3. V2: close > mean(14) + RSI > 50 + close > quantile(0.8)

**Metric:**
- Win Rate
- Profit Factor
- Số tín hiệu

**Data Range:** 3 tháng gần nhất
**Status:** TODO

---

## Hypothesis HYP-STR-001-02: Quantile Channel Width Impact

**Tên:** Độ rộng quantile channel ảnh hưởng đến chất lượng tín hiệu thế nào?

**Null Hypothesis:** q=0.8/0.2 không khác biệt so với q=0.9/0.1 về win rate adjusted.

**Alternative Hypothesis:** q=0.8/0.2 cho số tín hiệu nhiều hơn 40% nhưng win rate chỉ giảm 5% so với q=0.9/0.1.

**Logic test:**
- Giữ nguyên mean(14) + RSI(14) > 50
- Thay đổi quantile threshold:
  1. q=0.75/0.25 (rộng)
  2. q=0.80/0.20 (tiêu chuẩn)
  3. q=0.90/0.10 (hẹp)
  4. q=0.95/0.05 (cực hẹp)

**Metric:**
- Win Rate theo từng q
- Số tín hiệu/tháng
- Profit Factor
- Avg Win / Avg Loss

**Data Range:** 3 tháng
**Status:** TODO

---

## Hypothesis HYP-STR-001-03: RSI Threshold Sensitivity

**Tên:** Ngưỡng RSI 50 có phải là optimal filter không?

**Null Hypothesis:** RSI > 50 không filter được nhiễu so với không dùng RSI.

**Alternative Hypothesis:** RSI > 60 cho win rate cao hơn 5% so với RSI > 50, dù số tín hiệu giảm 30%.

**Logic test:**
- Giữ mean(14) + quantile(0.8)
- Thay đổi RSI threshold:
  1. Không RSI (baseline)
  2. RSI > 40
  3. RSI > 50
  4. RSI > 60
  5. RSI > 70

**Metric:**
- Win Rate
- Profit Factor
- Số tín hiệu/tháng

**Data Range:** 3 tháng
**Status:** TODO

---

## Hypothesis HYP-STR-001-04: Exit Strategy Comparison

**Tên:** Exit bằng mean crossover vs RSI reversal — cái nào hiệu quả hơn?

**Null Hypothesis:** Exit bằng mean crossover và RSI reversal không khác biệt về profit.

**Alternative Hypothesis:** Kết hợp cả 2 exit (mean + RSI) cho profit factor cao hơn 15% so với chỉ dùng mean.

**Logic test:**
- Entry giống nhau (quantile + mean + RSI)
- So sánh 3 exit:
  1. Exit: close < mean(14)
  2. Exit: RSI < 40
  3. Exit: close < mean(14) | RSI < 40

**Metric:**
- Profit Factor
- Avg Win / Avg Loss
- Max Drawdown
- Số giao dịch

**Data Range:** 3 tháng
**Status:** TODO

---

## Hypothesis HYP-STR-001-05: Window Size Sensitivity

**Tên:** Window 14 có optimal cho VN30F1M daily không?

**Null Hypothesis:** Window size không ảnh hưởng đáng kể đến kết quả.

**Alternative Hypothesis:** Window 14 cho Sharpe ratio cao nhất trong các window {10, 14, 20, 30}.

**Logic test:**
- Giữ quantile(0.8) + RSI > 50
- Thay đổi window cho cả mean và quantile:
  1. Window = 10
  2. Window = 14
  3. Window = 20
  4. Window = 30

**Metric:**
- Sharpe Ratio
- Win Rate
- Max Drawdown

**Data Range:** 3 tháng
**Status:** TODO

---

## Hypothesis HYP-STR-001-06: Market Regime Performance

**Tên:** Strategy hoạt động thế nào trong các điều kiện thị trường khác nhau?

**Null Hypothesis:** Strategy không có sự khác biệt giữa trending và ranging market.

**Alternative Hypothesis:** Strategy hoạt động tốt hơn trong trending market (win rate ≥ 55%) và kém hơn trong ranging market (win rate ≤ 45%).

**Logic test:**
- Phân loại thị trường bằng ADX:
  - Trending: ADX(14) > 25
  - Ranging: ADX(14) < 20
- Đo metric riêng cho từng regime

**Metric:**
- Win Rate (trending)
- Win Rate (ranging)
- Profit Factor theo regime
- Số tín hiệu theo regime

**Data Range:** 6 tháng
**Status:** TODO

---

## Backtest Scenarios

| Scenario | Điều kiện | Kỳ vọng |
|----------|-----------|----------|
| Normal | Trending, vol trung bình | Win Rate ≥ 52% |
| Choppy | Ranging, vol thấp | Win Rate ≥ 45%, DD ≤ 10% |
| High Vol | Spike, gap | Slippage test, SL hoạt động |
| Low Liq | Spread rộng | Hạn chế trade |

---

## Scorecard Target

| Metric | Target | Pass? |
|--------|--------|-------|
| Win Rate | ≥ 52% | □ |
| Profit Factor | ≥ 1.3 | □ |
| Sharpe Ratio | ≥ 0.8 | □ |
| Max Drawdown | ≤ 12% | □ |
| Consecutive Losses | ≤ 4 | □ |
| Avg Win / Avg Loss | ≥ 1.3 | □ |

---

*End of Hypothesis — Strategy #001*
