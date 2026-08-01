# Thesis 07: Intraday Session Microstructure

> **Session:** 2026-07-03 — New thesis group
> **Platform:** XNOQuant — `CustomStrategy(SimpleAlgorithm)`
> **Target:** VN30F futures — khai thác đặc thù phiên giao dịch VN
> **Timeframes:** 5m, 15m

---

## 1. Ý tưởng tổng quan

Thị trường VN có cấu trúc phiên đặc thù: pre-cash (8:45-9:00), morning trending (9:00-11:30), lunch dead zone (11:30-13:00), afternoon continuation (13:00-14:30), ATC manipulation (14:30-14:45). Thesis 07 khai thác các hành vi giá lặp lại theo phiên.

---

## 2. 5 Templates

| Template | Session | Entry Logic | Exit Logic | Tham số |
|----------|---------|-------------|------------|---------|
| **T07-A Open Drive** | 02:00-02:30 UTC (mở cửa sáng) | close > SMA(fast) + volume > SMA + return_roll > 0 | return_roll < 0 | fast_window, vol_window |
| **T07-B Lunch Revert** | 03:30-04:15 UTC (trước nghỉ trưa) | RSI > 70 short / RSI < 30 long + volume | RSI cross 50 | rsi_window, vol_window |
| **T07-C Close Squeeze** | 06:00-07:15 UTC (chiều) | ROC > 0 + volume spike × mult + ADX > entry | ROC < 0 | roc_window, vol_window, vol_mult |
| **T07-D Pre-ATC Rev** | 06:45-07:20 UTC (trước ATC) | BBands touch + volume confirm | cross SMA | bb_window, bb_mult, vol_window |
| **T07-E VWAP Bounce** | 02:00-04:30 + 06:00-07:15 | price ±z% from VWAP + return_roll | cross VWAP | vwap_window, z_entry |

---

## 3. Session Window (UTC → VN)

| UTC | VN | Hành vi | Giao dịch |
|:---:|:--:|---------|:---------:|
| 01:45-02:00 | 8:45-9:00 | Pre-cash, volume thấp | ❌ Tránh |
| 02:00-04:30 | 9:00-11:30 | Trending sáng | ✅ T07-A open |
| 04:30-06:00 | 11:30-13:00 | Lunch dead zone | ❌ Close positions |
| 06:00-07:30 | 13:00-14:30 | Chiều continuation | ✅ T07-C/D open |
| 07:30-07:45 | 14:30-14:45 | ATC manipulation | ❌ Flat bắt buộc |

---

## 4. Parameter Grid

| Template | Params | Variants × TF | Total |
|----------|--------|:-------------:|:-----:|
| T07-A | fast [8,13,20] × vol [14,20] | 6 × 2 = 12 | 12 |
| T07-B | rsi [7,10,14] × vol [14,20] | 6 × 2 = 12 | 12 |
| T07-C | roc [3,5] × vol [14,20] × mult [1.5,2.0] | 8 × 2 = 16 | 16 |
| T07-D | bb [14,20] × mult [2.0,2.5] × vol [14,20] | 8 × 2 = 16 | 16 |
| T07-E | vwap [14,20] × z [1.0,2.0] | 4 × 2 = 8 | 8 |
| **Total** | | | **64** |

---

## 5. Acceptance Criteria

- Sharpe ≥ 2.0, CAGR > 20%, Max DD > -20%
- Win Rate > 55% cho session-specific signals
- Số tín hiệu ≥ 30/năm (không quá thưa)

---

## 6. VN Market Mapping

| Đặc thù | Template | Cơ chế |
|---------|----------|--------|
| Retail FOMO đầu phiên | T07-A | Volume spike + momentum entry, exit khi hết đà |
| Lunch revert pattern | T07-B | RSI extreme trước nghỉ, kỳ vọng quay đầu sau lunch |
| ATC volume spike | T07-C | Breakout chiều với volume ×2, exit trước ATC |
| Basis squeeze | T07-D | BBands extreme trước đóng cửa, mean revert |
| VWAP anchor | T07-E | Price xoay quanh VWAP cả ngày, bounce tại ±1-2% |
