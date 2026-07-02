# Alpha Ideas — 5 New Strategy Concepts (Vietnam Derivatives Focus)

> **Session:** 2026-07-02 — Fresh brainstorm, no legacy thesis constraints
> **Core principle:** Leverage Vietnam market microstructure (80-90% retail, 1:6-1:8 leverage, session quirks, unique futures data)
> **Sharpe Formula:** Mỗi idea được thiết kế với 7 thành phần của công thức Sharpe ≥ 2.0 tích hợp ngay từ đầu

---

## Sharpe ≥ 2.0 Template

```
Entry:  core_signal                         # Alpha đặc thù
        & (adx > 22)                        # Noise filter
        & (return_roll > 0 cho long, < 0 cho short)  # Momentum confirm
        & (volume > SMA)                    # Volume confirm
        & (abs(roc) > 0.003)               # Whipsaw guard

Exit:   core_exit                           # Alpha-specific exit
        | (abs(return_roll) < threshold)    # Asymmetric: momentum chết
        | (adx < 15)                        # Xu hướng chết
        | trailing_stop                     # Chandelier bảo vệ

Risk:   position_close_after_n_candles      # Session gating
        | position_close_ranges             # Lunch, pre-ATC
        | recent_exit cooldown              # Consecutive loss protection
```

---

## Idea 1: "Cascade Catcher" — Margin Call Domino

### Concept
VN30F1M leverage 1:6-1:8 → 2% drop triggers margin calls → forced selling cascade (2-5 candles). OI drop confirms smart money đã thoát.

### Core Alpha Signal
```
# Short: cascade active
oi_drop = pct_change(oi, 1) < -0.01
vol_spike = matched_volume > SMA(matched_vol, 20) * 2.0
price_fall = pct_change(close, 1) < -0.005
cascade = oi_drop & vol_spike & price_fall

# Long: cascade exhaustion
vol_collapse = matched_volume < SMA(matched_vol, 20) * 0.5
price_stable = abs(pct_change(close, 1)) < 0.001
exhaustion = oi_drop & vol_collapse & price_stable
```

### Sharpe 7-component Design
| Component | Implementation |
|-----------|---------------|
| **ADX > 22** | `& (adx > 22)` trên entry |
| **return_roll > 0** | `& (return_roll < 0)` cho short; `& (return_roll > 0)` cho long (exhaustion) |
| **Volume > SMA** | `& (matched_volume > SMA * 2)` — dùng futures matched volume |
| **ROC > 0.3%** | `& (pct_change(1) < -0.005)` — price fall phải rõ ràng |
| **Asymmetric exit** | `exit \| (abs(return_roll) < threshold) \| (adx < 15)` |
| **Session gating** | `position_close_ranges = ["04:30-06:00"]` (lunch), close trước ATC |
| **Consecutive loss** | `recent_exit = rolling_max(exit, 3)` block re-entry |

### Entry Logic
```
short_setup = cascade & (return_roll < 0) & (adx > 22)
long_setup  = exhaustion & (return_roll > 0) & (adx > 22)
```

### Exit Logic
```
exit_setup = crossed_below(close, oi_sma)           # OI trend đảo
           | crossed_above(close, oi_sma)
           | crossed_below(abs(return_roll), threshold)  # Momentum chết
           | crossed_below(adx, 15)                      # ADX chết
           | trailing_stop
```

### Key Data
`fut_matched_volume_vn30f1m_1d`, `fut_open_interest_vn30f1m_1d`, `pv_close`

### TF Suitability
| 5min | 15min | 30min | 60min |
|:----:|:-----:|:-----:|:-----:|
| ✅ | ✅ | ⚠️ | ❌ |

### Parameter Grid
| Variant | OI Drop | Vol Spike | Price Fall | return_roll | ADX Entry | ADX Exit |
|---------|:-------:|:---------:|:----------:|:-----------:|:---------:|:--------:|
| **Aggr** | > 0.5% | > 1.5x | > 0.3% | window=3 | > 20 | < 13 |
| **Std** | > 1.0% | > 2.0x | > 0.5% | window=5 | > 22 | < 15 |
| **Cons** | > 2.0% | > 3.0x | > 1.0% | window=5 | > 25 | < 18 |

