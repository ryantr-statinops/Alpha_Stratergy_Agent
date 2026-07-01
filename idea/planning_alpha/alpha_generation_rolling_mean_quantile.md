# Alpha Generation: Rolling Mean & Rolling Quantile (~500 Alphas)

**Target Market:** VnFuture (VN30F1M)  
**Core Concepts:** Rolling Mean, Rolling Quantile, Combination Indicators  
**Generated:** 2026-07-01  

---

## 1. Tổng quan phương pháp

Tất cả alpha đều sử dụng **3 building blocks**:

| Block | Cú pháp | Mô tả |
|-------|---------|-------|
| Rolling Mean | `self.feat.rolling_mean(s1, window=N)` | Trung bình động |
| Rolling Quantile | `self.feat.rolling_quantile(s1, window=N, q=X)` | Phân vị động |
| Giá đầu vào | `pv_close`, `pv_high`, `pv_low`, `pv_volume`, `fut_*_vn30f1m_1d` | Dữ liệu thị trường |

**Cấu trúc alpha chuẩn:**
```python
# Entry
entry_long = (price > rolling_mean) & [confirmation]
entry_short = (price < rolling_mean) & [confirmation]

# Exit
exit_long = (price < rolling_mean * 0.98) | [stop_condition]
exit_short = (price > rolling_mean * 1.02) | [stop_condition]

self.set_positions(exit_long | exit_short, position=0)
self.set_positions(entry_long, position=1)
self.set_positions(entry_short, position=-1)
```

---

## 2. Price Source Mapping

| ID | Price Source | Công thức |
|----|-------------|-----------|
| P01 | `close` | `self.data.pv_close` |
| P02 | `typical_price` | `self.feat.typprice(high, low, close)` |
| P03 | `weighted_close` | `self.feat.wclprice(high, low, close)` |
| P04 | `median_price` | `self.feat.medprice(high, low)` |
| P05 | `hlc3` | `self.feat.hlc3(high, low, close)` |
| P06 | `ohlc4` | `self.feat.ohlc4(open, high, low, close)` |
| P07 | `high` | `self.data.pv_high` |
| P08 | `low` | `self.data.pv_low` |
| P09 | `volume` | `self.data.pv_volume` |
| P10 | `vwap` | `self.feat.vwap(high, low, close, volume)` |

---

## 3. Rolling Window Mapping

| ID | Window | Ứng dụng |
|----|--------|----------|
| W01 | 3 | Siêu ngắn (scalping) |
| W02 | 5 | Ngắn |
| W03 | 8 | Fibonacci |
| W04 | 10 | |
| W05 | 14 | Tiêu chuẩn (RSI, ATR) |
| W06 | 20 | Tháng giao dịch |
| W07 | 30 | |
| W08 | 50 | |
| W09 | 100 | |
| W10 | 200 | Dài hạn |

---

## 4. Quantile Values

| ID | q | Ý nghĩa |
|----|---|---------|
| Q01 | 0.05 | Extreme low |
| Q02 | 0.10 | Oversold cục bộ |
| Q03 | 0.20 | Lower channel |
| Q04 | 0.25 | Lower quartile |
| Q05 | 0.50 | Median |
| Q06 | 0.75 | Upper quartile |
| Q07 | 0.80 | Upper channel |
| Q08 | 0.90 | Overbought cục bộ |
| Q09 | 0.95 | Extreme high |

---

## 5. Confirmation Indicators

| ID | Indicator | Cú pháp | Điều kiện Long | Điều kiện Short |
|----|-----------|---------|----------------|-----------------|
| C01 | RSI | `self.feat.rsi(close, 14)` | RSI > 50 | RSI < 50 |
| C02 | ADX | `self.feat.adx(high, low, close, 14)` | ADX > 20 | ADX > 20 |
| C03 | MACD | `self.feat.macd(close, 12, 26, 9)` | MACD > Signal | MACD < Signal |
| C04 | Volume SMA | `self.feat.sma(volume, 20)` | Vol > Vol_SMA | Vol > Vol_SMA |
| C05 | ROC | `self.feat.roc(close, 10)` | ROC > 0 | ROC < 0 |
| C06 | CMO | `self.feat.cmo(close, 14)` | CMO > 0 | CMO < 0 |
| C07 | ATR | `self.feat.atr(high, low, close, 14)` | ATR > ATR_SMA | ATR > ATR_SMA |
| C08 | Volume Z | `self.feat.volume_z(volume, 30)` | Vol_Z > 0 | Vol_Z > 0 |
| C09 | MFI | `self.feat.mfi(high, low, close, volume, 14)` | MFI > 50 | MFI < 50 |
| C10 | Plus_DI | `self.feat.plus_di(high, low, close, 14)` | +DI > -DI | +DI < -DI |

