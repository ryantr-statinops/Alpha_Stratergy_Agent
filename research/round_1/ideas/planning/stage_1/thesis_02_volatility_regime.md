# Thesis 02: Volatility Regime

> **Core Ideas:** Volatility Clustering (GARCH proxy), HMM proxy (regime detection)
> **VN Market Fit:** Không có circuit breaker → trend momentum mạnh, biến động cụm; margin call cascade tạo vol spike; retail herding gây regime change nhanh
> **Data Fields:** `pv_close`, `pv_high`, `pv_low`, `pv_volume`
> **Timeframes:** 5min, 15min, 30min, 60min

---

## 1. Core API

```
Volatility:      self.feat.rolling_std(close, window=N)
                 self.feat.var(close, timeperiod=N)
                 self.feat.stddev(close, timeperiod=N)
                 self.feat.atr(high, low, close, timeperiod=N)
                 self.feat.natr(high, low, close, timeperiod=N)     # ATR %
                 self.feat.trange(high, low, close)

Regime:          self.feat.adx(high, low, close, timeperiod=N)
                 self.feat.adxr(high, low, close, timeperiod=N)     # Smoothed ADX
                 self.feat.trendmode(close)                          # 1=trend, 0=cycle
                 self.feat.kama(close, timeperiod=N)                 # Adaptive to regime
                 self.feat.mama(close) → (mama, fama)
                 self.feat.dcperiod(close)                           # Dominant cycle
```

---

## 2. Templates

### T02-A: Rolling Std Regime — Volatility Breakout

Detect volatility expansion → trade breakout direction.