---

## Idea 2: "Basis Bounce" — Futures vs Cash Reversion

### Concept
Retail FOMO đẩy basis (futures - VN30) ra xa fair value. Basis ở extreme + volume đuối = hết đà → reversion về mean.

### Core Alpha Signal
```
basis = pv_close - pv_vn30_close
basis_zscore = rolling_zscore(basis, 20)

# Short: basis quá rộng = retail đang FOMO long futures
short_basis = (basis_zscore > 2.5)

# Long: basis quá hẹp (âm) = retail đang panic short
long_basis = (basis_zscore < -2.5)
```

### Sharpe 7-component Design
| Component | Implementation |
|-----------|---------------|
| **ADX > 22** | `& (adx > 22)` — chỉ trade khi futures có xu hướng |
| **return_roll > 0** | Dùng return_roll của basis (basis_momentum), không của price |
| **Volume > SMA** | `& (matched_volume < SMA * 1.2)` — volume ĐUỐI = hết đà |
| **ROC > 0.3%** | `& (abs(roc_basis, 3) > 0.005)` — basis phải di chuyển đủ xa |
| **Asymmetric exit** | `basis_zscore về [-1, 1] \| return_roll_basis đảo` |
| **Session gating** | Chỉ trade morning session (VN 9:00-11:30) — basis tin cậy nhất |
| **Consecutive loss** | `cooldown = 3` — không re-entry ngay sau basis squeeze |

### Entry Logic
```
basis_roll = rolling_mean(pct_change(basis, 1), window=5)
short_setup = short_basis & (basis_roll < 0) & (adx > 22) & (matched_vol < SMA * 1.2)
long_setup  = long_basis  & (basis_roll > 0) & (adx > 22) & (matched_vol < SMA * 1.2)
```

### Exit Logic
```
exit_setup = between(basis_zscore, -1, 1)
           | crossed_below(abs(basis_roll), threshold)
           | crossed_below(adx, 15)
           | trailing_stop
```

### Key Data
`pv_close`, `pv_vn30_close`, `fut_matched_volume_vn30f1m_1d`

### TF Suitability
| 5min | 15min | 30min | 60min |
|:----:|:-----:|:-----:|:-----:|
| ❌ | ⚠️ | ✅ | ✅ |

### Parameter Grid
| Variant | Z-score Entry | Basis Window | return_roll | ADX Entry | Volume Filter |
|---------|:-------------:|:------------:|:-----------:|:---------:|:-------------:|
| **Aggr** | > 2.0 | 14 | window=3 | > 20 | < SMA * 1.3 |
| **Std** | > 2.5 | 20 | window=5 | > 22 | < SMA * 1.2 |
| **Cons** | > 3.0 | 34 | window=8 | > 25 | < SMA * 1.0 |

---

## Idea 3: "Lunch Gap" — Pre/Post Lunch Mean Reversion

### Concept
Lunch (11:30-13:00 VN = 04:30-06:00 UTC): futures vẫn giao dịch, volume cực thấp. Giá bị đẩy ảo. Phiên chiều revert trong 3-5 nến.

### Core Alpha Signal
```
lunch_move = (close_at_13:00 - close_at_11:30) / close_at_11:30
atr = atr(high, low, close, timeperiod=14)
lunch_vol_ratio = matched_volume / SMA(matched_vol, 20)

# Trade chiều ngược lunch move
gap_down = (lunch_move < -0.5 * atr) & (lunch_vol_ratio < 0.3)
gap_up   = (lunch_move > 0.5 * atr)  & (lunch_vol_ratio < 0.3)
```