---

# FAMILY A: Rolling Mean Price Level (200 alphas)

Mỗi alpha: **PriceSource so sánh với Rolling Mean của chính nó**

## Công thức chung

```python
mean = self.feat.rolling_mean(price_source, window=N)

entry_long = price_source > mean          # Giá trên mean → Long
entry_short = price_source < mean         # Giá dưới mean → Short
exit = self.op.crossed_below(price_source, mean)  # hoặc crossed_above
```

## Parameter Grid (200 combinations)

| Alpha ID | Price | Window | Direction |
|----------|-------|--------|-----------|
| A-001 | P01 | W01 | LONG |
| A-002 | P01 | W01 | SHORT |
| A-003 | P01 | W02 | LONG |
| A-004 | P01 | W02 | SHORT |
| A-005 | P01 | W03 | LONG |
| A-006 | P01 | W03 | SHORT |
| A-007 | P01 | W04 | LONG |
| A-008 | P01 | W04 | SHORT |
| A-009 | P01 | W05 | LONG |
| A-010 | P01 | W05 | SHORT |
| A-011 | P01 | W06 | LONG |
| A-012 | P01 | W06 | SHORT |
| A-013 | P01 | W07 | LONG |
| A-014 | P01 | W07 | SHORT |
| A-015 | P01 | W08 | LONG |
| A-016 | P01 | W08 | SHORT |
| A-017 | P01 | W09 | LONG |
| A-018 | P01 | W09 | SHORT |
| A-019 | P01 | W10 | LONG |
| A-020 | P01 | W10 | SHORT |
| A-021..A-040 | P02 | W01-W10 | LONG/SHORT |
| A-041..A-060 | P03 | W01-W10 | LONG/SHORT |
| A-061..A-080 | P04 | W01-W10 | LONG/SHORT |
| A-081..A-100 | P05 | W01-W10 | LONG/SHORT |
| A-101..A-120 | P06 | W01-W10 | LONG/SHORT |
| A-121..A-140 | P07 | W01-W10 | LONG/SHORT |
| A-141..A-160 | P08 | W01-W10 | LONG/SHORT |
| A-161..A-180 | P09 | W01-W10 | LONG/SHORT |
| A-181..A-200 | P10 | W01-W10 | LONG/SHORT |

### Chi tiết mở rộng (A-001..A-020)

```
A-001: close > rolling_mean(close, 3) → LONG
A-002: close < rolling_mean(close, 3) → SHORT
A-003: close > rolling_mean(close, 5) → LONG
A-004: close < rolling_mean(close, 5) → SHORT
A-005: close > rolling_mean(close, 8) → LONG
A-006: close < rolling_mean(close, 8) → SHORT
A-007: close > rolling_mean(close, 10) → LONG
A-008: close < rolling_mean(close, 10) → SHORT
A-009: close > rolling_mean(close, 14) → LONG
A-010: close < rolling_mean(close, 14) → SHORT
A-011: close > rolling_mean(close, 20) → LONG
A-012: close < rolling_mean(close, 20) → SHORT
A-013: close > rolling_mean(close, 30) → LONG
A-014: close < rolling_mean(close, 30) → SHORT
A-015: close > rolling_mean(close, 50) → LONG
A-016: close < rolling_mean(close, 50) → SHORT
A-017: close > rolling_mean(close, 100) → LONG
A-018: close < rolling_mean(close, 100) → SHORT
A-019: close > rolling_mean(close, 200) → LONG
A-020: close < rolling_mean(close, 200) → SHORT
```

**Quy tắc sinh A-021..A-200:** Thay P01 bằng P02..P10, giữ nguyên window và direction mapping như trên.

