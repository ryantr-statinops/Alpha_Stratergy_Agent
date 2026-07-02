# Thesis 06: Multi-Factor Composite

> **Core Ideas:** Z-score composite của tất cả signals từ T01-T05, tiered sizing theo ADX, multi-layer confirmation
> **VN Market Fit:** Tổng hợp nhiều tín hiệu để giảm false signal trong thị trường retail-dominated; tiered sizing thích ứng với regime
> **Data Fields:** All fields
> **Timeframes:** 15min, 30min, 60min

---

## 1. Core API

```
Composite:       self.feat.rolling_zscore(s1, window=N)
                 self.feat.rolling_rank(s1, window=N)
                 self.feat.zscore(s1, timeperiod=N)
                 self.feat.price_z(close, timeperiod=N)
                 self.feat.volume_z(volume, timeperiod=N)
                 self.feat.add(s1, s2)
                 self.feat.mult(s1, s2)
                 self.feat.sub(s1, s2)
                 self.feat.div(s1, s2)

Regime:          self.feat.adx(high, low, close, timeperiod=N)
                 self.feat.trendmode(close)
                 self.feat.rolling_std(s1, window=N)
```

---

## 2. Templates

### T06-A: Z-Score Composite — 3-Factor

```python
class CustomStrategy(SimpleAlgorithm):
    z_window = {z_window}
    z_threshold = {z_threshold}
    rsi_window = {rsi_window}

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        high = self.data.pv_high
        low = self.data.pv_low

        # Factor 1: Price momentum
        price_z = self.feat.rolling_zscore(close, window=self.z_window)

        # Factor 2: Volume
        vol_z = self.feat.volume_z(volume, timeperiod=self.z_window)

        # Factor 3: ROC momentum
        momentum = self.feat.roc(close, timeperiod=self.rsi_window)
        mom_z = self.feat.rolling_zscore(momentum, window=self.z_window)

        # Composite = equal-weighted z-score sum
        composite = price_z + mom_z + vol_z
        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        rsi_ok = self.op.between(rsi, 30, 70)

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        core_long = (composite > self.z_threshold)
        core_short = (composite < -self.z_threshold)

        strong_long = core_long & rsi_ok & (adx_val > 22) & (vol_z > 0) & (return_roll > 0)
        weak_long = core_long & rsi_ok & (adx_val > 18) & (return_roll > 0)
        strong_short = core_short & rsi_ok & (adx_val > 22) & (vol_z < 0) & (return_roll < 0)
        weak_short = core_short & rsi_ok & (adx_val > 18) & (return_roll < 0)

        exit_setup = (self.op.abs(composite) < 0.5) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-1)
```

### T06-B: 4-Factor Composite (Price + Volume + Volatility + Cross-Market)

```python
class CustomStrategy(SimpleAlgorithm):
    z_window = {z_window}
    z_threshold = {z_threshold}

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        high = self.data.pv_high
        low = self.data.pv_low
        vn30_close = self.data.pv_vn30_close

        # Factor 1: Price
        price_z = self.feat.price_z(close, timeperiod=self.z_window)

        # Factor 2: Volume
        vol_z = self.feat.volume_z(volume, timeperiod=self.z_window)

        # Factor 3: Volatility (ATR)
        atr = self.feat.atr(high, low, close, timeperiod=14)
        vola_z = self.feat.rolling_zscore(atr, window=self.z_window)

        # Factor 4: Cross-market (futures vs VN30)
        ratio = close / vn30_close
        ratio_z = self.feat.rolling_zscore(ratio, window=self.z_window)

        composite = price_z + vol_z + vola_z + ratio_z

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        rsi = self.feat.rsi(close, timeperiod=14)

        core_long = (composite > self.z_threshold) & (rsi > 30) & (rsi < 70)
        core_short = (composite < -self.z_threshold) & (rsi > 30) & (rsi < 70)

        strong_long = core_long & (adx_val > 22) & (vol_z > 0) & (return_roll > 0)
        weak_long = core_long & (adx_val > 18) & (return_roll > 0)
        strong_short = core_short & (adx_val > 22) & (vol_z < 0) & (return_roll < 0)
        weak_short = core_short & (adx_val > 18) & (return_roll < 0)

        exit_setup = (self.op.abs(composite) < 1.0) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-1)
```

### T06-C: Trend + Momentum + Volume + Volatility Layer

Multi-layer confirmation: mỗi layer phải đồng thuận.

