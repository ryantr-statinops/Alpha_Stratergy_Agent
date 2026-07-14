# Single-Feat Alpha — Danh sách Indicator đủ mạnh để đánh đơn

> Nguồn: `syntax/feature_syntax.md` (140+ indicators)
> Nguyên tắc: Chỉ dùng **1 feat duy nhất** làm tín hiệu chính, không kết hợp nhiều indicator.
> Pattern: Trend following (`feat > threshold` → long, `feat < threshold` → short, `crossed(feat, threshold)` → exit)

---

## Đã gen (33 indicators)

| File | Indicator | Threshold | Data |
|------|-----------|-----------|------|
| `SF_RSI_15min.py` | `rsi(close, 14)` | 50 | `close` |
| `SF_CCI_15min.py` | `cci(high, low, close, 20)` | 0 | `close, high, low` |
| `SF_CMO_15min.py` | `cmo(close, 14)` | 0 | `close` |
| `SF_WillR_15min.py` | `willr(high, low, close, 14)` | -50 | `close, high, low` |
| `SF_STOCH_15min.py` | `stoch(high, low, close, 14, 3, 3)` | 50 | `close, high, low` |
| `SF_STOCHRSI_15min.py` | `stochrsi(close, 14, 14, 3, 3)` | 0.5 | `close` |
| `SF_AROONOSC_15min.py` | `aroonosc(high, low, 25)` | 0 | `high, low` |
| `SF_LINEARREG_SLOPE_15min.py` | `linearreg_slope(close, 20)` | 0 | `close` |
| `SF_LINEARREG_ANGLE_15min.py` | `linearreg_angle(close, 20)` | 0 | `close` |
| `SF_TSF_15min.py` | `tsf(close, 20)` | — | `close` |
| `SF_SAR_15min.py` | `sar(high, low, 0.02, 0.2)` | — | `close, high, low` |
| `SF_MAMA_15min.py` | `mama(close, 0.5, 0.05)` | — | `close` |
| `SF_HT_TRENDLINE_15min.py` | `ht_trendline(close)` | — | `close` |
| `SF_BOP_15min.py` | `bop(open, high, low, close)` | — | `open, high, low, close` |
| `SF_OBV_15min.py` | `obv(close, volume)` | — | `close, volume` |
| `SF_MFI_15min.py` | `mfi(high, low, close, volume, 14)` | — | `close, high, low, volume` |
| `SF_CMF_15min.py` | `cmf(high, low, close, volume, 20)` | — | `close, high, low, volume` |
| `SF_AD_15min.py` | `ad(high, low, close, volume)` | — | `close, high, low, volume` |
| `SF_BBANDS_15min.py` | `bbands(close, 20, 2)` | — | `close` |
| `SF_PRICE_Z_15min.py` | `price_z(close, 20)` | — | `close` |
| `SF_ROLLING_ZSCORE_15min.py` | `rolling_zscore(close, 20)` | — | `close` |
| `SF_DONCHIAN_15min.py` | `donchian_upper/lower(high/low, 20)` | — | `close, high, low` |
| `SF_ENGULFING_15min.py` | `engulfing_pattern(open, high, low, close)` | — | `open, high, low, close` |
| `SF_MORNING_STAR_15min.py` | `morning_star(open, high, low, close, 10)` | — | `open, high, low, close` |
| `SF_EVENING_STAR_15min.py` | `evening_star(open, high, low, close, 10)` | — | `open, high, low, close` |
| `SF_HAMMER_15min.py` | `hammer(open, high, low, close)` | — | `open, high, low, close` |
| `SF_SHOOTING_STAR_15min.py` | `shooting_star(open, high, low, close)` | — | `open, high, low, close` |
| `SF_MARUBOZU_15min.py` | `marubozu(open, high, low, close)` | — | `open, high, low, close` |
| `SF_3WHITE_SOLDIERS_15min.py` | `three_white_soldiers(open, high, low, close, 10)` | — | `open, high, low, close` |
| `SF_3BLACK_CROWS_15min.py` | `three_black_crows(open, high, low, close, 10)` | — | `open, high, low, close` |
| `SF_ROLLING_RANK_15min.py` | `rolling_rank(close, 20)` | — | `close` |
| `SF_ROLLING_ARGMAX_15min.py` | `rolling_argmax(high, 20)` | — | `high` |
| `SF_ROLLING_ARGMIN_15min.py` | `rolling_argmin(low, 20)` | — | `low` |

---

## Tier 1A — Fit pattern trend-following (có thể gen ngay)

Các indicator dùng được pattern `feat > threshold → long, feat < threshold → short, exit = crossed(feat, threshold)`.