---

# FAMILY B: Rolling Mean Crossover (110 alphas)

Mỗi alpha: **Fast Mean crossover Slow Mean** hoặc **Price crossover Mean**

## Sub-family B1: Price × Mean Crossed (20 alphas)

```python
entry_long = self.op.crossed_above(price, rolling_mean(price, N))
entry_short = self.op.crossed_below(price, rolling_mean(price, N))
exit = ... # reverse cross hoặc time-based
```

| Alpha ID | Price | Window | Logic |
|----------|-------|--------|-------|
| B1-001..B1-010 | P01 | W01..W10 | Crossed above → LONG |
| B1-011..B1-020 | P01 | W01..W10 | Crossed below → SHORT |

## Sub-family B2: Fast × Slow Mean Crossover (90 alphas)

```python
fast_mean = self.feat.rolling_mean(price, N_fast)
slow_mean = self.feat.rolling_mean(price, N_slow)
entry_long = self.op.crossed_above(fast_mean, slow_mean)
entry_short = self.op.crossed_below(fast_mean, slow_mean)
```

| Alpha ID | Price | Fast/Slow | Logic |
|----------|-------|-----------|-------|
| B2-001 | P01 | W02/W04 (5/10) | Fast crossed above Slow → LONG |
| B2-002 | P01 | W02/W04 | Fast crossed below Slow → SHORT |
| B2-003 | P01 | W02/W05 (5/14) | Fast crossed above Slow → LONG |
| B2-004 | P01 | W02/W05 | Fast crossed below Slow → SHORT |
| B2-005 | P01 | W02/W06 (5/20) | Fast crossed above Slow → LONG |
| B2-006 | P01 | W02/W06 | Fast crossed below Slow → SHORT |
| B2-007 | P01 | W03/W06 (8/20) | Fast crossed above Slow → LONG |
| B2-008 | P01 | W03/W06 | Fast crossed below Slow → SHORT |
| B2-009 | P01 | W04/W07 (10/30) | Fast crossed above Slow → LONG |
| B2-010 | P01 | W04/W07 | Fast crossed below Slow → SHORT |
| B2-011 | P01 | W04/W08 (10/50) | Fast crossed above Slow → LONG |
| B2-012 | P01 | W04/W08 | Fast crossed below Slow → SHORT |
| B2-013 | P01 | W05/W08 (14/50) | Fast crossed above Slow → LONG |
| B2-014 | P01 | W05/W08 | Fast crossed below Slow → SHORT |
| B2-015 | P01 | W06/W09 (20/100) | Fast crossed above Slow → LONG |
| B2-016 | P01 | W06/W09 | Fast crossed below Slow → SHORT |
| B2-017 | P01 | W06/W10 (20/200) | Fast crossed above Slow → LONG |
| B2-018 | P01 | W06/W10 | Fast crossed below Slow → SHORT |
| B2-019..B2-036 | P02 | W02..W10 (9 pairs) | Repeat as above |
| B2-037..B2-054 | P03 | W02..W10 | Repeat |
| B2-055..B2-072 | P04 | W02..W10 | Repeat |
| B2-073..B2-090 | P05 | W02..W10 | Repeat |

---

# FAMILY C: Rolling Mean + Confirmation (100 alphas)

Mỗi alpha: **Price vs Rolling Mean + 1 confirmation indicator**

## Công thức chung

```python
mean = self.feat.rolling_mean(price, window=N)
entry_long = (price > mean) & confirmation_long
entry_short = (price < mean) & confirmation_short
```

## Parameter Grid