```python
class CustomStrategy(SimpleAlgorithm):
    mid_window = {mid_window}
    vol_window = {vol_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close

        # Layer 1: Trend (EMA)
        ema = self.feat.ema(close, timeperiod=self.mid_window)
        trend_ok = close > ema

        # Layer 2: Momentum (ROC)
        roc = self.feat.roc(close, timeperiod={roc_window})
        momentum_ok = roc > 0

        # Layer 3: Volume
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        volume_ok = volume > vol_sma

        # Layer 4: Volatility (ATR trend)
        atr = self.feat.atr(high, low, close, timeperiod=14)
        atr_trend = atr > self.feat.sma(atr, timeperiod=self.vol_window)

        # Layer 5: Cross-market
        vn30_roc = self.feat.roc(vn30_close, timeperiod={roc_window})
        vn30_ok = vn30_roc > 0

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        # Core with layers
        core_long = trend_ok & momentum_ok & vn30_ok
        core_short = (~trend_ok) & (~momentum_ok) & (~vn30_ok)

        strong_long = core_long & volume_ok & atr_trend & (adx_val > 22) & (return_roll > 0)
        weak_long = core_long & (adx_val > 18) & (return_roll > 0)
        strong_short = core_short & volume_ok & atr_trend & (adx_val > 22) & (return_roll < 0)
        weak_short = core_short & (adx_val > 18) & (return_roll < 0)

        exit_setup = self.op.crossed_below(close, ema) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-1)
```

### T06-D: Z-Score Composite + Candlestick Confirmation

Kết hợp z-score composite với candlestick pattern để tăng độ tin cậy.

```python
class CustomStrategy(SimpleAlgorithm):
    z_window = {z_window}

    def __algorithm__(self):
        close = self.data.pv_close
        open_price = self.data.pv_open
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close

        # Z-score factors
        price_z = self.feat.price_z(close, timeperiod=self.z_window)
        vol_z = self.feat.volume_z(volume, timeperiod=self.z_window)
        momentum = self.feat.roc(close, timeperiod=14)
        mom_z = self.feat.rolling_zscore(momentum, window=self.z_window)

        composite = price_z + mom_z + vol_z

        # Candlestick confirmation
        hammer = self.feat.hammer(open_price, high, low, close)
        engulf = self.feat.engulfing_pattern(open_price, high, low, close)
        morning = self.feat.morning_star(open_price, high, low, close)
        evening = self.feat.evening_star(open_price, high, low, close)

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        bullish_pattern = hammer | engulf | morning
        bearish_pattern = evening  # Add more bearish patterns

        long_setup = (composite > 1.5) & bullish_pattern & (adx_val > 22) & (return_roll > 0)
        short_setup = (composite < -1.5) & bearish_pattern & (adx_val > 22) & (return_roll < 0)
        exit_setup = (self.op.abs(composite) < 0.5) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T06-E: Adaptive Regime-Weighted Composite

Trọng số các factor thay đổi theo regime thị trường.

```python
class CustomStrategy(SimpleAlgorithm):
    z_window = {z_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        atr = self.feat.atr(high, low, close, timeperiod=14)
        atr_sma = self.feat.sma(atr, timeperiod=20)

        # Regime detection
        strong_trend = adx_val > 25
        weak_trend = (adx_val > 20) & (adx_val <= 25)
        high_vol = atr > atr_sma * 1.3

        # Factors
        price_z = self.feat.price_z(close, timeperiod=self.z_window)
        vol_z = self.feat.volume_z(volume, timeperiod=self.z_window)
        momentum = self.feat.roc(close, timeperiod=14)
        mom_z = self.feat.rolling_zscore(momentum, window=self.z_window)
        ratio = close / vn30_close
        ratio_z = self.feat.rolling_zscore(ratio, window=self.z_window)

        # Regime-weighted composite
        if strong_trend:
            composite = price_z * 1.5 + mom_z * 1.0 + vol_z * 0.5
        elif high_vol:
            composite = price_z * 1.0 + vol_z * 1.5 + ratio_z * 0.5
        else:
            composite = price_z * 0.5 + ratio_z * 1.0 + mom_z * 0.5

        rsi = self.feat.rsi(close, timeperiod=14)

        strong_long = (composite > {z_entry}) & (adx_val > 22) & (rsi > 40) & (return_roll > 0)
        weak_long = (composite > {z_entry}) & (adx_val > 18) & (return_roll > 0)
        strong_short = (composite < -{z_entry}) & (adx_val > 22) & (rsi < 60) & (return_roll < 0)
        weak_short = (composite < -{z_entry}) & (adx_val > 18) & (return_roll < 0)

        exit_setup = (self.op.abs(composite) < 0.5) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-1)
```

---

## 3. Parameter Grid Summary

| Template | Parameter | Values | Variants |
|----------|-----------|--------|----------|
| T06-A | Z-window × Threshold × RSI | 3W × (2, 3) × 2W | 12 |
| T06-B | Z-window × Threshold × ADX | 3W × (2, 3, 4) × 3W | 18 |
| T06-C | Mid × Vol × ROC × ADX | 3W × 3W × 2W × 3W | 24 |
| T06-D | Z-window × Pattern combo | 3W × 3 combos | 9 |
| T06-E | Z-window × Z-entry | 3W × (2, 3) | 6 |
| **Total** | | | **~69** |

---

*End of Thesis 06 Design*
