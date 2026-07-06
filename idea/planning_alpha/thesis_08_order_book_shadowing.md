# Thesis 08: Order Book Shadowing — Institutional Footprint Proxy

> **Core Idea:** Phát hiện "bóng ma sổ lệnh" — dùng dữ liệu futures (OI, matched volume, agreed volume, value/volume ratio) để phát hiện khi nào lệnh chặn lớn đang được dựng lên hoặc gỡ bỏ, từ đó trade breakout/reversal.
> 
> **VN Market Fit:** Retail 80-90% thường sợ khối lượng chặn lớn, trong khi đó là "bẫy thanh khoản" do tay to spoof. Khi lệnh chặn biến mất, giá lao qua mức đó rất nhanh.
> 
> **Data Fields:** `fut_open_interest_vn30f1m_1d`, `fut_matched_volume_vn30f1m_1d`, `fut_matched_value_vn30f1m_1d`, `fut_agreed_volume_vn30f1m_1d`, `fut_agreed_value_vn30f1m_1d`, `pv_close`, `pv_volume`, `pv_vn30_close`
> 
> **Timeframes:** 15min, 30min, 60min (daily `fut_*` fields được broadcast xuống intraday bars)

---

## 1. Core API

```
OHLCV:            self.data.pv_close, self.data.pv_high, self.data.pv_low, self.data.pv_volume
                  self.data.pv_open
Futures:          self.data.fut_open_interest_vn30f1m_1d
                  self.data.fut_matched_volume_vn30f1m_1d
                  self.data.fut_matched_value_vn30f1m_1d
                  self.data.fut_agreed_volume_vn30f1m_1d
                  self.data.fut_agreed_value_vn30f1m_1d
                  self.data.fut_total_volume_vn30f1m_1d
                  self.data.fut_total_value_vn30f1m_1d
VN30:             self.data.pv_vn30_close

Features:         self.feat.rolling_zscore(s1, window=N)
                  self.feat.volume_z(volume, timeperiod=N)
                  self.feat.price_z(close, timeperiod=N)
                  self.feat.rolling_max(s1, window=N)
                  self.feat.rolling_min(s1, window=N)
                  self.feat.sma(s1, timeperiod=N)
                  self.feat.ema(s1, timeperiod=N)
                  self.feat.adx(high, low, close, timeperiod=N)
                  self.feat.roc(close, timeperiod=N)
                  self.feat.rsi(close, timeperiod=N)
                  self.feat.beta(s1, s2, timeperiod=N)

Operators:        self.op.crossed_above(s1, s2)
                  self.op.crossed_below(s1, s2)
                  self.op.fillna(s, value=0)
                  self.op.pct_change(s, periods=1)
                  self.op.abs(s)
                  self.op.between(s, lower, upper)
```

---

## 2. Proxy Signals & Interpretation

### Proxy A: OI Divergence (Open Interest Divergence)
- **Cơ chế:** Khi giá VN30F chạm vùng kháng cự (rolling_max), OI bắt đầu giảm = các lệnh chặn (short positions) đang được đóng = "bức tường" biến mất
- **Tín hiệu:** OI giảm > 1σ + giá tại rolling_max của N phiên = breakout short-term sắp xảy ra
- **Short counterpart:** OI giảm + giá tại rolling_min = short covering = bounce

### Proxy B: Volume Absorption (Khối lượng hấp thụ)
- **Cơ chế:** Matched volume spike tại vùng resistance nhưng giá không break = liquidity đang bị hấp thụ bởi tay to
- **Tín hiệu:** Volume > SMA(vol, N) * 1.5 + giá nằm trong range hẹp (high - low < ATR * 0.5) = absorption đang diễn ra
- **Exit:** Khi volume đột ngột giảm mà giá vẫn giữ level = wall đã consumed, chuẩn bị breakout

### Proxy C: Agreed Volume Footprint (Dấu chân thỏa thuận)
- **Cơ chế:** Thỏa thuận (agreed volume) là block deals institutional. Khi agreed volume tăng đột biến, tay to đang positioning
- **Tín hiệu:** Agreed volume z-score > 2.0 + price cùng hướng = follow institutional flow
- **Exit:** Agreed volume z-score < 0.5 (giao dịch thỏa thuận kết thúc)