| Alpha ID | Price | Window | Confirmation | Logic |
|----------|-------|--------|-------------|-------|
| C-001 | P01 | W05 | C01 (RSI > 50) | close > mean(14) & RSI > 50 → LONG |
| C-002 | P01 | W05 | C01 (RSI < 50) | close < mean(14) & RSI < 50 → SHORT |
| C-003 | P01 | W06 | C01 (RSI > 50) | close > mean(20) & RSI > 50 → LONG |
| C-004 | P01 | W06 | C01 (RSI < 50) | close < mean(20) & RSI < 50 → SHORT |
| C-005 | P01 | W08 | C01 (RSI > 50) | close > mean(50) & RSI > 50 → LONG |
| C-006 | P01 | W08 | C01 (RSI < 50) | close < mean(50) & RSI < 50 → SHORT |
| C-007 | P01 | W05 | C02 (ADX > 20) | close > mean(14) & ADX > 20 → LONG |
| C-008 | P01 | W05 | C02 (ADX > 20) | close < mean(14) & ADX > 20 → SHORT |
| C-009 | P01 | W06 | C02 (ADX > 20) | close > mean(20) & ADX > 20 → LONG |
| C-010 | P01 | W06 | C02 (ADX > 20) | close < mean(20) & ADX > 20 → SHORT |
| C-011 | P01 | W08 | C02 (ADX > 20) | close > mean(50) & ADX > 20 → LONG |
| C-012 | P01 | W08 | C02 (ADX > 20) | close < mean(50) & ADX > 20 → SHORT |
| C-013 | P01 | W05 | C03 (MACD > Signal) | close > mean(14) & MACD > Signal → LONG |
| C-014 | P01 | W05 | C03 (MACD < Signal) | close < mean(14) & MACD < Signal → SHORT |
| C-015 | P01 | W06 | C03 (MACD > Signal) | close > mean(20) & MACD > Signal → LONG |
| C-016 | P01 | W06 | C03 (MACD < Signal) | close < mean(20) & MACD < Signal → SHORT |
| C-017 | P01 | W08 | C03 (MACD > Signal) | close > mean(50) & MACD > Signal → LONG |
| C-018 | P01 | W08 | C03 (MACD < Signal) | close < mean(50) & MACD < Signal → SHORT |
| C-019 | P01 | W05 | C04 (Vol > SMA) | close > mean(14) & Vol > SMA20 → LONG |
| C-020 | P01 | W05 | C04 (Vol > SMA) | close < mean(14) & Vol > SMA20 → SHORT |
| C-021..C-030 | P01 | W06,W08,W10 × C04,C05,C06,C07,C08 | Various combos |
| C-031..C-040 | P02 | W05,W06,W08 × C01,C02,C03 | Typical price + confirm |
| C-041..C-050 | P03 | W05,W06,W08 × C05,C06,C09 | Weighted close + confirm |
| C-051..C-060 | P06 | W05,W06,W08 × C01,C02,C03 | OHLC4 + confirm |
| C-061..C-070 | P10 | W05,W06,W08 × C04,C08,C10 | VWAP + confirm |
| C-071..C-080 | P07 | W05,W06,W08 × C01,C02,C03 | High + confirm |
| C-081..C-090 | P08 | W05,W06,W08 × C01,C02,C03 | Low + confirm |
| C-091..C-100 | P09 | W05,W06,W08 × C04,C08,C09 | Volume + confirm |

---

# FAMILY D: Rolling Quantile Price Level (180 alphas)

Mỗi alpha: **PriceSource so sánh với Rolling Quantile của chính nó**

## Công thức chung

```python
quantile = self.feat.rolling_quantile(price, window=N, q=Q)
entry_long = price > quantile     # Giá trên quantile → Long (breakout)
entry_short = price < quantile    # Giá dưới quantile → Short (breakdown)
```

## Parameter Grid

