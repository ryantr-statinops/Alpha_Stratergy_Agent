# Thesis 04: Microstructure Flow

> **Core Ideas:** OBI proxy (Balance of Power, Chaikin Money Flow), VPIN proxy (volume/OI imbalance), Margin Call Cascade
> **VN Market Fit:** Retail 80-90% → BOP/CMF detect accumulation/distribution; OI drop + volume spike = margin call cascade; avg trade size surge = whale footprint
> **Data Fields:** `pv_close`, `pv_open`, `pv_high`, `pv_low`, `pv_volume`, `fut_matched_volume_vn30f1m_1d`, `fut_matched_value_vn30f1m_1d`, `fut_open_interest_vn30f1m_1d`, `fut_total_volume_vn30f1m_1d`, `fut_total_value_vn30f1m_1d`
> **Timeframes:** 5min, 15min, 30min

---

## 1. Core API

```
Microstructure:  self.feat.bop(open_, high, low, close)               # Balance of Power
                 self.feat.cmf(high, low, close, volume, timeperiod=N)# Chaikin Money Flow
                 self.feat.ad(high, low, close, volume)               # Acc/Dist
                 self.feat.adosc(high, low, close, volume, fast, slow)# A/D Oscillator
                 self.feat.mfi(high, low, close, volume, timeperiod=N)# Money Flow Index
                 self.feat.obv(close, volume)                         # On Balance Volume

Futures Data:    self.data.fut_matched_volume_vn30f1m_1d
                 self.data.fut_matched_value_vn30f1m_1d
                 self.data.fut_open_interest_vn30f1m_1d
                 self.data.fut_total_volume_vn30f1m_1d
                 self.data.fut_total_value_vn30f1m_1d
                 self.data.fut_agreed_volume_vn30f1m_1d
                 self.data.fut_agreed_value_vn30f1m_1d
```

---

## 2. Templates

### T04-A: Balance of Power + CMF Flow Detection

