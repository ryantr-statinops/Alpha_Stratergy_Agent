# Thesis 13: CMF + Bollinger Squeeze Breakout

**ID:** HYP-13-CMF-SQZ  
**Thesis:** 13  
**Folder:** `thesis_13_cmf_squeeze_breakout`  
**Target:** Thị trường VN30F1M — tận dụng retail herding sau squeeze + CMF confirmation.

---

## 1. Core Logic

### Ingredients

| Thành phần | Function | Vai trò |
|-----------|----------|---------|
| **Bollinger Squeeze** | `self.feat.bbands` | Phát hiện vùng tích lũy (bb_width thấp nhất N phiên) |
| **CMF** | `self.feat.cmf` | Xác định hướng dòng tiền (CMF > 0 = accumulation, < 0 = distribution) |
| **ADX** | `self.feat.adx` | Universal trend filter: ADX > 22 để trade breakout |
| **Volume** | `self.data.pv_volume` | Confirmation: volume > SMA(vol, window) |
| **ATR** | `self.feat.atr` | Stop-loss + trailing exit |

### Pipeline

```
Layer 1: self.data → close, high, low, volume
Layer 2: self.feat → bb_width, cmf, adx, atr, sma
Layer 3: logic entry/exit với mask + assert
Layer 4: self.set_positions(Exit → Long → Short)
```

---

## 2. Các Variants

### T13-A: CMF + Squeeze Breakout (core)

```
Entry Long:
  - bb_width đang ở mức thấp nhất 20 phiên (squeeze zone)
  - cmf > 0 (dòng tiền vào)
  - adx > 22 (xu hướng có)
  - volume > sma_volume (xác nhận khối lượng)
  - close > sma_20 (giá trên MA ngắn)

Entry Short:
  - bb_width đang ở mức thấp nhất 20 phiên
  - cmf < 0 (dòng tiền ra)
  - adx > 22
  - volume > sma_volume
  - close < sma_20

Exit Long: kf_z > 0.2 | adx < adx_exit | atr_stop_long
Exit Short: kf_z < -0.2 | adx < adx_exit | atr_stop_short
```

Trong đó `kf_z` dùng Kalman proxy (`self.feat.sma(10)` + residual z-score) làm early exit indicator.

### T13-B: CMF + Pullback

- Chỉ trade sau squeeze + breakout đã xảy ra, chờ pullback về SMA20.
- Long: giá hồi về SMA20 nhưng vẫn trên SMA50, CMF vẫn > 0.
- Short: giá hồi về SMA20 nhưng vẫn dưới SMA50, CMF vẫn < 0.

### T13-C: CMF Reversal

- Trade khi squeeze đã hết (bb_width thoát khỏi đáy 20 phiên) và CMF quay đầu
- Long: CMF từ âm chuyển dương + giá breakout lên trên SMA20
- Short: CMF từ dương chuyển âm + giá breakout xuống dưới SMA20

---

## 3. Parameter Defaults

| Parameter | T13-A | T13-B | T13-C | Mô tả |
|-----------|:-----:|:-----:|:-----:|-------|
| bb_window | 20 | 20 | 20 | Cửa sổ Bollinger |
| bb_nbdev | 2 | 2 | 2 | Std dev cho BB |
| cmf_window | 20 | 20 | 20 | Cửa sổ CMF |
| adx_min | 22 | 22 | 22 | ADX tối thiểu để entry |
| adx_exit | 18 | 18 | 18 | ADX để exit |
| atr_mult | 2.5 | 2.5 | 2.5 | Hệ số ATR stop |
| kf_window | 10 | 10 | 10 | Cửa sổ Kalman proxy |
| kf_z_exit | 0.5 | 0.5 | 0.5 | Ngưỡng z-score exit |

---

## 4. Null Hypothesis

Nếu không dùng CMF filter, squeeze breakout không có directional bias → win rate ~50%, Sharpe < 0.5.

## 5. Alternative Hypothesis

CMF > 0 (dòng tiền vào) + squeeze breakout → Long sẽ có win rate ≥ 58% và Sharpe ≥ 1.2.

## 6. Metrics

| Metric | Target | Weight |
|--------|:------:|:------:|
| Sharpe Ratio | ≥ 1.2 | HIGH |
| Win Rate | ≥ 55% | MEDIUM |
| Profit Factor | ≥ 1.5 | MEDIUM |
| Max Drawdown | ≥ -40% | HIGH |
| Avg Trades/Week | ≥ 3 | LOW |

---

## 7. Hard Rules Checklist

- [x] ADF filter cho entry (không trade noise khi ADX < 22)
- [x] Volume confirmation
- [x] Asymmetric exit (entry strict, exit loose)
- [x] Signal mask: `long_signal = long_setup & (~exit_long)`
- [x] Thứ tự Exit → Long → Short
- [x] `assert not (long_signal & short_signal).any()`
- [x] Neutral zone giữa entry và exit threshold (kf_z_entry=1.5, kf_z_exit=0.5)
- [ ] Cần validate cross-timeframe consistency