# Thesis 09: Institutional Flow Arbitrage

## Core Concept

Phân tích dòng tiền tổ chức qua Open Interest (OI), Matched Volume/Value và VN30 Index
để xác định động lực thực sự đằng sau biến động giá VN30F futures.

Không dùng individual stock data — chỉ dùng futures OHLCV + daily `fut_*_1d` fields + VN30 index.

## Data Sources

| Field | Source | Update |
|-------|--------|--------|
| `pv_close/high/low/volume` | Futures OHLCV | Real-time |
| `pv_vn30_close` | VN30 Index | Real-time |
| `fut_open_interest_vn30f1m_1d` | OI (daily) | 1x/ngày |
| `fut_matched_volume/value_vn30f1m_1d` | Matched khớp lệnh | 1x/ngày |
| `fut_total_volume/value_vn30f1m_1d` | Tổng GTGD | 1x/ngày |

## Strategy Files

### T09-A: OI Confirmation

So sánh hướng OI change vs futures return:
- OI ↑ + price ↑ = genuine uptrend (new money in)
- OI ↑ + price ↓ = genuine downtrend (new shorts)
- OI ↓ + price ↓ = weak downtrend (short covering → fade)
- OI ↓ + price ↑ = weak uptrend (liquidation → fade)

Hạn chế: tín hiệu chỉ thay đổi 1x/ngày, phù hợp timeframe 60m+.

### T09-B: Flow Divergence

Matched Value change + VN30 alignment + Volume filter:
- matched_value ↑ + price cùng hướng + VN30 confirm = institutional flow
- matched_value ↓ = low conviction → fade price move
- Volume spike confirms signal quality

Daily field update → tín hiệu valid cả ngày sau khi daily data refresh.

### T09-C: Composite Flow

Kết hợp 3 tín hiệu OHLCV-based (an toàn, real-time):
- `price_z`: futures z-score (oversold/overbought)
- `vn30_z`: VN30 z-score (index context)
- `vol_z`: volume z-score (participation level)
- Binary flow direction: OI ↑ == matched_volume ↑ = aligned flow

Entry khi composite extreme + flow aligned. Exit khi composite decay hoặc ADX yếu.

## Khung thời gian hỗ trợ

- **60m**: khuyên dùng — daily fields change 1x/ngày, cần TF đủ lớn
- Có thể chạy Daily TF nhưng signal sparse
- TF < 60m: signal giống nhau cả ngày (daily fields constant intraday)

## Lưu ý

- Các `fut_*_1d` fields chỉ update 1 lần/ngày → signal trên intraday TF là constant cho đến hết ngày
- Không dùng `rolling_zscore` trên daily fields (z-score của constant = 0/NaN — xem thesis 08)
- Chỉ dùng `pct_change()` cho daily fields, `rolling_zscore` cho OHLCV (real-time)