| Feat | Data | Threshold | Entry | Exit | Gen |
|------|------|-----------|-------|------|-----|
| **`rsi(close, 14)`** | `close` | 50 | `rsi > 50` / `rsi < 50` | `crossed(rsi, 50)` | ✅ `SF_RSI_15min.py` |
| **`cci(high, low, close, 20)`** | `close, high, low` | 0 | `cci > 0` / `cci < 0` | `crossed(cci, 0)` | ✅ `SF_CCI_15min.py` |
| **`cmo(close, 14)`** | `close` | 0 | `cmo > 0` / `cmo < 0` | `crossed(cmo, 0)` | ✅ `SF_CMO_15min.py` |
| **`willr(high, low, close, 14)`** | `close, high, low` | -50 | `willr > -50` / `willr < -50` | `crossed(willr, -50)` | ✅ `SF_WillR_15min.py` |
| **`stoch(high, low, close, 14, 3, 3)`** | `close, high, low` | 50 | `k > 50` / `k < 50` | `crossed(k, 50)` | ✅ `SF_STOCH_15min.py` |
| **`stochrsi(close, 14, 14, 3, 3)`** | `close` | 0.5 | `stochrsi > 0.5` / `< 0.5` | `crossed(stochrsi, 0.5)` | ✅ `SF_STOCHRSI_15min.py` |
| **`aroonosc(high, low, 25)`** | `high, low` | 0 | `aroonosc > 0` / `aroonosc < 0` | `crossed(aroonosc, 0)` | ✅ `SF_AROONOSC_15min.py` |
| **`linearreg_slope(close, 20)`** | `close` | 0 | `linearreg_slope > 0` / `< 0` | `crossed(linearreg_slope, 0)` | ✅ `SF_LINEARREG_SLOPE_15min.py` |
| **`linearreg_angle(close, 20)`** | `close` | 0 | `linearreg_angle > 0` / `< 0` | `crossed(linearreg_angle, 0)` | ✅ `SF_LINEARREG_ANGLE_15min.py` |
| **`tsf(close, 20)`** | `close` | — | `tsf > close` / `tsf < close` | `crossed(tsf, close)` | ✅ `SF_TSF_15min.py` |

---

## Tier 1B — Cần custom logic (không fit pattern đơn giản)

Các indicator này không dùng được pattern `feat > threshold / feat < threshold / crossed(feat, threshold)` vì entry/exit phức tạp hơn.

