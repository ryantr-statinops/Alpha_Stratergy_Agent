# Thesis 05: Cross-Market Correlation

> **Core Ideas:** Correlation, Cointegration proxy (spread z-score), Beta, Relative strength
> **VN Market Fit:** Basis (futures-cash) biến động mạnh → spread z-score trade; DJI global spillover; VN30 index confirmation
> **Data Fields:** `pv_close`, `pv_vn30_open`, `pv_vn30_high`, `pv_vn30_low`, `pv_vn30_close`, `pv_vn30_volume`, `pv_dji_open`, `pv_dji_high`, `pv_dji_low`, `pv_dji_close`, `pv_dji_volume`
> **Timeframes:** 15min, 30min, 60min

---

## 1. Core API

```
Correlation:     self.feat.correl(s1, s2, timeperiod=N)                # Pearson r
                 self.feat.rolling_correlation(s1, s2, window=N)        # Rolling
                 self.feat.beta(s1, s2, timeperiod=N)                   # Beta
                 self.feat.rolling_covariance(s1, s2, window=N)         # Covariance

Regression:      self.feat.linearreg_intercept(s1, timeperiod=N)
                 self.feat.linearreg_slope(s1, timeperiod=N)
                 self.feat.linearreg(s1, timeperiod=N)
                 self.feat.tsf(s1, timeperiod=N)

Volatility:      self.feat.atr(high, low, close, timeperiod=N)
                 self.feat.rolling_std(s1, window=N)
```

---

## 2. Templates

### T05-A: Futures-VN30 Spread Reversion (Cointegration Proxy)

