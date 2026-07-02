# Alpha Ideas — 5 New Strategy Concepts (Vietnam Derivatives Focus)

> **Session:** 2026-07-02 — Fresh brainstorm, no legacy thesis constraints
> **Core principle:** Leverage Vietnam market microstructure (80-90% retail, 1:6-1:8 leverage, session quirks, unique futures data)

---

## Idea 1: "Cascade Catcher" — Margin Call Domino

### Concept
VN30F1M margin leverage 1:6-1:8 means a 2% drop triggers margin calls. Forced selling cascades create predictable short opportunities lasting 2-5 candles (15-30 min) before exhaustion.

### Alpha Signal
```
Short:
  OI_drop = (OI - OI.shift(1)) / OI.shift(1) < -0.01   # OI giảm > 1%
  vol_spike = matched_volume > SMA(matched_volume, 20) * 2
  price_drop = ROC(close, 1) < -0.005
  cascade = OI_drop AND vol_spike AND price_drop
  entry = cascade AND (return_roll < -threshold) AND (adx > 22)

Long (cascade exhaustion):
  vol_collapse = matched_volume < SMA(matched_volume, 20) * 0.5
  price_stabilize = ROC(close, 1) > -0.001 AND ROC(close, 1) < 0.001
  exhaustion = vol_collapse AND price_stabilize
  entry = exhaustion AND return_roll_vừa chéo lên trên 0
```

### Key Data Fields
- `fut_matched_volume_vn30f1m_1d`
- `fut_open_interest_vn30f1m_1d`
- `pv_close`, `pv_high`, `pv_low`

### Optimal Timeframe
**5-15 min** — cascade xảy ra nhanh, 30-60min bỏ lỡ điểm vào

### Parameter Variants
| Variant | OI Drop | Vol Spike | ROC Threshold | Return_Roll Window |
|---------|:-------:|:---------:|:-------------:|:------------------:|
| Aggressive | > 0.5% | > 1.5x | < -0.3% | 3 |
| Standard | > 1% | > 2x | < -0.5% | 5 |
| Conservative | > 2% | > 3x | < -1% | 5 |

### Risk Notes
- Không catch falling knife — chờ OI đã drop mới vào
- Exit ngay khi vol trở về baseline
- Lunch zone: không trade cascade gần 11:30

---

## Idea 2: "Basis Bounce" — Futures vs Cash Reversion

### Concept
Retail FOMO đẩy basis (futures - VN30 index) ra xa giá trị fair. Khi basis ở extreme + volume đuối, reversion mạnh về mean.

### Alpha Signal
```
basis = pv_close - pv_vn30_close
basis_zscore = rolling_zscore(basis, 20)
basis_vol = rolling_std(basis, 20)

Short:
  basis_zscore > 2.5                      # basis quá rộng
  AND matched_volume < SMA(matched_volume, 20)  # volume đuối → hết đà
  AND stoch_K < 20                        # overbought

Long:
  basis_zscore < -2.5
  AND matched_volume < SMA(matched_volume, 20)
  AND stoch_K > 80                        # oversold

Exit:
  basis_zscore về trong khoảng [-1, 1]
  OR basis quay về SMA(basis, 20)
```

### Key Data Fields
- `pv_close` (futures price)
- `pv_vn30_close` (VN30 index)
- `fut_matched_volume_vn30f1m_1d`

### Optimal Timeframe
**30-60 min** — basis divergence cần thời gian hình thành

### Parameter Variants
| Variant | Z-score Entry | Basis Window | Stoch Threshold |
|---------|:------------:|:------------:|:---------------:|
| Aggressive | 2.0 | 14 | 30/70 |
| Standard | 2.5 | 20 | 20/80 |
| Conservative | 3.0 | 34 | 10/90 |

### Risk Notes
- Không trade expiry week (basis biến động bất thường)
- Kiểm tra cash dividend dates — basis bị nhiễu
- Session: morning session volume cao nhất, basis tin cậy nhất

