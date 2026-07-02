# Vietnam Market Characteristics — Strategy Design Guide

> Tài liệu tham chiếu về đặc thù thị trường Việt Nam và cách ánh xạ thành thiết kế chiến lược định lượng trên XNOQuant.
> Đọc sau `README.md` và `template_example/strategy_framework.md`, trước khi code.

---

## 1. Tổng quan thị trường Việt Nam

| Đặc điểm | Mô tả | Hệ quả giao dịch |
|----------|-------|------------------|
| **Retail chiếm 80-90%** | Nhà đầu tư cá nhân áp đảo, thiếu chuyên nghiệp | Herding, FOMO, panic sell tạo extreme moves |
| **Đòn bẩy phái sinh 1:6-1:8** | Margin call xảy ra nhanh, cascade effect | Forced selling/buying tạo momentum mạnh |
| **Dòng tiền luân chuyển nhanh** | Retail chuyển hướng theo tin tức hàng ngày | Regime change thường xuyên, trend kéo dài 2-3 phiên |
| **Thanh khoản tập trung** | VN30F1M là sản phẩm phái sinh chính, thanh khoản tốt nhất | Spread thấp, dễ vào lệnh size lớn |
| **Thiếu institutional flow ổn định** | Không có pension fund, ETF flow như发达市场 | Không có "smart money" ổn định để follow |
| **Tin tức nội tại chi phối** | KQKD, news, policy thay đổi đột ngột | Gap risk cao, cần risk management chặt |

---

## 2. Đặc thù phái sinh VN30F1M

| Đặc thù | Chi tiết | Ứng dụng Strategy |
|---------|----------|-------------------|
| **T+0 (same-day trading)** | Mua bán trong ngày không giới hạn số lần | Scalping, intraday strategies khả thi |
| **Giờ giao dịch** | Sáng 8:45-11:30, Chiều 13:00-14:45 | Session-based strategies (thesis 07) |
| **ATC 14:30-14:45** | Khớp lệnh định kỳ đóng cửa, dễ bị manipulation | Close position trước 14:20 |
| **Basis volatility** | Chênh lệch futures-cash biến động mạnh | Cross-market strategies (thesis 05) |
| **Không có circuit breaker** | Giá có thể biến động >3% trong 1 nến | Trend momentum mạnh, mean reversion rủi ro |
| **Pre-cash (8:45-9:00)** | Khớp lệnh liên tục trước cash market mở cửa | Volume thấp, spread rộng → tránh trade |
| **Lunch break (11:30-13:00)** | Thị trường futures vẫn giao dịch nhưng volume thấp | Dead zone → đóng position, avoid noise |
| **Weekend gap** | Giá mở cửa sáng thứ 2 thường gap so với thứ 6 | Position management cuối tuần |

---

## 3. Mapping: Đặc thù → Thiết kế Strategy

Bảng dưới đây là **core reference** cho mọi quyết định thiết kế strategy. Mỗi đặc thù thị trường được ánh xạ thành signal, entry rule, exit rule, và danh sách templates áp dụng.

### 3.1. Retail Herding & Momentum

```
# Đặc thù: Retail chase trend khi giá breakout
# Cơ chế: FOMO → mua đuổi đỉnh / panic → bán tháo đáy
# Hệ quả: Trend kéo dài 3-5 nến sau breakout
```

| Signal | Entry Rule | Exit Rule | Templates |
|--------|-----------|-----------|-----------|
| `ROC(close, fast) > threshold` + `volume > SMA(vol, N)` | Long: ADX > 22 & return_roll > 0 | return_roll < 0 hoặc ADX < 18 | momentum_vol, breakout_vol, trend_adx |
| `ROC(close, fast) < -threshold` + volume surge | Short: ADX > 22 & return_roll < 0 | return_roll > 0 | momentum_cascade, breakout |
| `close > BBands_upper` | KHÔNG SHORT (retail còn đuổi) | — | — |
| `close < BBands_lower` | KHÔNG LONG (panic chưa hết) | — | — |

### 3.2. Margin Call Cascade

```
# Đặc thù: Margin call → forced selling cascade
# Cơ chế: Giá giảm → margin call → forced sell → giá giảm tiếp
# Hệ quả: Volume spike + price drop > 1% trong 1-2 nến, hồi phục nhanh sau đó
```

| Signal | Entry Rule | Exit Rule | Templates |
|--------|-----------|-----------|-----------|
| `volume > SMA(vol, N) * 2` AND `ROC(close, 1) < -0.01` | Short tại nến thứ 2 của cascade | return_roll > 0 hoặc VBS < SMA(vol, VBS)/2 | momentum_cascade, volume_surge |
| `OI giảm mạnh` (position unwinding) | Short: xác nhận volume + price drop | Close khi OI ổn định | volume_oi |
| `Basis mở rộng` (futures giảm nhanh hơn cash) | Short: basis < -2σ | Basis quay về 0 | cross_basis |

