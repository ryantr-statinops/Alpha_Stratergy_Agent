# Planning Alpha — Strategy #001: Mean + Quantile + RSI

**Target Market:** VnFuture (VN30F1M)  
**Khung thời gian:** 1D  
**Core Alpha:** I-001 (Combined Mean + Quantile), C-001 (Mean + RSI)  
**Status:** Planning

---

## 1. Strategy Overview

### Chiến lược

Kết hợp 3 tín hiệu để tạo entry/exit:

1. **Rolling Mean** (fast trend) — `rolling_mean(close, 14)`
2. **Rolling Quantile Upper** (breakout confirmation) — `rolling_quantile(close, 14, 0.8)`
3. **RSI** (momentum filter) — `rsi(close, 14)`

### Logic

```
LONG entry:
  - close > rolling_quantile(close, 14, 0.8)    (breakout upper channel)
  - close > rolling_mean(close, 14)              (trend filter: above mean)
  - RSI > 50                                     (momentum confirmation)

SHORT entry:
  - close < rolling_quantile(close, 14, 0.2)    (breakdown lower channel)
  - close < rolling_mean(close, 14)              (trend filter: below mean)
  - RSI < 50                                     (momentum confirmation)

EXIT:
  - close crosses below rolling_mean(close, 14)  (long exit)
  - close crosses above rolling_mean(close, 14)  (short exit)
  - Hoặc RSI reversed (RSI < 40 cho long, RSI > 60 cho short)
```

### Position Sizing

| Position | Exposure |
|----------|----------|
| Long | 1.0 (100%) |
| Short | -1.0 (100%) |
| Flat | 0.0 |

---

## 2. Alpha Components

### Alpha I-001: Combined Mean + Quantile

**Nguồn:** Family I trong alpha generation doc

```python
mean_14 = self.feat.rolling_mean(close, window=14)
upper = self.feat.rolling_quantile(close, 14, 0.8)
lower = self.feat.rolling_quantile(close, 14, 0.2)

# Breakout + Trend
long_signal = (close > upper) & (close > mean_14)
short_signal = (close < lower) & (close < mean_14)
```

**Kỳ vọng:**
- Win Rate: ≥ 50%
- Profit Factor: ≥ 1.2
- Số tín hiệu/tháng: 8-15

### Alpha C-001: Rolling Mean + RSI

**Nguồn:** Family C trong alpha generation doc

```python
mean_14 = self.feat.rolling_mean(close, window=14)
rsi = self.feat.rsi(close, timeperiod=14)

long_signal = (close > mean_14) & (rsi > 50)
short_signal = (close < mean_14) & (rsi < 50)
```

**Kỳ vọng:**
- Win Rate: ≥ 52%
- Profit Factor: ≥ 1.15
- Số tín hiệu/tháng: 10-20

---

## 3. Combined Strategy Logic

Gộp 2 alpha thành 1 strategy hoàn chỉnh:

```python
class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # === Data ===
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        # === Features ===
        mean_14 = self.feat.rolling_mean(close, window=14)
        upper_q = self.feat.rolling_quantile(close, 14, 0.8)
        lower_q = self.feat.rolling_quantile(close, 14, 0.2)
        rsi = self.feat.rsi(close, timeperiod=14)

        # === Entry Signals ===
        # Long: breakout upper quantile + above mean + RSI bullish
        long_setup = (
            (close > upper_q)
            & (close > mean_14)
            & (rsi > 50)
        )

        # Short: breakdown lower quantile + below mean + RSI bearish
        short_setup = (
            (close < lower_q)
            & (close < mean_14)
            & (rsi < 50)
        )

        # === Exit Signals ===
        exit_long = (close < mean_14) | (rsi < 40)
        exit_short = (close > mean_14) | (rsi > 60)
        exit_setup = exit_long | exit_short

        # === Position Sizing ===
        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1.0)
        self.set_positions(short_setup, position=-1.0)
```

---

## 4. Parameter Grid

| Parameter | Giá trị | Khoảng test |
|-----------|---------|-------------|
| Mean window | 14 | 10, 14, 20 |
| Quantile window | 14 | 10, 14, 20 |
| Quantile upper q | 0.80 | 0.75, 0.80, 0.85 |
| Quantile lower q | 0.20 | 0.15, 0.20, 0.25 |
| RSI period | 14 | 10, 14, 21 |
| RSI long threshold | 50 | 45, 50, 55 |
| RSI exit long | 40 | 35, 40, 45 |

---

## 5. Risk Management

| Rule | Giá trị |
|------|---------|
| Max position | 1.0 / -1.0 |
| Risk per trade | ≤ 2% tài khoản |
| Max concurrent positions | ≤ 3 |
| Max drawdown | 15% (cảnh báo), 20% (dừng) |
| Min liquidity | Spread < 0.5% |

---

## 6. Expected Metrics

| Metric | Target | Acceptable |
|--------|--------|------------|
| Win Rate | ≥ 52% | ≥ 48% |
| Profit Factor | ≥ 1.3 | ≥ 1.1 |
| Sharpe Ratio | ≥ 0.8 | ≥ 0.5 |
| Max DD | ≤ 12% | ≤ 15% |
| Consecutive Losses | ≤ 4 | ≤ 5 |
| Trades/month | 10-15 | 5-20 |

---

## 7. Next Steps

- [ ] Chuyển sang Hypothesis Loop (Bước 2b)
- [ ] Tạo hypothesis test cases trong `idea/hypothesis/`
- [ ] User Review (Bước 3)
- [ ] Coding (Bước 4)
- [ ] Output (Bước 5)

---

*End of Planning — Strategy #001*