---

## Idea 3: "Lunch Gap" — Pre/Post Lunch Mean Reversion

### Concept
Lunch break (11:30-13:00 VN = 04:30-06:00 UTC) futures vẫn giao dịch với volume rất thấp. Giá dễ bị đẩy ảo. Phiên chiều mở cửa thường reversion mạnh trong 3-5 nến đầu.

### Alpha Signal
```
lunch_move = (close_13:00 - close_11:30) / close_11:30
lunch_range = ATR(close, timeperiod=14)  # daily ATR for reference

Long (lunch gap down):
  lunch_move < -0.5 * lunch_range        # giá giảm quá mức trong lunch
  AND matched_volume < SMA_20 * 0.3      # volume lunch cực thấp → giá ảo

Short (lunch gap up):
  lunch_move > 0.5 * lunch_range
  AND matched_volume < SMA_20 * 0.3

Entry timing: exactly 13:00-13:15 (06:00-06:15 UTC)
Exit: 13:15-13:30 hoặc str开头 profit 0.5*lunch_range
```

### Key Data Fields
- `pv_close`, `fut_matched_volume_vn30f1m_1d`
- Session-specific: chỉ active trong window 06:00-06:15 UTC

### Optimal Timeframe
**5 min** — trade nhanh, 3-5 nến là kết thúc

### Parameter Variants
| Variant | Lunch Move Threshold | Exit Target | Stop Loss |
|---------|:-------------------:|:-----------:|:---------:|
| Aggressive | 0.3x ATR | 0.3x ATR | 0.5x ATR |
| Standard | 0.5x ATR | 0.5x ATR | 0.8x ATR |
| Conservative | 0.8x ATR | 0.5x ATR | 1.0x ATR |

### Risk Notes
- Chỉ trade khi lunch volume thực sự thấp (< 30% SMA)
- Không trade nếu lunch move do news gap (khác với thin market noise)
- Set cứng stop loss — lunch gap đôi khi không revert

---

## Idea 4: "Whale Footprint" — Average Trade Size Surge

### Concept
`avg_trade_size = matched_value / matched_volume`. Khi avg_trade tăng đột biến, "cá mập" đang giao dịch. Nếu giá chưa phản ứng, họ đang tích lũy/phân phối âm thầm → breakout imminent.

### Alpha Signal
```
avg_trade = fut_matched_value_vn30f1m_1d / fut_matched_volume_vn30f1m_1d
avg_trade_sma = SMA(avg_trade, 20)
avg_trade_sigma = rolling_std(avg_trade, 20)

whale_active = avg_trade > avg_trade_sma + 2 * avg_trade_sigma
price_range = (rolling_max(close, 10) - rolling_min(close, 10)) / rolling_min(close, 10)
price_compressed = price_range < 0.01  # under 1% range, 10 candles

Long:
  whale_active
  AND price_compressed
  AND return_roll > 0
  AND volume_breakout = matched_volume > SMA(matched_volume, 20) * 1.5

Short:
  whale_active
  AND price_compressed
  AND return_roll < 0
  AND volume_breakout

Exit:
  close breakout of SEA(compression_range) hoặc return_roll đảo chiều
```

### Key Data Fields
- `fut_matched_value_vn30f1m_1d`
- `fut_matched_volume_vn30f1m_1d`
- `pv_close`, `pv_high`, `pv_low`

### Optimal Timeframe
**15-30 min** — cần đủ nến để tính avg_trade SMA. 60min cũng được nhưng ít tín hiệu hơn.

### Parameter Variants
| Variant | Whale Threshold | Compression Lookback | Volume Breakout |
|---------|:--------------:|:--------------------:|:---------------:|
| Aggressive | 1.5σ | 7 | 1.5x |
| Standard | 2.0σ | 10 | 2.0x |
| Conservative | 2.5σ | 14 | 2.5x |