```python
class CustomStrategy(SimpleAlgorithm):
    vol_window = {vol_window}
    vol_entry = {vol_entry}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        atr = self.feat.atr(high, low, close, timeperiod=self.vol_window)
        atr_sma = self.feat.sma(atr, timeperiod=self.vol_window)
        adx_val = self.feat.adx(high, low, close, timeperiod=self.vol_window)

        vol_expansion = atr > atr_sma * self.vol_entry
        roc = self.feat.roc(close, timeperiod=5)

        long_setup = vol_expansion & (roc > 0) & (adx_val > 22)
        short_setup = vol_expansion & (roc < 0) & (adx_val > 22)
        exit_setup = (atr < atr_sma) | self.op.crossed_below(adx_val, 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T02-B: Rolling Std Regime — Mean Reversion (Low Vol)

Detect volatility compression → trade mean reversion.

```python
class CustomStrategy(SimpleAlgorithm):
    vol_window = {vol_window}
    vol_compress = {vol_compress}
    rsi_window = {rsi_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        atr = self.feat.atr(high, low, close, timeperiod=self.vol_window)
        atr_sma = self.feat.sma(atr, timeperiod=self.vol_window)
        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)

        vol_compression = atr < atr_sma * self.vol_compress

        long_setup = vol_compression & (rsi < 30)
        short_setup = vol_compression & (rsi > 70)
        exit_setup = self.op.crossed_above(rsi, 50) | self.op.crossed_below(rsi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T02-C: Regime Classification (HMM Proxy)

3-state regime detection → different trading rules per regime.

```python
class CustomStrategy(SimpleAlgorithm):
    adx_window = {adx_window}
    vol_window = {vol_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        adx_val = self.feat.adx(high, low, close, timeperiod=self.adx_window)
        atr = self.feat.atr(high, low, close, timeperiod=self.vol_window)
        atr_sma = self.feat.sma(atr, timeperiod=self.vol_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        vol_ratio = volume / vol_sma
        vol_regime = self.feat.rolling_std(atr, window=self.vol_window)
        vol_regime_sma = self.feat.sma(vol_regime, window=self.vol_window)

        # Regime: 3-state classification
        # State 1: Strong trend + high vol → momentum
        # State 2: Weak trend + low vol → mean reversion
        # State 3: Ranging → flat
        roc_fast = self.feat.roc(close, timeperiod=5)
        upper_q = self.feat.rolling_quantile(close, window=20, q=0.8)
        lower_q = self.feat.rolling_quantile(close, window=20, q=0.2)

        momentum_mode = (adx_val > 25) & (vol_regime > vol_regime_sma)
        meanrev_mode = (adx_val < 22) & (vol_regime < vol_regime_sma)

        # Momentum entries (State 1)
        mom_long = momentum_mode & (roc_fast > 0) & (volume > vol_sma)
        mom_short = momentum_mode & (roc_fast < 0) & (volume > vol_sma)

        # Mean reversion entries (State 2)
        mr_long = meanrev_mode & (close < lower_q) & (volume < vol_sma)
        mr_short = meanrev_mode & (close > upper_q) & (volume < vol_sma)

        long_setup = mom_long | mr_long
        short_setup = mom_short | mr_short
        exit_setup = self.op.crossed_below(adx_val, 15) | (adx_val < 18)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T02-D: ATR Trailing Stop + Trend

Use ATR for both entry filter and trailing stop.

```python
class CustomStrategy(SimpleAlgorithm):
    atr_window = {atr_window}
    atr_mult = {atr_mult}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        atr = self.feat.atr(high, low, close, timeperiod=self.atr_window)
        ema = self.feat.ema(close, timeperiod={ema_window})
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        long_setup = (close > ema) & (adx_val > 22) & (close > (close - atr * self.atr_mult))
        short_setup = (close < ema) & (adx_val > 22) & (close < (close + atr * self.atr_mult))
        exit_setup = self.op.crossed_below(close, ema) | self.op.crossed_above(close, ema)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T02-E: Normalized ATR Regime Switching

Use NATR (%) for cross-asset comparable volatility regime.

```python
class CustomStrategy(SimpleAlgorithm):
    natr_window = {natr_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        natr = self.feat.natr(high, low, close, timeperiod=self.natr_window)
        natr_sma = self.feat.sma(natr, timeperiod=self.natr_window)
        adx_val = self.feat.adx(high, low, close, timeperiod=self.natr_window)

        high_vol = natr > natr_sma * 1.3
        low_vol = natr < natr_sma * 0.7

        # High vol → trend following (wider stop)
        # Low vol → mean reversion (tighter stop)

        roc = self.feat.roc(close, timeperiod=5)
        rsi = self.feat.rsi(close, timeperiod=14)

        long_trend = high_vol & (roc > 0) & (adx_val > 22)
        short_trend = high_vol & (roc < 0) & (adx_val > 22)
        long_rev = low_vol & (rsi < 30) & (adx_val < 20)
        short_rev = low_vol & (rsi > 70) & (adx_val < 20)

        long_setup = long_trend | long_rev
        short_setup = short_trend | short_rev
        exit_setup = self.op.crossed_below(adx_val, 15) | (natr < natr_sma * 0.5)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T02-F: Adaptive KAMA Trend

KAMA tự động điều chỉnh tốc độ theo volatility regime.

```python
class CustomStrategy(SimpleAlgorithm):
    kama_window = {kama_window}
    kama_slow = {kama_slow}
    kama_fast = {kama_fast}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        kama = self.feat.kama(close, timeperiod=self.kama_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        long_setup = (close > kama) & (adx_val > 22)
        short_setup = (close < kama) & (adx_val > 22)
        exit_setup = self.op.crossed_below(close, kama) | self.op.crossed_above(close, kama)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

---

## 3. Parameter Grid Summary

| Template | Parameter | Values | Variants |
|----------|-----------|--------|----------|
| T02-A | Vol window × Entry mult | 4W × (1.3, 1.5, 2.0) | 12 |
| T02-B | Vol window × Compress × RSI | 4W × (0.5, 0.7) × (14, 21) | 16 |
| T02-C | ADX window × Vol window | 4W × 4W | 16 |
| T02-D | ATR window × Mult × EMA | 4W × (2, 3) × 2W | 16 |
| T02-E | NATR window | 4W | 8 |
| T02-F | KAMA window × ADX | 4W × 4W | 16 |
| **Total** | | | **~84** |

---

*End of Thesis 02 Design*