| Alpha ID | Price | Window | q | Direction |
|----------|-------|--------|---|-----------|
| D-001 | P01 | W04 | Q07 (0.80) | close > quantile(10, 0.8) → LONG |
| D-002 | P01 | W04 | Q03 (0.20) | close < quantile(10, 0.2) → SHORT |
| D-003 | P01 | W04 | Q09 (0.95) | close > quantile(10, 0.95) → LONG (extreme) |
| D-004 | P01 | W04 | Q01 (0.05) | close < quantile(10, 0.05) → SHORT (extreme) |
| D-005 | P01 | W04 | Q05 (0.50) | close > quantile(10, 0.5) → LONG (above median) |
| D-006 | P01 | W04 | Q05 (0.50) | close < quantile(10, 0.5) → SHORT (below median) |
| D-007..D-012 | P01 | W05 | Q07,Q03,Q09,Q01,Q05,Q05 | Repeat with window=14 |
| D-013..D-018 | P01 | W06 | Q07,Q03,Q09,Q01,Q05,Q05 | Repeat with window=20 |
| D-019..D-024 | P01 | W07 | Q07,Q03,Q09,Q01,Q05,Q05 | Repeat with window=30 |
| D-025..D-030 | P01 | W08 | Q07,Q03,Q09,Q01,Q05,Q05 | Repeat with window=50 |
| D-031..D-036 | P01 | W09 | Q07,Q03,Q09,Q01,Q05,Q05 | Repeat with window=100 |
| D-037..D-042 | P01 | W10 | Q07,Q03,Q09,Q01,Q05,Q05 | Repeat with window=200 |
| D-043..D-078 | P01 | W01,W02,W03,W01,W02,W03 | Q07,Q03,Q09,Q01,Q05,Q05 | Short windows |
| D-079..D-084 | P02 | W04 | Q07,Q03,Q09,Q01,Q05,Q05 | Typical price |
| D-085..D-090 | P02 | W05 | Q07,Q03,Q09,Q01,Q05,Q05 | |
| D-091..D-096 | P02 | W06 | Q07,Q03,Q09,Q01,Q05,Q05 | |
| D-097..D-102 | P03 | W04 | Q07,Q03,Q09,Q01,Q05,Q05 | Weighted close |
| D-103..D-108 | P03 | W05 | repeat | |
| D-109..D-114 | P03 | W06 | repeat | |
| D-115..D-120 | P04 | W04 | Q07,Q03,Q09,Q01,Q05,Q05 | Median price |
| D-121..D-126 | P04 | W05 | repeat | |
| D-127..D-132 | P04 | W06 | repeat | |
| D-133..D-138 | P05 | W04 | Q07,Q03,Q09,Q01,Q05,Q05 | HLC3 |
| D-139..D-144 | P05 | W05 | repeat | |
| D-145..D-150 | P05 | W06 | repeat | |
| D-151..D-156 | P10 | W04 | Q07,Q03,Q09,Q01,Q05,Q05 | VWAP |
| D-157..D-162 | P10 | W05 | repeat | |
| D-163..D-168 | P10 | W06 | repeat | |
| D-169..D-174 | P09 | W04 | Q07,Q03,Q09,Q01,Q05,Q05 | Volume |
| D-175..D-180 | P09 | W05 | repeat | |

---

# FAMILY E: Rolling Quantile Channel (80 alphas)

Mỗi alpha: **Kênh giá từ Upper/Lower Quantile, giao dịch breakout hoặc reversion**

## Sub-family E1: Quantile Breakout (40 alphas)

```python
upper = self.feat.rolling_quantile(price, window=N, q=Q_HIGH)
lower = self.feat.rolling_quantile(price, window=N, q=Q_LOW)
entry_long = price > upper
entry_short = price < lower
```

| Alpha ID | Price | Window | q_Low | q_High | Logic |
|----------|-------|--------|-------|--------|-------|
| E1-001 | P01 | W04 | 0.20 | 0.80 | close > Q80 → LONG; close < Q20 → SHORT |
| E1-002 | P01 | W05 | 0.20 | 0.80 | Same, window=14 |
| E1-003 | P01 | W06 | 0.20 | 0.80 | Same, window=20 |
| E1-004 | P01 | W07 | 0.20 | 0.80 | Same, window=30 |
| E1-005 | P01 | W08 | 0.20 | 0.80 | Same, window=50 |
| E1-006 | P01 | W04 | 0.10 | 0.90 | tight channel |
| E1-007 | P01 | W05 | 0.10 | 0.90 | tight channel |
| E1-008 | P01 | W06 | 0.10 | 0.90 | tight channel |
| E1-009 | P01 | W04 | 0.05 | 0.95 | extreme channel |
| E1-010 | P01 | W05 | 0.05 | 0.95 | extreme channel |
| E1-011..E1-020 | P02 | W04,W05,W06 | 0.20/0.80, 0.10/0.90, 0.05/0.95 | Typical price |
| E1-021..E1-030 | P03 | W04,W05,W06 | 0.20/0.80, 0.10/0.90, 0.05/0.95 | Weighted close |
| E1-031..E1-040 | P05 | W04,W05,W06 | 0.20/0.80, 0.10/0.90, 0.05/0.95 | HLC3 |