| Feat | Lý do | Entry | Exit | File |
|------|-------|-------|------|------|
| **`sar(high, low, 0.02, 0.2)`** | Exit = `crossed(close, sar)` không phải `crossed(sar, threshold)` | `sar < close` → long; `sar > close` → short | `crossed(close, sar)` | ✅ `SF_SAR_15min.py` |
| **`mama(close, 0.5, 0.05)`** | 2 outputs (mama, fama), crossover | `mama > fama` → long; `mama < fama` → short | `crossed(mama, fama)` | ✅ `SF_MAMA_15min.py` |
| **`ht_trendline(close)`** | Exit = `crossed(close, ht_trendline)` | `close > ht_trendline` → long | `crossed(close, ht_trendline)` | ✅ `SF_HT_TRENDLINE_15min.py` |
| **`bop(open, high, low, close)`** | Entry asymmetric (0.5 / -0.5), exit khác threshold | `bop > 0.5` → long; `bop < -0.5` → short | `crossed(bop, 0)` | ✅ `SF_BOP_15min.py` |
| **`obv(close, volume)`** | Dùng rolling_mean, không phải threshold cố định | `obv > rolling_mean(obv, 20)` → long | `crossed(obv, rolling_mean(obv, 20))` | ✅ `SF_OBV_15min.py` |
| **`mfi(high, low, close, volume, 14)`** | Mean reversion | `mfi < 20` → long; `mfi > 80` → short | `crossed(mfi, 50)` | ✅ `SF_MFI_15min.py` |
| **`cmf(high, low, close, volume, 20)`** | Mean reversion | `cmf < -0.3` → long; `cmf > 0.3` → short | `crossed(cmf, 0)` | ✅ `SF_CMF_15min.py` |
| **`ad(high, low, close, volume)`** | Dùng rolling_mean | `ad > rolling_mean(ad, 20)` → long | `crossed(ad, rolling_mean(ad, 20))` | ✅ `SF_AD_15min.py` |
| **`bbands(close, 20, 2)`** | Mean reversion | `close < lower_band` → long; `close > upper_band` → short | `crossed(close, middle_band)` | ✅ `SF_BBANDS_15min.py` |
| **`price_z(close, 20)`** | Mean reversion | `price_z < -2` → long; `price_z > 2` → short | `abs(price_z) < 1` | ✅ `SF_PRICE_Z_15min.py` |
| **`rolling_zscore(close, 20)`** | Mean reversion | `rolling_zscore < -2` → long; `> 2` → short | `abs(rolling_zscore) < 1` | ✅ `SF_ROLLING_ZSCORE_15min.py` |
| **`donchian_upper/low(high/low, 20)`** | Breakout pattern | `close > donchian_upper` → long | `crossed(close, donchian_upper) \| crossed(close, donchian_lower)` | ✅ `SF_DONCHIAN_15min.py` |
| **`engulfing_pattern(open, high, low, close)`** | Dùng `== 1` / `== -1`, không phải threshold | `engulfing == 1` → long; `engulfing == -1` → short | time stop (5 bars) | ✅ `SF_ENGULFING_15min.py` |
| **`morning_star(open, high, low, close, 10)`** | 3-bar bullish reversal | `morning_star == 1` → long | time stop (5 bars) | ✅ `SF_MORNING_STAR_15min.py` |
| **`evening_star(open, high, low, close, 10)`** | 3-bar bearish reversal | `evening_star == 1` → short | time stop (5 bars) | ✅ `SF_EVENING_STAR_15min.py` |
| **`hammer(open, high, low, close)`** | Single-bar bullish reversal | `hammer == 1` → long | time stop (5 bars) | ✅ `SF_HAMMER_15min.py` |
| **`shooting_star(open, high, low, close)`** | Single-bar bearish reversal | `shooting_star == 1` → short | time stop (5 bars) | ✅ `SF_SHOOTING_STAR_15min.py` |
| **`marubozu(open, high, low, close)`** | No shadow → directional strength | `marubozu == 1` → long; `marubozu == -1` → short | time stop (5 bars) | ✅ `SF_MARUBOZU_15min.py` |
| **`three_white_soldiers(open, high, low, close, 10)`** | 3-bar bullish confirmation | `three_white_soldiers == 1` → long | time stop (5 bars) | ✅ `SF_3WHITE_SOLDIERS_15min.py` |
| **`three_black_crows(open, high, low, close, 10)`** | 3-bar bearish confirmation | `three_black_crows == 1` → short | time stop (5 bars) | ✅ `SF_3BLACK_CROWS_15min.py` |
| **`rolling_rank(close, 20)`** | Mean reversion | `rolling_rank < 0.1` → long; `> 0.9` → short | `abs(rolling_rank - 0.5) < 0.2` | ✅ `SF_ROLLING_RANK_15min.py` |
| **`rolling_argmax(high, 20)`** | Mean reversion + time stop | `rolling_argmax >= 10` → long; `rolling_argmax == 0` → short | time stop (5 bars) | ✅ `SF_ROLLING_ARGMAX_15min.py` |
| **`rolling_argmin(low, 20)`** | Mean reversion + time stop | `rolling_argmin == 0` → long; `rolling_argmin >= 10` → short | time stop (5 bars) | ✅ `SF_ROLLING_ARGMIN_15min.py` |

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

## Template code cho Single-Feat Alpha (Trend Following)

```python
class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        feat = self.feat.<indicator>(<args>)

        long_setup = feat > <threshold>
        short_setup = feat < <threshold>
        exit_setup = self.op.crossed(feat, <threshold>)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
```

---

## Lưu ý khi thiết kế Single-Feat Alpha

1. **Trend following**: Dùng `feat > threshold` → long, `feat < threshold` → short (không phải mean reversion)
2. **Exit duy nhất**: `self.op.crossed(feat, threshold)` — exit khi feat cắt threshold từ cả 2 hướng
3. **Session gating**: Luôn thêm `position_open_ranges`, `position_close_ranges`, `position_close_after_n_candles` cho VNFuture
4. **Không cần class attributes**: Threshold hardcode trực tiếp trong logic
5. **Không cần ATR / stop-loss**: Pattern đơn giản, exit duy nhất bằng crossed
6. **Sinh file mới**: Dùng `python tools/gen_single_feat.py <indicator> <feat_call> <threshold> [--data <vars>]`

---

## Kế hoạch triển khai

### Phase 1: Kiểm tra & Đánh giá
- [ ] **P1.1** — Kiểm tra kết quả backtest 10 strategy trên web
  - CAGR còn -100% không? Win rate? Sharpe? Số lệnh?
  - Nếu CAGR vẫn -100% → cần sửa pattern (thêm ADX filter, return_roll, volume confirmation)
  - Nếu CAGR cải thiện → gen tiếp các phase sau