### Sharpe 7-component Design
| Component | Implementation |
|-----------|---------------|
| **ADX > 22** | `& (adx > 22)` — phiên chiều phải có trend |
| **return_roll > 0** | `& (return_roll > 0)` cho long gap-down; `< 0` cho short gap-up |
| **Volume > SMA** | Lunch volume phải THẤP (< 30% SMA) để xác nhận giá ảo |
| **ROC > 0.3%** | `& (lunch_move > 0.5*atr)` — move phải đủ lớn |
| **Asymmetric exit** | `exit sau 3-5 nến \| return_roll đảo` |
| **Session gating** | Chỉ mở entry 06:00-06:15 UTC (13:00-13:15 VN); close 06:15-06:30 |
| **Consecutive loss** | `cooldown = 5` — chờ phiên sau nếu lunch gap fail |

### Entry Logic
```
long_setup  = gap_down  & (return_roll > 0) & (adx > 22)
short_setup = gap_up    & (return_roll < 0) & (adx > 22)
```

### Exit Logic
```
exit_setup = crossed_below(return_roll, 0)     # Momentum hết
           | crossed_below(adx, 15)             # Trend chết
           | bars_since(entry) > 5              # Max hold 5 nến
```

### Key Data
`pv_close`, `pv_high`, `pv_low`, `fut_matched_volume_vn30f1m_1d`

### TF Suitability
| 5min | 15min | 30min | 60min |
|:----:|:-----:|:-----:|:-----:|
| ✅ | ⚠️ | ❌ | ❌ |

### Parameter Grid
| Variant | Lunch Move | Vol Ratio | return_roll | ADX Entry | Max Hold |
|---------|:----------:|:---------:|:-----------:|:---------:|:--------:|
| **Aggr** | > 0.3x ATR | < 0.4x | window=3 | > 20 | 3 |
| **Std** | > 0.5x ATR | < 0.3x | window=3 | > 22 | 5 |
| **Cons** | > 0.8x ATR | < 0.2x | window=3 | > 25 | 5 |

---

## Idea 4: "Whale Footprint" — Average Trade Size Surge

### Concept
`avg_trade = matched_value / matched_volume`. Khi avg_trade tăng đột biến + giá nén = cá mập đang tích lũy → breakout imminent.

### Core Alpha Signal
```
avg_trade = fut_matched_value / fut_matched_volume
avg_trade_sma = SMA(avg_trade, 20)
avg_trade_std = rolling_std(avg_trade, 20)
price_compression = (max(close,10) - min(close,10)) / min(close,10) < 0.01

whale = avg_trade > avg_trade_sma + 2 * avg_trade_std
```

### Sharpe 7-component Design
| Component | Implementation |
|-----------|---------------|
| **ADX > 22** | `& (adx > 22)` — breakout cần xu hướng |
| **return_roll > 0** | Xác nhận hướng breakout: `& (return_roll > 0)` cho long |
| **Volume > SMA** | `& (matched_volume > SMA * 1.5)` — breakout phải có volume |
| **ROC > 0.3%** | `& (abs(roc(close, 1)) > 0.003)` — breakout đủ mạnh |
| **Asymmetric exit** | `exit khi compression break \| return_roll đảo` |
| **Session gating** | 15-30min TF: tránh lunch, tránh ATC |
| **Consecutive loss** | `cooldown = 2` — whale signal hiếm, chờ signal thật |

### Entry Logic
```
breakout_vol = matched_volume > SMA(matched_vol, 20) * 1.5
long_setup  = whale & price_compression & breakout_vol & (return_roll > 0) & (adx > 22)
short_setup = whale & price_compression & breakout_vol & (return_roll < 0) & (adx > 22)
```

### Exit Logic
```
exit_setup = crossed_below(close, SMA(close, 20))    # Hết range
           | crossed_below(abs(return_roll), threshold)
           | crossed_below(adx, 15)
           | trailing_stop
```

### Key Data
`fut_matched_value_vn30f1m_1d`, `fut_matched_volume_vn30f1m_1d`, `pv_close`, `pv_high`, `pv_low`

### TF Suitability
| 5min | 15min | 30min | 60min |
|:----:|:-----:|:-----:|:-----:|
| ⚠️ | ✅ | ✅ | ✅ |

