# Single-Feat Alpha — Danh sách Indicator đủ mạnh để đánh đơn

> Nguồn: `syntax/feature_syntax.md` (140+ indicators)
> Nguyên tắc: Chỉ dùng **1 feat duy nhất** làm tín hiệu chính, không kết hợp nhiều indicator.

---

## Tier 1 — Tín hiệu rõ ràng, độc lập, actionable ngay

Các feat này tự thân đã cho oversold/overbought, divergence, hoặc tín hiệu entry/exit trực tiếp. Chỉ cần 1 threshold là có thể giao dịch.

### Momentum Oscillators

| Feat | Signal | Entry | Exit | Timeframe |
|------|--------|-------|------|-----------|
| **`rsi(close, 14)`** | Oversold < 30, Overbought > 70 | `rsi < 30` → long; `rsi > 70` → short | `crossed_above(rsi, 50)` hoặc `rsi > 50` | 15, 30, 60 |
| **`stoch(high, low, close, 14, 3, 3)`** | %K < 20 oversold, %K > 80 overbought | `k < 20` → long; `k > 80` → short | `crossed_above(k, 50)` | 15, 30 |
| **`stochrsi(close, 14, 14, 3, 3)`** | Nhạy hơn RSI, bắt sớm reversal | `stochrsi < 0.2` → long; `> 0.8` → short | `crossed_above(stochrsi, 0.5)` | 15, 30 |
| **`cci(high, low, close, 20)`** | Overbought > +100, Oversold < -100 | `cci < -100` → long; `cci > 100` → short | `crossed_above(cci, 0)` | 15, 30, 60 |
| **`willr(high, low, close, 14)`** | Oversold < -80, Overbought > -20 | `willr < -80` → long; `willr > -20` → short | `crossed_above(willr, -50)` | 15, 30 |
| **`cmo(close, 14)`** | -100/+100, nhạy hơn RSI | `cmo < -50` → long; `cmo > 50` → short | `crossed_above(cmo, 0)` | 15, 30, 60 |

### Trend / Directional

| Feat | Signal | Entry | Exit | Timeframe |
|------|--------|-------|------|-----------|
| **`sar(high, low, 0.02, 0.2)`** | Dot flip báo đảo trend | `sar < close` → long; `sar > close` → short | `crossed_below(close, sar)` | 15, 30, 60 |
| **`mama(close, 0.5, 0.05)`** | (mama, fama) crossover | `crossed_above(mama, fama)` → long; `crossed_below(mama, fama)` → short | `crossed_below(mama, fama)` | 15, 30 |
| **`ht_trendline(close)`** | Hilbert trend direction | `close > ht_trendline` → long; `close < ht_trendline` → short | `crossed_below(close, ht_trendline)` | 15, 30, 60 |
| **`aroonosc(high, low, 25)`** | -100 đến +100, trend strength + direction | `aroonosc > 0` → long; `aroonosc < 0` → short | `crossed_below(aroonosc, 0)` | 15, 30, 60 |
| **`bop(open, high, low, close)`** | +1/-1, sức mạnh buyer/seller | `bop > 0.5` → long; `bop < -0.5` → short | `crossed_below(bop, 0)` | 5, 15, 30 |

### Volume / Flow

| Feat | Signal | Entry | Exit | Timeframe |
|------|--------|-------|------|-----------|
| **`obv(close, volume)`** | Divergence với price | `obv > rolling_mean(obv, 20)` → long; `obv < rolling_mean(obv, 20)` → short | `crossed_below(obv, rolling_mean(obv, 20))` | 15, 30, 60 |
| **`mfi(high, low, close, volume, 14)`** | Volume-weighted RSI, 0-100 | `mfi < 20` → long; `mfi > 80` → short | `crossed_above(mfi, 50)` | 15, 30, 60 |
| **`cmf(high, low, close, volume, 20)`** | +1/-1, money flow | `cmf < -0.3` → long; `cmf > 0.3` → short | `crossed_above(cmf, 0)` | 15, 30, 60 |
| **`ad(high, low, close, volume)`** | Accumulation/distribution | `ad > rolling_mean(ad, 20)` → long; `ad < rolling_mean(ad, 20)` → short | `crossed_below(ad, rolling_mean(ad, 20))` | 15, 30, 60 |

### Volatility / Price Extremes

| Feat | Signal | Entry | Exit | Timeframe |
|------|--------|-------|------|-----------|
| **`bbands(close, 20, 2)`** | Price chạm band → reversal | `close < lower_band` → long; `close > upper_band` → short | `crossed_above(close, middle_band)` | 15, 30, 60 |
| **`price_z(close, 20)`** | Z-score > 2 hoặc < -2 | `price_z < -2` → long; `price_z > 2` → short | `abs(price_z) < 1` | 15, 30, 60 |
| **`rolling_zscore(close, 20)`** | Tương tự price_z | `rolling_zscore < -2` → long; `rolling_zscore > 2` → short | `abs(rolling_zscore) < 1` | 15, 30, 60 |
| **`donchian_upper(high, 20)` / `donchian_lower(low, 20)`** | Breakout levels | `close > donchian_upper` → long; `close < donchian_lower` → short | `crossed_below(close, donchian_upper)` | 15, 30, 60 |

### Candlestick Reversal

