# Thesis 01: Rolling Mean + Quantile

> **Core Ideas:** Rolling Mean, Quantile, Rolling Z-Score, Rolling Rank
> **VN Market Fit:** Retail herding tạo extreme moves → quantile extremes detect FOMO/panic; mean filters trend
> **Data Fields:** `pv_close`, `pv_high`, `pv_low`, `pv_volume`, `pv_vn30_close`, `pv_dji_close`, `fut_*`
> **Timeframes:** 5min, 15min, 30min, 60min

---

## 1. Core API

```
Rolling Mean:    self.feat.rolling_mean(s1, window=N)
                 self.feat.sma(close, timeperiod=N)
                 self.feat.ema(series, timeperiod=N)
                 self.feat.kama(series, timeperiod=N)    # Kaufman Adaptive
                 self.feat.mama(series)                   # MESA Adaptive → (mama, fama)
                 self.feat.wma / dema / tema / t3 / trima

Quantile:        self.feat.rolling_quantile(s1, window=N, q=0.5)
                 self.feat.rolling_rank(s1, window=N)
                 self.feat.rolling_percentile_rank(s1, window=N)
                 self.feat.rolling_median(s1, window=N)
                 self.feat.rolling_mad(s1, window=N)

Z-Score:         self.feat.rolling_zscore(s1, window=N)
                 self.feat.zscore(s1, timeperiod=N)
                 self.feat.price_z(close, timeperiod=N)
                 self.feat.volume_z(volume, timeperiod=N)
```

---

## 2. Templates

### T01-A: Price vs Rolling Mean (Level)

```python
class CustomStrategy(SimpleAlgorithm):
    mean_window = {mean_window}

    def __algorithm__(self):
        close = self.data.pv_close

        mean = self.feat.rolling_mean(close, window=self.mean_window)

        long_setup = close > mean
        short_setup = close < mean
        exit_setup = self.op.crossed_below(close, mean) | self.op.crossed_above(close, mean)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

**Variants:** 10 price sources × 10 windows × 2 directions = 200 variants
Price sources: close, typical (hlc3), weighted (wclprice), median (medprice), ohlc4, high, low, volume, vwap
Windows: 3, 5, 8, 10, 14, 20, 30, 50, 100, 200

### T01-B: Rolling Mean Crossover

```python
class CustomStrategy(SimpleAlgorithm):
    fast_window = {fast_window}
    slow_window = {slow_window}

    def __algorithm__(self):
        close = self.data.pv_close

        fast_ma = self.feat.sma(close, timeperiod=self.fast_window)
        slow_ma = self.feat.sma(close, timeperiod=self.slow_window)

        long_setup = self.op.crossed_above(fast_ma, slow_ma)
        short_setup = self.op.crossed_below(fast_ma, slow_ma)
        exit_setup = self.op.crossed_below(fast_ma, slow_ma) | self.op.crossed_above(fast_ma, slow_ma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

**Variants:** 5 price sources × 5 fast/slow pairs × 2 directions = 50 variants

### T01-C: Mean + Confirmation

```python
class CustomStrategy(SimpleAlgorithm):
    mean_window = {mean_window}

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        mean = self.feat.rolling_mean(close, window=self.mean_window)
        rsi = self.feat.rsi(close, timeperiod={rsi_window})
        vol_sma = self.feat.sma(volume, timeperiod={vol_window})

        long_setup = (close > mean) & (rsi > 50) & (volume > vol_sma)
        short_setup = (close < mean) & (rsi < 50) & (volume > vol_sma)
        exit_setup = self.op.crossed_below(close, mean) | self.op.crossed_above(close, mean)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

**Confirmation options:** RSI > 50, ADX > 22, MACD > Signal, Volume > SMA, ROC > 0, CMO > 0, +DI > -DI, MFI > 50

### T01-D: Price vs Rolling Quantile (Breakout)

```python
class CustomStrategy(SimpleAlgorithm):
    q_window = {q_window}
    q_high = {q_high}
    q_low = {q_low}

    def __algorithm__(self):
        close = self.data.pv_close

        upper = self.feat.rolling_quantile(close, window=self.q_window, q=self.q_high)
        lower = self.feat.rolling_quantile(close, window=self.q_window, q=self.q_low)

        long_setup = close > upper
        short_setup = close < lower
        exit_setup = self.op.crossed_below(close, upper) | self.op.crossed_above(close, lower)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

**Variant quantile pairs:** (0.80, 0.20), (0.90, 0.10), (0.95, 0.05), (0.75, 0.25), (0.85, 0.15)

### T01-E: Mean + Quantile Channel

```python
class CustomStrategy(SimpleAlgorithm):
    mean_window = {mean_window}
    q_window = {q_window}

    def __algorithm__(self):
        close = self.data.pv_close

        mean = self.feat.rolling_mean(close, window=self.mean_window)
        upper = self.feat.rolling_quantile(close, window=self.q_window, q=0.8)
        lower = self.feat.rolling_quantile(close, window=self.q_window, q=0.2)

        # Breakout + trend alignment
        long_setup = (close > upper) & (close > mean)
        short_setup = (close < lower) & (close < mean)
        exit_setup = self.op.crossed_below(close, mean) | self.op.crossed_above(close, mean)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T01-F: Rolling Z-Score Mean Reversion

```python
class CustomStrategy(SimpleAlgorithm):
    z_window = {z_window}
    z_entry = {z_entry}

    def __algorithm__(self):
        close = self.data.pv_close

        price_z = self.feat.rolling_zscore(close, window=self.z_window)

        long_setup = price_z < -self.z_entry
        short_setup = price_z > self.z_entry
        exit_setup = self.op.between(price_z, -1, 1)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

**Variant z-entry thresholds:** 2.0, 2.5, 3.0, 1.5

### T01-G: Adaptive MA (KAMA/MAMA)

```python
class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close

        mama, fama = self.feat.mama(close)
        kama = self.feat.kama(close, timeperiod={kama_window})

        long_setup = (close > kama) & (mama > fama)
        short_setup = (close < kama) & (mama < fama)
        exit_setup = self.op.crossed_below(close, kama) | self.op.crossed_above(close, kama)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

---

## 3. Parameter Grid Summary

| Template | Parameter | Values | Variants |
|----------|-----------|--------|----------|
| T01-A | Price source × Window × Dir | 10P × 10W × 2D | 200 |
| T01-B | Fast/Slow pairs × Price | 5 pairs × 5P | 50 |
| T01-C | Window × Confirmation | 3W × 8C | 48 |
| T01-D | Quantile pair × Window | 5Q × 6W | 30 |
| T01-E | Mean window × Q window | 4W × 3W | 12 |
| T01-F | Z-window × threshold | 4W × 4T | 16 |
| T01-G | KAMA window | 4W | 8 |
| **Total** | | | **~364** |

---

*End of Thesis 01 Design*