### 3.3. Basis Manipulation

```
# Đặc thự: Futures-cash basis bị đẩy để trap retail
# Cơ chê: Market maker đẩy basis rộng → retail chase → đảo chiều
# Hệ quả: Basis > 2σ thường precede reversal
```

| Signal | Entry Rule | Exit Rule | Templates |
|--------|-----------|-----------|-----------|
| `basis = close - VN30_close` | Short: basis > 2σ & stochastic > 80 | basis về MA(20) | cross_relative |
| `basis < -2σ` & VN30 đang tăng | Long: basis < -2σ & stochastic < 20 | basis về MA(20) | cross_relative |

### 3.4. Session Microstructure

| Session (UTC) | Giờ VN | Hành vi | Chiến lược | Position Sizing |
|---------------|--------|---------|------------|-----------------|
| 01:45-02:00 | 8:45-9:00 | Pre-cash, volume thấp | AVOID | 0 |
| 02:00-04:30 | 9:00-11:30 | Trending mạnh nhất, volume cao | Full momentum | 1.0 |
| 04:30-06:00 | 11:30-13:00 | Lunch dead zone | Close positions | 0 |
| 06:00-07:30 | 13:00-14:30 | Afternoon continuation | Trend hoặc mean revert | 0.75 |
| 07:30-07:45 | 14:30-14:45 | ATC manipulation | FLAT bắt buộc | 0 |

### 3.5. Calendar Effects

| Effect | Mô tả | Action |
|--------|-------|--------|
| **Thứ 2 đầu tuần** | Price gap from weekend, retail quyết định TUẦN MỚI | Avoid new positions in first 30min |
| **Thứ 6 cuối tuần** | Position squaring, giảm volume chiều | Take profit, giảm size |
| **Expiry week** (thứ 5 tuần thứ 3) | Basis biến động mạnh, volume tăng | Adjust threshold +0.5σ |
| **Cash dividend date** | Cash adjustment ảnh hưởng VN30 | Tránh cross-market |
| **Holiday** (Tết, 30/4, 2/9) | Volume giảm 50-70%, spread rộng | Flat khuyến nghị |

---

## 4. Parameter Guidelines theo chế độ thị trường

| Chế độ | ADX | return_roll threshold | ROC threshold | Position | Volume filter | Templates phù hợp |
|--------|:---:|:---------------------:|:-------------:|:--------:|:-------------:|-------------------|
| **Trending mạnh** | > 25 | > 0 (any) | > 0.3% | 1.0 | Không cần | momentum_vol, trend_macd, breakout |
| **Trending yếu** | 20-25 | > 0 (any) | > 0.5% | 0.5 | volume > SMA(20) | trend_adx, momentum_quantile |
| **Ranging** | < 20 | KHÔNG TRADE | — | 0 | — | — |
| **Volatility cao** (ATR > 2%) | > 22 | > 0 | > 0.3% | 0.75 | volume > SMA(14) | breakout_range, volatility |
| **Volatility thấp** (ATR < 0.5%) | > 20 | > threshold_N | > 0.5% | 0.5 | volume > SMA(20) | momentum_quantile, volume_surge |
| **Gap day** (open > 1% away prev close) | — | — | — | 0 | — | Chờ 30 phút |

**Nguyên tắc vàng:** Nếu ADX < 20, KHÔNG trade. Đây là nguyên nhân số 1 khiến Sharpe thấp.

---

## 5. Sharpe Optimization Rules

Các rule **bắt buộc** để hướng tới Sharpe ≥ 2.0-2.5:

### 5.1. Universal ADX Trend Filter
```python
# Áp dụng cho MỌI strategy
trend_filter = self.feat.ADX(self.data.pv_high, self.data.pv_low, self.data.pv_close, window=ADX_WINDOW)
entry_condition &= (trend_filter > 22)
exit_condition |= (trend_filter < 18)
```

### 5.2. return_roll Momentum Smoothing
```python
# Bắt buộc: chỉ vào lệnh khi momentum đã confirmed
return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
return_roll = self.feat.rolling_mean(return_1, window=RETURN_ROLL_WINDOW)
long_entry &= (return_roll > 0)
short_entry &= (return_roll < 0)
# Asymmetric exit (tighter exit)
long_exit |= (return_roll < 0)   # Exit khi momentum chết
short_exit |= (return_roll > 0)
```

### 5.3. Volume Confirmation
```python
# Bắt buộc: signal cần khối lượng xác nhận
vol_ma = self.feat.SMA(self.data.pv_volume, window=VOL_WINDOW)
entry_condition &= (self.data.pv_volume > vol_ma)  # Volume > SMA
```