### Parameter Grid
| Variant | Whale σ | Compression | Vol Breakout | return_roll | ADX |
|---------|:-------:|:-----------:|:------------:|:-----------:|:---:|
| **Aggr** | > 1.5σ | 7 candles | > 1.5x | window=3 | > 20 |
| **Std** | > 2.0σ | 10 candles | > 2.0x | window=5 | > 22 |
| **Cons** | > 2.5σ | 14 candles | > 2.5x | window=5 | > 25 |

---

## Idea 5: "Retail Exhaustion" — Volume Spike Reversal

### Concept
Retail 80-90%: volume spike + nến dài = đỉnh FOMO/panic. Retail exhausted → reversal.

### Core Alpha Signal
```
vol_ratio = pv_volume / SMA(pv_volume, 14)
candle_body = abs(pv_close - pv_open)
atr = atr(high, low, close, timeperiod=14)
vol_spike = (vol_ratio > 3.0) & (candle_body > 1.5 * atr)

# Long: panic short exhaustion
panic_long  = vol_spike & (close < quantile(close, 20, 0.10)) & (open < close)

# Short: FOMO long exhaustion
fomo_short  = vol_spike & (close > quantile(close, 20, 0.90)) & (open > close)
```

### Sharpe 7-component Design
| Component | Implementation |
|-----------|---------------|
| **ADX > 22** | `& (adx > 22)` — reversal cần xu hướng nền |
| **return_roll > 0** | Phân biệt panic exhaustion (return_roll vừa chéo lên) vs falling knife |
| **Volume > SMA** | `& (pv_volume > SMA * 3)` — volume spike là core signal |
| **ROC > 0.3%** | `& (candle_body > 1.5*atr)` — nến đủ lớn |
| **Asymmetric exit** | `exit \| return_roll đảo \| adx < 15` |
| **Session gating** | Lunch + ATC: không trade panic gần cuối phiên |
| **Consecutive loss** | `cooldown = 3` — spike có thể là trend continuation |

### Entry Logic
```
long_setup  = panic_long  & (return_roll > -0.005) & (adx > 22)
short_setup = fomo_short  & (return_roll < 0.005)  & (adx > 22)
```

### Exit Logic
```
exit_setup = crossed_below(close, SMA(close, 20))    # Hồi phục xong
           | crossed_below(abs(return_roll), threshold)
           | crossed_below(adx, 15)
           | trailing_stop
```

### Key Data
`pv_close`, `pv_open`, `pv_high`, `pv_low`, `pv_volume`

### TF Suitability
| 5min | 15min | 30min | 60min |
|:----:|:-----:|:-----:|:-----:|
| ✅ | ✅ | ⚠️ | ❌ |

### Parameter Grid
| Variant | Vol Spike | Body/ATR | Quantile | return_roll | ADX |
|---------|:---------:|:--------:|:--------:|:-----------:|:---:|
| **Aggr** | > 2.5x | > 1.2x | 0.15/0.85 | window=3 | > 20 |
| **Std** | > 3.0x | > 1.5x | 0.10/0.90 | window=3 | > 22 |
| **Cons** | > 4.0x | > 2.0x | 0.05/0.95 | window=5 | > 25 |

---

## Summary: Acceptance Criteria Mapping

| Metric | Target | Cascade Catcher | Basis Bounce | Lunch Gap | Whale Footprint | Retail Exhaust |
|--------|:------:|:---------------:|:------------:|:---------:|:---------------:|:--------------:|
| **Sharpe** | ≥ 2.0 | 7/7 components | 7/7 | 7/7 | 7/7 | 7/7 |
| **CAGR** | > 20% | Short-duration, tần suất cao | Tần suất thấp hơn | Chỉ 2 trade/ngày | Tần suất thấp | Tần suất trung bình |
| **Max DD** | > -20% | ADX filter + asymmetric exit bảo vệ |

**Kết luận:** Cả 5 idea đều đã tích hợp đủ 7 thành phần Sharpe. Sự khác biệt nằm ở tần suất tín hiệu và độ tin cậy — sẽ được xác nhận qua backtest.