```python
class CustomStrategy(SimpleAlgorithm):
    cmf_window = {cmf_window}

    def __algorithm__(self):
        close = self.data.pv_close
        open_price = self.data.pv_open
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bop = self.feat.bop(open_price, high, low, close)
        cmf = self.feat.cmf(high, low, close, volume, timeperiod=self.cmf_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        vol_sma = self.feat.sma(volume, timeperiod={vol_window})

        # Buying pressure: BOP > 0 + CMF > 0
        # Selling pressure: BOP < 0 + CMF < 0
        buying_pressure = (bop > 0) & (cmf > 0)
        selling_pressure = (bop < 0) & (cmf < 0)

        long_setup = buying_pressure & (adx_val > 22) & (volume > vol_sma)
        short_setup = selling_pressure & (adx_val > 22) & (volume > vol_sma)
        exit_setup = self.op.crossed_below(cmf, 0) | self.op.crossed_above(cmf, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T04-B: MFI Volume-Weighted Reversal

```python
class CustomStrategy(SimpleAlgorithm):
    mfi_window = {mfi_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        mfi = self.feat.mfi(high, low, close, volume, timeperiod=self.mfi_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        vol_sma = self.feat.sma(volume, timeperiod={vol_window})

        long_setup = (mfi < 30) & (adx_val > 20) & (volume > vol_sma * 0.5)
        short_setup = (mfi > 70) & (adx_val > 20) & (volume > vol_sma * 0.5)
        exit_setup = self.op.crossed_above(mfi, 50) | self.op.crossed_below(mfi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T04-C: OI + Volume Cascade (Margin Call Proxy)

```python
class CustomStrategy(SimpleAlgorithm):
    oi_window = {oi_window}
    vol_window = {vol_window}
    oi_drop_threshold = {oi_drop_threshold}
    vol_spike_mult = {vol_spike_mult}

    def __algorithm__(self):
        close = self.data.pv_close
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d
        oi = self.data.fut_open_interest_vn30f1m_1d

        oi_sma = self.feat.sma(oi, timeperiod=self.oi_window)
        vol_sma = self.feat.sma(matched_vol, timeperiod=self.vol_window)

        oi_change = self.op.fillna(self.op.pct_change(oi, periods=1), value=0)
        oi_drop = oi_change < -self.oi_drop_threshold
        vol_spike = matched_vol > vol_sma * self.vol_spike_mult
        price_fall = self.op.pct_change(close, periods=1) < -{price_fall_threshold}

        cascade = oi_drop & vol_spike & price_fall

        vol_collapse = matched_vol < vol_sma * 0.5
        price_stable = self.op.abs(self.op.pct_change(close, periods=1)) < {price_fall_threshold} * 0.2
        exhaustion = oi_drop & vol_collapse & price_stable

        long_setup = exhaustion
        short_setup = cascade

        exit_setup = self.op.crossed_below(close, oi_sma) | self.op.crossed_above(close, oi_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

**Variant parameter grid:**
| Variant | OI Drop | Vol Spike | Price Fall | return_roll | ADX Entry |
|---------|:-------:|:---------:|:----------:|:-----------:|:---------:|
| Aggr | > 0.5% | > 1.5x | > 0.3% | window=3 | > 20 |
| Std | > 1.0% | > 2.0x | > 0.5% | window=5 | > 22 |
| Cons | > 2.0% | > 3.0x | > 1.0% | window=5 | > 25 |

### T04-D: Whale Footprint — Average Trade Size

```python
class CustomStrategy(SimpleAlgorithm):
    whale_window = {whale_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        matched_val = self.data.fut_matched_value_vn30f1m_1d
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d

        avg_trade = matched_val / matched_vol
        avg_trade_sma = self.feat.sma(avg_trade, timeperiod=self.whale_window)
        avg_trade_std = self.feat.rolling_std(avg_trade, window=self.whale_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        whale = avg_trade > avg_trade_sma + {whale_sigma} * avg_trade_std
        vol_sma = self.feat.sma(matched_vol, timeperiod=self.whale_window)
        price_compression = (self.feat.rolling_max(close, 10) - self.feat.rolling_min(close, 10)) / self.feat.rolling_min(close, 10) < 0.01

        long_setup = whale & price_compression & (matched_vol > vol_sma * 1.5) & (adx_val > 22)
        short_setup = whale & price_compression & (matched_vol > vol_sma * 1.5) & (adx_val > 22)
        exit_setup = self.op.crossed_below(close, self.feat.sma(close, 20)) | self.op.crossed_above(close, self.feat.sma(close, 20))

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T04-E: A/D Oscillator Divergence

```python
class CustomStrategy(SimpleAlgorithm):
    adosc_fast = {adosc_fast}
    adosc_slow = {adosc_slow}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        adosc = self.feat.adosc(high, low, close, volume, fastperiod=self.adosc_fast, slowperiod=self.adosc_slow)
        rsi = self.feat.rsi(close, timeperiod=14)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)

        price_rising = close > self.op.previous(close)
        price_falling = close < self.op.previous(close)

        # Bullish divergence: price down, adosc up
        bullish_div = price_falling & (adosc > self.op.previous(adosc)) & (rsi < 40)
        # Bearish divergence: price up, adosc down
        bearish_div = price_rising & (adosc < self.op.previous(adosc)) & (rsi > 60)

        long_setup = bullish_div & (adx_val > 20)
        short_setup = bearish_div & (adx_val > 20)
        exit_setup = self.op.crossed_below(close, self.feat.sma(close, 14)) | self.op.crossed_above(close, self.feat.sma(close, 14))

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T04-F: OBV Trend Confirmation

```python
class CustomStrategy(SimpleAlgorithm):
    obv_window = {obv_window}

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        obv = self.feat.obv(close, volume)
        obv_sma = self.feat.sma(obv, timeperiod=self.obv_window)
        close_sma = self.feat.sma(close, timeperiod=self.obv_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        long_setup = (close > close_sma) & (obv > obv_sma) & (adx_val > 22)
        short_setup = (close < close_sma) & (obv < obv_sma) & (adx_val > 22)
        exit_setup = self.op.crossed_below(obv, obv_sma) | self.op.crossed_above(obv, obv_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T04-G: Volume Flow Imbalance

```python
class CustomStrategy(SimpleAlgorithm):
    imbalance_window = {imbalance_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        matched_val = self.data.fut_matched_value_vn30f1m_1d
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d
        oi = self.data.fut_open_interest_vn30f1m_1d

        avg_trade = matched_val / matched_vol
        close_sma = self.feat.sma(close, timeperiod=self.imbalance_window)
        oi_change = self.op.fillna(self.op.pct_change(oi, periods=1), value=0)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        # OI tăng + avg trade lớn = smart money accumulation
        smart_money_long = (oi_change > 0) & (avg_trade > self.feat.sma(avg_trade, self.imbalance_window))
        # OI giảm + volume spike = distribution / cascade
        smart_money_short = (oi_change < -0.005) & (matched_vol > self.feat.sma(matched_vol, self.imbalance_window) * 1.5)

        long_setup = smart_money_long & (close > close_sma) & (adx_val > 22)
        short_setup = smart_money_short & (close < close_sma) & (adx_val > 22)
        exit_setup = self.op.crossed_below(close, close_sma) | self.op.crossed_above(close, close_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

---

## 3. Parameter Grid Summary

| Template | Parameter | Values | Variants |
|----------|-----------|--------|----------|
| T04-A | CMF window × ADX × Vol | 3 × 3 × 3 | 18 |
| T04-B | MFI window × ADX | 3W × 3W | 9 |
| T04-C | OI/Vol/Price × 3 variants | 3 variants × 4 TFs | 12 |
| T04-D | Whale window × Sigma | 3W × (1.5, 2.0, 2.5) | 9 |
| T04-E | ADOSC fast/slow | 2 pairs | 8 |
| T04-F | OBV window × ADX | 3W × 3W | 9 |
| T04-G | Imbalance window | 3W | 6 |
| **Total** | | | **~71** |

---

*End of Thesis 04 Design*