### Phase 2: Gen Tier 1B (19 indicators — custom logic)
- [x] **P2.1** — `sar(high, low, 0.02, 0.2)` — `SF_SAR_15min.py`
- [x] **P2.2** — `mama(close, 0.5, 0.05)` — `SF_MAMA_15min.py`
- [x] **P2.3** — `ht_trendline(close)` — `SF_HT_TRENDLINE_15min.py`
- [x] **P2.4** — `bop(open, high, low, close)` — `SF_BOP_15min.py`
- [x] **P2.5** — `obv(close, volume)` — `SF_OBV_15min.py`
- [x] **P2.6** — `mfi(high, low, close, volume, 14)` — `SF_MFI_15min.py`
- [x] **P2.7** — `cmf(high, low, close, volume, 20)` — `SF_CMF_15min.py`
- [x] **P2.8** — `ad(high, low, close, volume)` — `SF_AD_15min.py`
- [x] **P2.9** — `bbands(close, 20, 2)` — `SF_BBANDS_15min.py`
- [x] **P2.10** — `price_z(close, 20)` — `SF_PRICE_Z_15min.py`
- [x] **P2.11** — `rolling_zscore(close, 20)` — `SF_ROLLING_ZSCORE_15min.py`
- [x] **P2.12** — `donchian_upper/low(high/low, 20)` — `SF_DONCHIAN_15min.py`
- [x] **P2.13** — Candlestick patterns (engulfing, morning_star, evening_star, hammer, shooting_star, marubozu, 3WS, 3BC) — `SF_ENGULFING_15min.py`, `SF_MORNING_STAR_15min.py`, `SF_EVENING_STAR_15min.py`, `SF_HAMMER_15min.py`, `SF_SHOOTING_STAR_15min.py`, `SF_MARUBOZU_15min.py`, `SF_3WHITE_SOLDIERS_15min.py`, `SF_3BLACK_CROWS_15min.py`
- [x] **P2.14** — `rolling_rank(close, 20)` — `SF_ROLLING_RANK_15min.py`
- [x] **P2.15** — `rolling_argmax(high, 20)` — `SF_ROLLING_ARGMAX_15min.py`
- [x] **P2.16** — `rolling_argmin(low, 20)` — `SF_ROLLING_ARGMIN_15min.py`

### Phase 3: Gen Tier 2 (14 indicators — cần filter)
- [ ] **P3.1** — `ema(close, 20)` + price cross
- [ ] **P3.2** — `sma(close, 20)` + price cross
- [ ] **P3.3** — `macd(close, 12, 26, 9)` — histogram đổi dấu
- [ ] **P3.4** — `ppo(close, 12, 26, 9)` — signal line cross
- [ ] **P3.5** — `momemtum(close, 10)` — threshold > 0
- [ ] **P3.6** — `roc(close, 10)` — threshold > 0
- [ ] **P3.7** — `trix(close, 15)` — signal cross
- [ ] **P3.8** — `ultosc(high, low, close, 7, 14, 28)` — threshold
- [ ] **P3.9** — `adx(high, low, close, 14)` — +DI/-DI direction
- [ ] **P3.10** — `dx(high, low, close, 14)` — price direction
- [ ] **P3.11** — `atr(high, low, close, 14)` — price direction
- [ ] **P3.12** — `volume_z(volume, 20)` — price move confirmation
- [ ] **P3.13** — `correl(close, vn30_close, 20)` — cross-asset
- [ ] **P3.14** — `beta(close, vn30_close, 20)` — relative risk

### Phase 4: Nâng cấp filters (từ vietnam_market_characteristics.md)
- [ ] **P4.1** — Thêm universal ADX filter (`ADX > 22` cho entry, `ADX < 18` cho exit)
- [ ] **P4.2** — Thêm return_roll momentum confirmation
- [ ] **P4.3** — Thêm volume confirmation (`volume > SMA(vol, 20)`)
- [ ] **P4.4** — Thêm consecutive loss protection (dừng sau 3 lỗ)

### Phase 5: Multi-feat thesis
- [ ] **P5.1** — Thiết kế thesis kết hợp Tier 1A + Tier 1B + Tier 2
- [ ] **P5.2** — Gen và submit batch multi-feat

### Workflow mỗi phase
```
1. Gen file mới
2. python tools/submit_all.py --test     # test 1 variant
3. python tools/submit_all.py            # submit full batch
4. Kiểm tra kết quả trên web
5. git add + git commit + git push       # commit thay đổi
```