### Proxy D: Large Lot Ratio (Tỷ lệ lệnh lớn)
- **Cơ chế:** matched_value / matched_volume ratio cao = giao dịch giá trị lớn (institutional size)
- **Tín hiệu:** Ratio z-score > 1.5 + direction confirmation = tay to đang tích lũy/phân phối
- **Exit:** Ratio z-score < 0 (trở về retail dominance)

---

## 3. Templates

### T08-A: OI Wall Detection

Phát hiện OI divergence tại key levels (support/resistance).

```python
class CustomStrategy(SimpleAlgorithm):
    oi_window = {oi_window}
    vol_window = {vol_window}
    return_window = {return_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        oi = self.data.fut_open_interest_vn30f1m_1d

        oi_z = self.feat.rolling_zscore(oi, window=self.oi_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        res_level = self.feat.rolling_max(close, window=self.oi_window)
        sup_level = self.feat.rolling_min(close, window=self.oi_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        # OI divergence: giá chạm resistance, OI giảm = wall đang được gỡ
        at_resistance = close >= res_level * 0.995
        at_support = close <= sup_level * 1.005
        oi_collapse = oi_z < -1.0

        long_setup = at_support & oi_collapse & (volume > vol_sma) & (adx_val > 18)
        short_setup = at_resistance & oi_collapse & (volume > vol_sma) & (adx_val > 18)
        exit_setup = (oi_z > 0) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T08-B: Volume Absorption

Phát hiện volume spike tại key levels không break → absorption.

```python
class CustomStrategy(SimpleAlgorithm):
    vol_window = {vol_window}
    return_window = {return_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d

        vol_ma = self.feat.sma(matched_vol, timeperiod=self.vol_window)
        vol_ratio = matched_vol / vol_ma
        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        range_pct = (high - low) / close
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        # Absorption: volume spike + range hẹp (giá không break)
        absorption = (vol_ratio > 1.5) & (range_pct < self.feat.sma(range_pct, timeperiod=20) * 0.7)
        res_level = self.feat.rolling_max(close, window=20)
        sup_level = self.feat.rolling_min(close, window=20)

        at_resistance = close >= res_level * 0.995
        at_support = close <= sup_level * 1.005

        # Long tại support sau absorption, short tại resistance sau absorption
        long_setup = at_support & absorption & (adx_val > 18) & (return_roll > 0)
        short_setup = at_resistance & absorption & (adx_val > 18) & (return_roll < 0)
        exit_setup = (vol_ratio < 1.0) | (adx_val < 15) | (self.op.abs(return_roll) < 0.0001)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T08-C: Agreed Volume Footprint

Phát hiện institutional positioning qua agreed volume spike.

```python
class CustomStrategy(SimpleAlgorithm):
    agree_window = {agree_window}
    vol_window = {vol_window}
    return_window = {return_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        agreed_vol = self.data.fut_agreed_volume_vn30f1m_1d
        agreed_val = self.data.fut_agreed_value_vn30f1m_1d

        agree_z = self.feat.rolling_zscore(agreed_vol, window=self.agree_window)
        vol_ma = self.feat.sma(volume, timeperiod=self.vol_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        roc_val = self.feat.roc(close, timeperiod=5)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        # Agreed volume spike = institutional positioning
        institutional_activity = agree_z > {agree_entry}

        long_setup = institutional_activity & (roc_val > 0) & (volume > vol_ma) & (adx_val > 18) & (return_roll > 0)
        short_setup = institutional_activity & (roc_val < 0) & (volume > vol_ma) & (adx_val > 18) & (return_roll < 0)
        exit_setup = (agree_z < 0.5) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T08-D: Large Lot Ratio Detection

Phát hiện institutional size trades qua matched value/volume ratio.

```python
class CustomStrategy(SimpleAlgorithm):
    ratio_window = {ratio_window}
    vol_window = {vol_window}
    return_window = {return_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d
        matched_val = self.data.fut_matched_value_vn30f1m_1d

        # Large lot ratio = matched_value / matched_volume
        lot_ratio = matched_val / matched_vol
        ratio_z = self.feat.rolling_zscore(lot_ratio, window=self.ratio_window)
        vol_ma = self.feat.sma(volume, timeperiod=self.vol_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        vn30_close = self.data.pv_vn30_close
        futures_premium = close / vn30_close
        premium_z = self.feat.rolling_zscore(futures_premium, window=self.ratio_window)

        # Ratio z-score cao = large lots active (institutional)
        # Kết hợp basis premium để confirm direction
        large_lots = ratio_z > {ratio_entry}

        long_setup = large_lots & (premium_z > 0) & (volume > vol_ma) & (adx_val > 18) & (return_roll > 0)
        short_setup = large_lots & (premium_z < 0) & (volume > vol_ma) & (adx_val > 18) & (return_roll < 0)
        exit_setup = (ratio_z < 0) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### T08-E: Composite Shadow (All 4 Proxies)

Kết hợp cả 4 proxy với z-score composite, signal mạnh khi nhiều proxy đồng thuận.

```python
class CustomStrategy(SimpleAlgorithm):
    composite_window = {composite_window}
    vol_window = {vol_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        oi = self.data.fut_open_interest_vn30f1m_1d
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d
        matched_val = self.data.fut_matched_value_vn30f1m_1d
        agreed_vol = self.data.fut_agreed_volume_vn30f1m_1d
        vn30_close = self.data.pv_vn30_close

        # Factor 1: OI divergence
        oi_z = self.feat.rolling_zscore(oi, window=self.composite_window)

        # Factor 2: Volume absorption (matched volume z-score)
        matched_z = self.feat.rolling_zscore(matched_vol, window=self.composite_window)

        # Factor 3: Agreed volume footprint
        agree_z = self.feat.rolling_zscore(agreed_vol, window=self.composite_window)

        # Factor 4: Large lot ratio
        lot_ratio = matched_val / matched_vol
        ratio_z = self.feat.rolling_zscore(lot_ratio, window=self.composite_window)

        # Factor 5: Basis premium
        premium = close / vn30_close
        premium_z = self.feat.rolling_zscore(premium, window=self.composite_window)

        # Composite (equal weighted)
        # OI giảm = positive signal (wall removed), volume + agreed = institutional flow
        shadow_composite = (-oi_z) + matched_z + agree_z + ratio_z + premium_z

        vol_ma = self.feat.sma(volume, timeperiod=self.vol_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=3)

        composite_threshold = {composite_entry}

        long_setup = (shadow_composite > composite_threshold) & (volume > vol_ma) & (adx_val > 20) & (return_roll > 0)
        short_setup = (shadow_composite < -composite_threshold) & (volume > vol_ma) & (adx_val > 20) & (return_roll < 0)
        exit_setup = (self.op.abs(shadow_composite) < 0.5) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

---

## 4. Parameter Grid Summary

| Template | Parameter | Values | Variants |
|----------|-----------|--------|:--------:|
| T08-A | oi_window × vol_window | [14, 20, 34] × [14, 20] | 6 |
| T08-B | vol_window | [14, 20, 34] | 3 |
| T08-C | agree_window × agree_entry | [14, 20, 34] × [1.5, 2.0] | 6 |
| T08-D | ratio_window × ratio_entry | [14, 20, 34] × [1.5, 2.0] | 6 |
| T08-E | composite_window × composite_entry | [14, 20] × [2.0, 3.0, 4.0] | 6 |
| **Total** | | | **~27 variants** |

---

## 5. Data Consideration

Vì `fut_*` fields đều là daily (`_1d` suffix), trên intraday timeframe platform sẽ broadcast giá trị daily xuống mỗi bar. Do đó:
- Signal chỉ thay đổi 1 lần/ngày (khi daily bar mới)
- Entry/exit được xử lý trên intraday bars với daily condition
- Timeframes: 15min, 30min, 60min đều khả thi

---

## 6. Risk Considerations

| Risk | Mitigation |
|------|-----------|
| `fut_*` data latency (daily chỉ cập nhật sau phiên) | Dùng `rolling_zscore` để signal không phụ thuộc vào giá trị tuyệt đối |
| OI giảm vì lý do khác (không phải spoof) | Kết hợp volume + ADX filter để confirm |
| Agreed volume thấp (không có thỏa thuận) | Template fallback: nếu agree volume = 0 thì dùng matched volume làm proxy |
| Overfitting trên daily data | Rolling window parameters được scale theo timeframe convention |

---

*End of Thesis 08 Design*