| Feat | Signal | Entry | Exit | Timeframe |
|------|--------|-------|------|-----------|
| **`engulfing_pattern(open, high, low, close)`** | Bullish/bearish engulfing | `engulfing_pattern == 1` → long; `engulfing_pattern == -1` → short | `engulfing_pattern == -1` (hoặc time stop) | 15, 30 |
| **`morning_star(open, high, low, close, 10)`** | 3-bar bullish reversal | `morning_star == 1` → long | time stop (5 bars) | 15, 30 |
| **`evening_star(open, high, low, close, 10)`** | 3-bar bearish reversal | `evening_star == 1` → short | time stop (5 bars) | 15, 30 |
| **`hammer(open, high, low, close)`** | Single-bar bullish reversal | `hammer == 1` → long | time stop (3 bars) | 15, 30 |
| **`shooting_star(open, high, low, close)`** | Single-bar bearish reversal | `shooting_star == 1` → short | time stop (3 bars) | 15, 30 |
| **`marubozu(open, high, low, close)`** | No shadow → directional strength | `marubozu == 1` → long; `marubozu == -1` → short | time stop (3 bars) | 15, 30 |
| **`three_white_soldiers(open, high, low, close, 10)`** | 3-bar bullish confirmation | `three_white_soldiers == 1` → long | time stop (5 bars) | 30, 60 |
| **`three_black_crows(open, high, low, close, 10)`** | 3-bar bearish confirmation | `three_black_crows == 1` → short | time stop (5 bars) | 30, 60 |

### Statistics / Rolling

| Feat | Signal | Entry | Exit | Timeframe |
|------|--------|-------|------|-----------|
| **`linearreg_slope(close, 20)`** | Trend speed (dương = tăng, âm = giảm) | `linearreg_slope > 0` → long; `linearreg_slope < 0` → short | `crossed_below(linearreg_slope, 0)` | 15, 30, 60 |
| **`linearreg_angle(close, 20)`** | Trend angle (độ) | `linearreg_angle > 10` → long; `linearreg_angle < -10` → short | `crossed_below(linearreg_angle, 0)` | 15, 30, 60 |
| **`tsf(close, 20)`** | Future price projection | `tsf > close` → long; `tsf < close` → short | `crossed_below(tsf, close)` | 15, 30, 60 |
| **`rolling_rank(close, 20)`** | Percentile rank (0-1) | `rolling_rank < 0.1` → long; `rolling_rank > 0.9` → short | `abs(rolling_rank - 0.5) < 0.2` | 15, 30, 60 |
| **`rolling_argmax(high, 20)`** | Bar since recent high | `rolling_argmax >= 10` → long (mean reversion); `rolling_argmax == 0` → short (new high fade) | time stop | 15, 30, 60 |
| **`rolling_argmin(low, 20)`** | Bar since recent low | `rolling_argmin >= 10` → short (mean reversion); `rolling_argmin == 0` → long (new low fade) | time stop | 15, 30, 60 |

---

## Tier 2 — Cần thêm 1 filter đơn giản

Các feat này cho tín hiệu tốt nhưng cần 1 filter phụ (volume, ADX, hoặc threshold) để tránh nhiễu.

| Feat | Filter cần thêm | Lý do |
|------|----------------|-------|
| **`ema(close, 20)`** | So sánh với price hoặc MA khác | Bản thân MA là lagging, cần cross |
| **`sma(close, 20)`** | So sánh với price | Tương tự EMA |
| **`macd(close, 12, 26, 9)`** | Lấy 1 output (hist) | Histogram đổi dấu = signal |
| **`ppo(close, 12, 26, 9)`** | Signal line cross | Tương tự MACD |
| **`momemtum(close, 10)`** | Threshold > 0 | Cần ngưỡng động |
| **`roc(close, 10)`** | Threshold > 0 | Cần ngưỡng động |
| **`trix(close, 15)`** | Signal cross | Cần signal line |
| **`ultosc(high, low, close, 7, 14, 28)`** | Threshold | Hơi phức tạp cho đơn feat |
| **`adx(high, low, close, 14)`** | Chỉ strength, không direction | Cần +DI/-DI hoặc price direction |
| **`dx(high, low, close, 14)`** | Chỉ strength | Cần price direction |
| **`atr(high, low, close, 14)`** | Volatility filter | Không direction, cần price |
| **`volume_z(volume, 20)`** | Unusual volume | Cần kết hợp price move |
| **`correl(close, vn30_close, 20)`** | Cross-asset | Cần price direction |
| **`beta(close, vn30_close, 20)`** | Relative risk | Cần price direction |

---



## Template code cho Single-Feat Alpha

```python
class SingleFeatAlpha(SimpleAlgorithm):

    # Chỉ 1-2 params cần thiết
    feat_window = 14
    entry_threshold = 30      # oversold
    exit_threshold = 50       # neutral

    def __algorithm__(self):
        # Layer 1: Data
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        # Layer 2: Single Feature
        rsi = self.feat.rsi(close, window=self.feat_window)

        # Layer 3: Logic
        long_setup = rsi < self.entry_threshold
        short_setup = rsi > (100 - self.entry_threshold)
        exit_setup = self.op.crossed_above(rsi, self.exit_threshold) | self.op.crossed_below(rsi, 100 - self.exit_threshold)

        # Mutual exclusive guard
        assert not (long_setup & short_setup).any()

        # Layer 4: Position
        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1.0)
        self.set_positions(short_setup, position=-1.0)
```

---

## Lưu ý khi thiết kế Single-Feat Alpha

1. **Neutral zone**: Luôn có gap giữa entry và exit threshold (vd entry=30, exit=50)
2. **Mutual exclusive**: Long và short không thể cùng true trên 1 bar
3. **Time stop**: Với candlestick patterns, luôn kèm time stop (3-5 bars) thay vì chờ tín hiệu ngược
4. **Không dùng `crossed_*` + level mixed**: Nếu entry dùng level (`rsi < 30`), exit dùng level (`rsi > 50`), không dùng `crossed_above`
5. **Không cần trend_filter / volume_filter**: Single feat tự thân đã đủ tín hiệu