### 5.4. Consecutive Loss Protection
```python
# Dừng trade sau 3 lỗ liên tiếp
consecutive_loss = self.op.fillna(self.op.consecutive_true(self.op.crossed_above(self.op.pct_change(PnL, periods=1), 0), periods=1), value=0)
entry_condition &= (consecutive_loss < 3)
```

### 5.5. Asymmetric Exit
```python
# Entry strict, exit loose
long_entry = strict_signal AND return_roll > 0
long_exit = loose_signal OR return_roll < 0 OR ADX < 18
# Không cho phép trade chờ đợi — cut loss nhanh
```

### 5.6. Session-Based Position Management
```python
# Lunch dead zone: close positions
position_close_after_n_candles = SESSION_CANDLES[tf]
# Tránh ATC: close trước 14:20 (UTC 07:20)
position_close_ranges = ["07:20-07:45"]
```

---

## 6. Tham số cụ thể cho từng timeframe

| Timeframe | RETURN_ROLL_WINDOW | ADX_WINDOW | VOL_WINDOW | SESSION_CANDLES | RETURN_THRESH |
|:---------:|:------------------:|:----------:|:----------:|:---------------:|:-------------:|
| 5min | 3 | 7 | 14 | 72 | 0.0001 |
| 15min | 5 | 10 | 20 | 24 | 0.0002 |
| 30min | 8 | 14 | 26 | 12 | 0.0003 |
| 60min | 14 | 21 | 34 | 6 | 0.0005 |

---

## 7. Risk Management Rules

| Rule | Mô tả | Cài đặt |
|------|-------|---------|
| **Max loss per trade** | Không để thua lỗ > 2% tài khoản 1 lệnh | Stop-loss implied by exit logic |
| **Max consecutive losses** | Dừng trade nếu 3 lệnh liên tiếp thua | `consecutive_loss < 3` |
| **Weekend gap protection** | Flat trước 14:45 thứ 6 | `position_close_ranges` cho thứ 6 |
| **Pre-cash avoidance** | Không trade 8:45-9:00 (volume thấp, spread rộng) | `position_open_ranges` bỏ qua pre-cash |
| **ATC avoidance** | Không giữ position qua ATC 14:30-14:45 | Close trước 14:20 |
| **Lunch dead zone** | Đóng position 11:30-13:00 | `position_close_ranges` = ["04:30-06:00"] |
| **Expiry week adjustment** | Tăng threshold 0.5σ trong tuần đáo hạn | Manual adjustment |
| **Basis squeeze** | Nếu basis > 3σ, giảm size 50% | Conditional sizing |

---

## 8. Regime Detection & Adaptation

```python
# Xác định chế độ thị trường tự động
adx = self.feat.ADX(high, low, close, window=ADX_WINDOW)
vol_ratio = self.data.pv_volume / self.feat.SMA(self.data.pv_volume, window=VOL_WINDOW)

if adx[-1] > 25:
    regime = "strong_trend"
    position_size = 1.0
    roc_threshold = 0.003
elif adx[-1] > 20:
    regime = "weak_trend"
    position_size = 0.5
    roc_threshold = 0.005
else:
    regime = "ranging"
    position_size = 0.0  # KHÔNG TRADE
```

---

## 9. Debug Checklist

Khi strategy không đạt Sharpe target, kiểm tra theo thứ tự:

| # | Check | Fix |
|---|-------|-----|
| 1 | ADX filter có hoạt động không? | Universal ADX > 22 cho entry |
| 2 | return_roll filter đúng chiều? | Long: > 0, Short: < 0 |
| 3 | Volume confirmation có không? | Volume > SMA(VOL_WINDOW) |
| 4 | Entry threshold có quá thấp? | ROC > 0.3-0.5% |
| 5 | Exit có quá chậm? | return_roll < 0 → exit ngay |
| 6 | Có session timing không? | Close lunch, close trước ATC |
| 7 | Consecutive loss protection? | Dừng sau 3 lỗ |
| 8 | Position bounds [-1, +1]? | self.set_positions đúng |
| 9 | Look-ahead bias? | Chỉ dùng data tại thời điểm signal |
| 10 | Noise trade trong ranging market? | ADX < 20 → không trade |

---

## 10. Summary: Công thức cho Sharpe ≥ 2.0

```
Sharpe ≥ 2.0 = 
  (ADX > 22)                            # Filter noise
  + (return_roll > 0)                   # Confirm momentum
  + (volume > SMA)                      # Volume confirmation
  + (ROC > 0.3%)                        # Avoid whipsaw
  + Asymmetric exit (return_roll < 0)   # Cut loss fast
  + Session gating (close lunch, pre-ATC)  # Avoid manipulation zones
  + Consecutive loss protection (3 max) # Preserve capital
```

Thiếu bất kỳ thành phần nào → Sharpe khó > 1.5.