```python
class CustomStrategy(SimpleAlgorithm):
    beta_window = {beta_window}
    z_entry = {z_entry}

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        high = self.data.pv_high
        low = self.data.pv_low

        # Spread = futures - beta * VN30
        beta_val = self.feat.beta(close, vn30_close, timeperiod=self.beta_window)
        spread = close - beta_val * vn30_close
        spread_z = self.feat.rolling_zscore(spread, window=self.beta_window)

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        basis = close - vn30_close
        basis_sma = self.feat.sma(basis, timeperiod=self.beta_window)

        # Spread extreme → mean reversion
        long_setup = (spread_z < -self.z_entry) & (adx_val > 20)
        short_setup = (spread_z > self.z_entry) & (adx_val > 20)
        exit_setup = self.op.between(spread_z, -1, 1) | self.op.crossed_below(adx_val, 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T05-B: VN30 Momentum Confirmation

```python
class CustomStrategy(SimpleAlgorithm):
    roc_window = {roc_window}

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close

        fut_roc = self.feat.roc(close, timeperiod=self.roc_window)
        vn30_roc = self.feat.roc(vn30_close, timeperiod=self.roc_window)

        long_setup = (fut_roc > 0) & (vn30_roc > 0)
        short_setup = (fut_roc < 0) & (vn30_roc < 0)
        exit_setup = self.op.crossed_below(fut_roc, 0) | self.op.crossed_above(fut_roc, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T05-C: Futures-Cash Basis Extreme

```python
class CustomStrategy(SimpleAlgorithm):
    basis_window = {basis_window}
    basis_entry = {basis_entry}

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        high = self.data.pv_high
        low = self.data.pv_low

        basis = close - vn30_close
        basis_z = self.feat.rolling_zscore(basis, window=self.basis_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d
        vol_sma = self.feat.sma(matched_vol, timeperiod=self.basis_window)

        # Basis extreme + volume fading = reversion imminent
        long_setup = (basis_z < -self.basis_entry) & (matched_vol < vol_sma) & (adx_val > 20)
        short_setup = (basis_z > self.basis_entry) & (matched_vol < vol_sma) & (adx_val > 20)
        exit_setup = self.op.between(basis_z, -1, 1)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T05-D: DJI Global Spillover

```python
class CustomStrategy(SimpleAlgorithm):
    roc_window = {roc_window}

    def __algorithm__(self):
        close = self.data.pv_close
        dji_close = self.data.pv_dji_close
        vn30_close = self.data.pv_vn30_close

        dji_roc = self.feat.roc(dji_close, timeperiod=self.roc_window)
        fut_roc = self.feat.roc(close, timeperiod=self.roc_window)
        vn30_roc = self.feat.roc(vn30_close, timeperiod=self.roc_window)

        # Consensus: cả 3 cùng hướng
        bullish = (fut_roc > 0) & (vn30_roc > 0) & (dji_roc > 0)
        bearish = (fut_roc < 0) & (vn30_roc < 0) & (dji_roc < 0)

        long_setup = bullish
        short_setup = bearish
        exit_setup = (~bullish) & (~bearish)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T05-E: Rolling Correlation Trend Filter

```python
class CustomStrategy(SimpleAlgorithm):
    correl_window = {correl_window}

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        dji_close = self.data.pv_dji_close
        high = self.data.pv_high
        low = self.data.pv_low

        fut_vn30_correl = self.feat.rolling_correlation(close, vn30_close, window=self.correl_window)
        fut_dji_correl = self.feat.rolling_correlation(close, dji_close, window=self.correl_window)

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        roc = self.feat.roc(close, timeperiod={roc_window})

        # Chỉ trade khi correlation đồng thuận
        correl_aligned = (fut_vn30_correl > 0.5) & (fut_dji_correl > 0)
        correl_negative = (fut_vn30_correl < -0.3) | (fut_dji_correl < -0.3)

        long_setup = correl_aligned & (roc > 0) & (adx_val > 22)
        short_setup = correl_aligned & (roc < 0) & (adx_val > 22)
        exit_setup = correl_negative | self.op.crossed_below(adx_val, 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T05-F: Relative Strength Ratio

```python
class CustomStrategy(SimpleAlgorithm):
    rs_window = {rs_window}

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close

        ratio = close / vn30_close
        ratio_sma = self.feat.sma(ratio, timeperiod=self.rs_window)
        ratio_roc = self.feat.roc(ratio, timeperiod=self.rs_window)
        ratio_slope = self.feat.linearreg_slope(ratio, timeperiod=self.rs_window)

        long_setup = (ratio > ratio_sma) & (ratio_roc > 0) & (ratio_slope > 0)
        short_setup = (ratio < ratio_sma) & (ratio_roc < 0) & (ratio_slope < 0)
        exit_setup = self.op.crossed_below(ratio, ratio_sma) | self.op.crossed_above(ratio, ratio_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T05-G: Correlation Breakdown Detection

```python
class CustomStrategy(SimpleAlgorithm):
    correl_window = {correl_window}

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        high = self.data.pv_high
        low = self.data.pv_low

        correl = self.feat.rolling_correlation(close, vn30_close, window=self.correl_window)
        correl_sma = self.feat.sma(correl, window=self.correl_window)
        correl_std = self.feat.rolling_std(correl, window=self.correl_window)

        # Breakdown: correlation drops > 2σ below mean
        breakdown = correl < (correl_sma - 2 * correl_std)
        # Rebuilding: correlation rising from low
        rebuilding = self.op.crossed_above(correl, correl_sma)

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        vol_sma = self.feat.sma(self.data.pv_volume, timeperiod={vol_window})
        volume = self.data.pv_volume

        # Trade breakdown: thị trường disconnect → cơ hội arbitrage
        long_setup = breakdown & (volume > vol_sma * 1.5) & (adx_val > 20)
        short_setup = breakdown & (volume > vol_sma * 1.5) & (adx_val > 20)
        exit_setup = rebuilding | self.op.crossed_below(adx_val, 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

---

## 3. Parameter Grid Summary

| Template | Parameter | Values | Variants |
|----------|-----------|--------|----------|
| T05-A | Beta window × Z-entry | 3W × (2.0, 2.5, 3.0) | 9 |
| T05-B | ROC window | 3W | 6 |
| T05-C | Basis window × Entry | 3W × (2.0, 2.5) | 6 |
| T05-D | ROC window | 3W | 6 |
| T05-E | Correl window × ROC | 3W × 3W | 9 |
| T05-F | RS window | 3W | 6 |
| T05-G | Correl window × Vol | 3W × 3W | 9 |
| **Total** | | | **~51** |

---

*End of Thesis 05 Design*