## Sub-family E2: Quantile Mean Reversion (40 alphas)

```python
entry_long = price < lower   # Oversold → buy
entry_short = price > upper  # Overbought → sell
exit_long = price > self.feat.rolling_quantile(price, N, 0.5)  # về median
exit_short = price < self.feat.rolling_quantile(price, N, 0.5)
```

Same parameter grid as E1 but reversed logic (long at lower, short at upper, exit at median).

| Alpha ID | Price | Window | q_Low | q_High | Logic |
|----------|-------|--------|-------|--------|-------|
| E2-001..E2-040 | Same as E1-001..E1-040 | | | Reversion: Long at lower band, Short at upper band |

---

# FAMILY F: Quantile + Confirmation (80 alphas)

Kết hợp quantile breakout/reversion với confirmation indicator.

## Công thức chung

```python
upper = self.feat.rolling_quantile(price, N, 0.8)
lower = self.feat.rolling_quantile(price, N, 0.2)
entry_long = (price > upper) & confirmation_long
entry_short = (price < lower) & confirmation_short
```

| Alpha ID | Price | Window | Confirmation | Logic |
|----------|-------|--------|-------------|-------|
| F-001 | P01 | W05 | C01 (RSI > 50) | Breakout Q80 + RSI>50 → LONG |
| F-002 | P01 | W05 | C01 (RSI < 50) | Breakout Q20 + RSI<50 → SHORT |
| F-003 | P01 | W06 | C01 (RSI > 50) | |
| F-004 | P01 | W06 | C01 (RSI < 50) | |
| F-005 | P01 | W05 | C02 (ADX > 20) | Breakout Q80 + ADX>20 → LONG |
| F-006 | P01 | W05 | C02 (ADX > 20) | Breakout Q20 + ADX>20 → SHORT |
| F-007 | P01 | W06 | C02 (ADX > 20) | |
| F-008 | P01 | W06 | C02 (ADX > 20) | |
| F-009 | P01 | W05 | C03 (MACD > Sig) | Breakout Q80 + MACD Bull → LONG |
| F-010 | P01 | W05 | C03 (MACD < Sig) | Breakout Q20 + MACD Bear → SHORT |
| F-011 | P01 | W06 | C03 (MACD > Sig) | |
| F-012 | P01 | W06 | C03 (MACD < Sig) | |
| F-013 | P01 | W05 | C04 (Vol > SMA20) | Breakout Q80 + High Vol → LONG |
| F-014 | P01 | W05 | C04 (Vol > SMA20) | Breakout Q20 + High Vol → SHORT |
| F-015 | P01 | W06 | C04 (Vol > SMA20) | |
| F-016 | P01 | W06 | C04 (Vol > SMA20) | |
| F-017..F-032 | P01 | W05,W06 | C05 (ROC), C06 (CMO), C09 (MFI), C10 (+DI) | |
| F-033..F-048 | P02 | W05,W06 | C01,C02,C03,C04,C05,C06,C09,C10 | Typical price |
| F-049..F-064 | P03 | W05,W06 | C01,C02,C03,C04,C05,C06,C09,C10 | Weighted close |
| F-065..F-080 | P10 | W05,W06 | C01,C02,C03,C04,C05,C06,C09,C10 | VWAP |

---

# FAMILY G: Multi-Timeframe Alpha (30 alphas)

Kết hợp rolling mean/quantile từ khung thời gian khác nhau.

## Công thức chung

```python
# Khung nhanh (ngắn)
mean_fast = self.feat.rolling_mean(close, 10)
# Khung chậm (dài) - mô phỏng bằng window lớn hơn
mean_slow = self.feat.rolling_mean(close, 50)

# Trend filter từ "higher timeframe"
entry_long = (close > mean_fast) & (mean_fast > mean_slow)
entry_short = (close < mean_fast) & (mean_fast < mean_slow)
```

