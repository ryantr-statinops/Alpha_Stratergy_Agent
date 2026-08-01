# Thesis 03: Time-Series Decomposition

> **Core Ideas:** Time-Series Decomposition (Hilbert Transform), Entropy proxy (dispersion)
> **VN Market Fit:** Phân biệt trend vs cycle để tránh trade ngược xu hướng; phát hiện regime change sớm qua sine/leadsine crossover
> **Data Fields:** `pv_close`
> **Timeframes:** 15min, 30min, 60min (5min too noisy for decomposition)

---

## 1. Core API

```
Decomposition:   self.feat.ht_trendline(series)          # Trend component
                 self.feat.dcperiod(close)                # Dominant cycle period
                 self.feat.trendmode(close)               # 1=trend, 0=cycle
                 self.feat.sine(close) → (sine, leadsine) # Cycle turning points
                 self.feat.linearreg(s1, timeperiod=N)    # Linear regression
                 self.feat.linearreg_slope(s1, timeperiod=N)
                 self.feat.linearreg_angle(s1, timeperiod=N)
                 self.feat.linearreg_intercept(s1, timeperiod=N)
                 self.feat.tsf(s1, timeperiod=N)          # Time series forecast

Dispersion:      self.feat.rolling_mad(s1, window=N)      # Robust dispersion
                 self.feat.rolling_std(s1, window=N)
                 self.faat.rolling_percentile_rank(s1, N) # Distribution shape
```

---

## 2. Templates

### T03-A: Hilbert Trendline + Sine Cycle Trading

```python
class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        trend = self.feat.ht_trendline(close)
        sine, leadsine = self.feat.sine(close)
        cycle_mode = self.feat.trendmode(close) == 0
        trend_mode = self.feat.trendmode(close) == 1
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        # Cycle mode: trade sine/leadsine crossover
        cycle_long = (sine > leadsine) & cycle_mode & (close > trend)
        cycle_short = (sine < leadsine) & cycle_mode & (close < trend)

        # Trend mode: trade trendline direction
        trend_long = (close > trend) & trend_mode & (adx_val > 22)
        trend_short = (close < trend) & trend_mode & (adx_val > 22)

        long_setup = cycle_long | trend_long
        short_setup = cycle_short | trend_short
        exit_setup = self.op.crossed_below(close, trend) | self.op.crossed_above(close, trend)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T03-B: Dominant Cycle Period — Adaptive Position Sizing

Dùng dcperiod để xác định cycle length → điều chỉnh position.

```python
class CustomStrategy(SimpleAlgorithm):
    base_window = {base_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        cycle_period = self.feat.dcperiod(close)
        trend = self.feat.ht_trendline(close)
        adx_val = self.feat.adx(high, low, close, timeperiod=self.base_window)

        # Scale position size based on cycle period
        # Short cycle → smaller size (noisier)
        # Long cycle → full size (more confident)
        cycle_ma = self.feat.sma(cycle_period, timeperiod=10)
        vol_scale = self.op.clip(cycle_ma / {max_cycle}, 0.3, 1.0)

        roc = self.feat.roc(close, timeperiod=5)

        long_setup = (close > trend) & (roc > 0) & (adx_val > 22)
        short_setup = (close < trend) & (roc < 0) & (adx_val > 22)
        exit_setup = self.op.crossed_below(close, trend) | self.op.crossed_above(close, trend)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=vol_scale)
        self.set_positions(short_setup, position=-vol_scale)
```

### T03-C: Linear Regression Slope Trend

```python
class CustomStrategy(SimpleAlgorithm):
    lr_window = {lr_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        slope = self.feat.linearreg_slope(close, timeperiod=self.lr_window)
        angle = self.feat.linearreg_angle(close, timeperiod=self.lr_window)
        forecast = self.feat.tsf(close, timeperiod=self.lr_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        long_setup = (slope > 0) & (angle > 5) & (close < forecast) & (adx_val > 22)
        short_setup = (slope < 0) & (angle < -5) & (close > forecast) & (adx_val > 22)
        exit_setup = self.op.crossed_below(slope, 0) | self.op.crossed_above(slope, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T03-D: Cycle Turning Point (Sine/Leadsine Crossover)

```python
class CustomStrategy(SimpleAlgorithm):
    rsi_window = {rsi_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        sine, leadsine = self.feat.sine(close)
        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        trend = self.feat.ht_trendline(close)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        # Crossover signals cycle turning point
        cycle_up = self.op.crossed_above(sine, leadsine)
        cycle_down = self.op.crossed_below(sine, leadsine)

        long_setup = cycle_up & (rsi > 30) & (adx_val > 20)
        short_setup = cycle_down & (rsi < 70) & (adx_val > 20)
        exit_setup = self.op.crossed_below(close, trend) | self.op.crossed_above(close, trend)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T03-E: Dispersion (Entropy Proxy)

Dùng rolling_mad / rolling_std ratio đo độ "hỗn loạn" của thị trường.

```python
class CustomStrategy(SimpleAlgorithm):
    mad_window = {mad_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        mad = self.feat.rolling_mad(close, window=self.mad_window)
        std = self.feat.rolling_std(close, window=self.mad_window)
        mad_ratio = mad / std
        mad_ratio_sma = self.feat.sma(mad_ratio, timeperiod=self.mad_window)

        # Low mad_ratio = structured market (trend following)
        # High mad_ratio = chaotic market (avoid)
        structured = mad_ratio < mad_ratio_sma * 0.8
        chaotic = mad_ratio > mad_ratio_sma * 1.2

        ema = self.feat.ema(close, timeperiod={ema_window})
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        long_setup = (close > ema) & structured & (adx_val > 22)
        short_setup = (close < ema) & structured & (adx_val > 22)
        exit_setup = self.op.crossed_below(close, ema) | self.op.crossed_above(close, ema) | chaotic

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

---

## 3. Parameter Grid Summary

| Template | Parameter | Values | Variants |
|----------|-----------|--------|----------|
| T03-A | ADX window | 4W | 8 |
| T03-B | Base window × Max cycle | 3W × (30, 50) | 6 |
| T03-C | LR window × ADX | 3W × 3W | 9 |
| T03-D | RSI window | 3W | 6 |
| T03-E | MAD window × EMA | 3W × 3W | 9 |
| **Total** | | | **~38** |

---

*End of Thesis 03 Design*