### Risk Notes
- Tín hiệu thưa (whale active không xảy ra hàng ngày)
- Cần kết hợp với hướng breakout thực tế (không trade ngược)
- Giá trị thỏa thuận (agreed) là nhiễu — nên dùng matched value/volume

---

## Idea 5: "Retail Exhaustion" — Volume Spike Reversal

### Concept
Retail chiếm 80-90% khối lượng. Khi volume đột biến + nến dài, đó là đỉnh điểm của FOMO (long) hoặc panic (short). Retail đã all-in → không còn lực đẩy tiếp → reversal.

### Alpha Signal
```
vol_ratio = pv_volume / SMA(pv_volume, 14)
candle_body = abs(pv_close - pv_open)
atr = ATR(pv_high, pv_low, pv_close, timeperiod=14)

vol_spike = vol_ratio > 3
big_candle = candle_body > 1.5 * atr

Long (short panic exhaustion):
  vol_spike AND big_candle
  AND close < rolling_quantile(close, 20, 0.10)  # giá ở extreme thấp
  AND return_roll > -0.005                        # không còn giảm mạnh
  AND open < close                                # nến xanh (đã hồi phục)

Short (long FOMO exhaustion):
  vol_spike AND big_candle
  AND close > rolling_quantile(close, 20, 0.90)  # giá ở extreme cao
  AND return_roll < 0.005                         # không còn tăng mạnh
  AND open > close                                # nến đỏ (đã suy yếu)

Exit:
  close quay về SMA(close, 20)
  hoặc sau 3-5 nến take profit
```

### Key Data Fields
- `pv_close`, `pv_open`, `pv_high`, `pv_low`, `pv_volume`

### Optimal Timeframe
**5-15 min** — panic/FOMO xảy ra trong vài nến, 60min quá trễ

### Parameter Variants
| Variant | Vol Spike | Big Candle | Quantile Extreme |
|---------|:---------:|:----------:|:----------------:|
| Aggressive | > 2.5x | > 1.2x ATR | 0.15/0.85 |
| Standard | > 3.0x | > 1.5x ATR | 0.10/0.90 |
| Conservative | > 4.0x | > 2.0x ATR | 0.05/0.95 |

### Risk Notes
- Nguy hiểm nhất: catch falling knife (volume spike trong downtrend mạnh chưa kết thúc)
- Luôn chờ nến xác nhận — trade nến sau spike, không trade nến spike
- Kết hợp ADX: nếu ADX > 30 thì đà quá mạnh, chờ thêm

---

## Quick Reference — TF Suitability Matrix

| Idea | 5min | 15min | 30min | 60min | Best |
|------|:----:|:-----:|:-----:|:-----:|:----:|
| 1. Cascade Catcher | ✅ | ✅ | ⚠️ | ❌ | 5-15min |
| 2. Basis Bounce | ❌ | ⚠️ | ✅ | ✅ | 30-60min |
| 3. Lunch Gap | ✅ | ⚠️ | ❌ | ❌ | 5min |
| 4. Whale Footprint | ⚠️ | ✅ | ✅ | ✅ | 15-30min |
| 5. Retail Exhaustion | ✅ | ✅ | ⚠️ | ❌ | 5-15min |

✅ Primary | ⚠️ Possible | ❌ Not suitable

---

## Universal Filters (Áp dụng cho tất cả)

Tất cả strategy đều cần:
1. **ADX > 22** — noise filter (entry)
2. **ADX < 15** — exit (momentum chết)
3. **return_roll > 0** — long confirmation / **< 0** — short
4. **Session gating** — position_close_ranges = ["04:30-06:00"] (lunch), close trước ATC
5. **Position sizing** — vol_scale = clip(avg_range / daily_range, 0.3, 1.0)
6. **Cooldown** — không trade lại ngay sau exit

---

## Next Steps

1. Chọn 1-2 idea ưu tiên để phân tích hypothesis chi tiết
2. Thiết kế cụ thể: entry/exit logic, parameter grid, biến thể
3. User review → approve → code