| Alpha ID | Mean Fast | Mean Slow | Quantile Filter | Logic |
|----------|-----------|-----------|-----------------|-------|
| G-001 | W02 (5) | W06 (20) | — | Price > MA5 & MA5 > MA20 → LONG |
| G-002 | W02 (5) | W06 (20) | — | Price < MA5 & MA5 < MA20 → SHORT |
| G-003 | W04 (10) | W08 (50) | — | Price > MA10 & MA10 > MA50 → LONG |
| G-004 | W04 (10) | W08 (50) | — | Price < MA10 & MA10 < MA50 → SHORT |
| G-005 | W05 (14) | W08 (50) | — | Price > MA14 & MA14 > MA50 → LONG |
| G-006 | W05 (14) | W08 (50) | — | Price < MA14 & MA14 < MA50 → SHORT |
| G-007 | W06 (20) | W09 (100) | — | Price > MA20 & MA20 > MA100 → LONG |
| G-008 | W06 (20) | W09 (100) | — | Price < MA20 & MA20 < MA100 → SHORT |
| G-009 | W06 (20) | W10 (200) | — | Price > MA20 & MA20 > MA200 → LONG |
| G-010 | W06 (20) | W10 (200) | — | Price < MA20 & MA20 < MA200 → SHORT |
| G-011 | W04 (10) | W06 (20) | Q80 breakout | Multitimeframe + quantile |
| G-012 | W04 (10) | W06 (20) | Q20 breakdown | |
| G-013..G-030 | W04,W05,W06 | W06,W08,W10 | Q80, Q20, Q50 | Combinations |

---

# FAMILY H: VnFuture-Specific Alpha (50 alphas)

Tận dụng các trường dữ liệu đặc thù của VnFuture.

## Công thức chung

```python
matched_vol = self.data.fut_matched_volume_vn30f1m_1d
total_vol = self.data.fut_total_volume_vn30f1m_1d
open_int = self.data.fut_open_interest_vn30f1m_1d

vol_ratio = matched_vol / total_vol  # Tỷ lệ khớp lệnh
oi_mean = self.feat.rolling_mean(open_int, window=N)
```

| Alpha ID | Data | Window | Logic |
|----------|------|--------|-------|
| H-001 | matched_volume | W05 | Vol > rolling_mean(vol, 14) → LONG |
| H-002 | matched_volume | W05 | Vol < rolling_mean(vol, 14) → SHORT |
| H-003 | matched_volume | W06 | Vol > rolling_mean(vol, 20) → LONG |
| H-004 | matched_volume | W06 | Vol < rolling_mean(vol, 20) → SHORT |
| H-005 | open_interest | W05 | OI > rolling_mean(OI, 14) → LONG |
| H-006 | open_interest | W05 | OI < rolling_mean(OI, 14) → SHORT |
| H-007 | open_interest | W06 | OI > rolling_mean(OI, 20) → LONG |
| H-008 | open_interest | W06 | OI < rolling_mean(OI, 20) → SHORT |
| H-009 | total_volume | W05 | TVol > rolling_mean(TVol, 14) → LONG |
| H-010 | total_volume | W05 | TVol < rolling_mean(TVol, 14) → SHORT |
| H-011..H-020 | matched_value | W05,W06 | Rolling mean + direction |
| H-021..H-030 | total_value | W05,W06 | Rolling mean + direction |
| H-031..H-040 | agreed_volume | W05,W06 | Quantile of agreed vol |
| H-041..H-050 | agreed_value | W05,W06 | Quantile + value |

---

# FAMILY I: Combined Rolling Mean + Rolling Quantile (30 alphas)

Kết hợp cả rolling mean và rolling quantile trong cùng một alpha.

## Công thức chung

```python
mean = self.feat.rolling_mean(close, N1)
upper = self.feat.rolling_quantile(close, N2, 0.8)
lower = self.feat.rolling_quantile(close, N2, 0.2)

# Breakout + Trend
entry_long = (close > upper) & (close > mean)   # Breakout upper, confirm above mean
entry_short = (close < lower) & (close < mean)   # Breakdown lower, confirm below mean

# Reversion + Trend
entry_long_r = (close < lower) & (close > mean)  # Oversold nhưng vẫn trên mean dài hạn
entry_short_r = (close > upper) & (close < mean) # Overbought nhưng dưới mean dài hạn
```

| Alpha ID | Mean Window | Quantile Window | Logic |
|----------|-------------|-----------------|-------|
| I-001 | W05 (14) | W04 (10) | Long: close > Q80 & close > MA14 |
| I-002 | W05 (14) | W04 (10) | Short: close < Q20 & close < MA14 |
| I-003 | W06 (20) | W05 (14) | Long: close > Q80 & close > MA20 |
| I-004 | W06 (20) | W05 (14) | Short: close < Q20 & close < MA20 |
| I-005 | W08 (50) | W06 (20) | Long: close > Q80 & close > MA50 |
| I-006 | W08 (50) | W06 (20) | Short: close < Q20 & close < MA50 |
| I-007 | W04 (10) | W07 (30) | Combined frame |
| I-008 | W04 (10) | W07 (30) | Opposite |
| I-009..I-015 | W05,W06,W08,W10 | W04,W05,W06,W08 | Various combos (reversion mode) |
| I-016..I-030 | Mixed | Mixed | Scale variants |

---

# FAMILY J: Advanced Alpha (30 alphas)

Kết hợp rolling mean/quantile với candlestick patterns và các logic nâng cao.

## Công thức chung

```python
mean = self.feat.rolling_mean(close, 20)
quantile_80 = self.feat.rolling_quantile(close, 20, 0.8)
quantile_20 = self.feat.rolling_quantile(close, 20, 0.2)

# Pattern detection
hammer = self.feat.hammer(open_, high, low, close)
engulf = self.feat.engulfing_pattern(open_, high, low, close)

entry_long = (hammer | engulf) & (close > mean) & (close < quantile_80)
```

| Alpha ID | Pattern | Filter | Logic |
|----------|---------|--------|-------|
| J-001 | hammer | close > mean(20) | Hammer + above mean → LONG |
| J-002 | hammer | close < mean(20) | Hammer + below mean → LONG (contrarian) |
| J-003 | engulfing_pattern | close > quantile_20 | Bullish engulf + above Q20 → LONG |
| J-004 | engulfing_pattern | close < quantile_80 | Bearish engulf + below Q80 → SHORT |
| J-005 | morning_star | close > mean(14) | Morning star + above MA14 → LONG |
| J-006 | evening_star | close < mean(14) | Evening star + below MA14 → SHORT |
| J-007 | three_white_soldiers | close > quantile_50 | 3WS + above median → LONG |
| J-008 | three_black_crows | close < quantile_50 | 3BC + below median → SHORT |
| J-009 | doji | close > mean(50) | Doji near MA50 (support test) |
| J-010 | harami_pattern | close between Q20-Q80 | Harami inside channel |
| J-011..J-020 | Shooting star, hanging_man, piercing_pattern | Various | Candlestick + mean filter |
| J-021..J-030 | hikkake_pattern, marubozu, spinning_top | Various | Candlestick + quantile filter |

---

## Tổng kết số lượng Alpha

| Family | Mô tả | Số lượng |
|--------|-------|----------|
| A | Rolling Mean Price Level | 200 |
| B | Rolling Mean Crossover | 110 |
| C | Rolling Mean + Confirmation | 100 |
| D | Rolling Quantile Price Level | 180 |
| E | Rolling Quantile Channel | 80 |
| F | Quantile + Confirmation | 80 |
| G | Multi-Timeframe | 30 |
| H | VnFuture-Specific | 50 |
| I | Combined Mean + Quantile | 30 |
| J | Advanced (Patterns) | 30 |
| **Tổng** | | **~890 alphas** |

---

## Hướng dẫn sử dụng

1. **Chọn alpha** từ danh sách theo ID
2. **Mapping** thành code Python theo template
3. **Kiểm thử** theo framework trong `idea/hypothesis/hypothesis_framework.md`
4. **Validate** hard rules (Risk, Drawdown, Liquidity...)
5. **Output** file `.py` vào `output/`

Ví dụ chuyển đổi A-009 thành code:

```python
class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        mean_14 = self.feat.rolling_mean(close, window=14)

        long_setup = close > mean_14     # A-009
        short_setup = close < mean_14    # A-010
        exit_setup = self.op.crossed_above(mean_14, close) | self.op.crossed_below(mean_14, close)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

---

*End of Alpha Generation Document*
