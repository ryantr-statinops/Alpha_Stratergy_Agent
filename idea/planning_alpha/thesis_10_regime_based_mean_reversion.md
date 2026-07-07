# Thesis 10: Regime-based Mean Reversion

> **Core Ideas:** Chia thị trường thành 3 regime dựa trên MA200 (Bull/Bear/Sideways), áp directional bias filter — chỉ long khi bull, chỉ short khi bear, 2 chiều khi sideways
> **VN Market Fit:** VN30F có xu hướng rõ rệt dài hạn — 2021 bull, 2022 bear, 2023-24 sideways — mỗi giai đoạn cần chiến lược riêng
> **Data Fields:** Chỉ cần OHLCV (pv_close/high/low/volume)
> **Timeframes:** 15m, 30m, 60m
> **Total Variants:** 3 core strategies

---

## Core Logic

1. **Regime classification**: `close` vs `sma(close, 200)`
   - **Bull**: `close > MA200 * 1.02` → chỉ Long, không Short
   - **Bear**: `close < MA200 * 0.98` → chỉ Short, không Long
   - **Sideways**: `|close/MA200 - 1| <= 0.02` → Mean Reversion 2 chiều

2. **Entry signals** phụ thuộc regime:
   - **Bull**: mua khi giá dip về MA20 (`close < sma(close, 20)`)
   - **Bear**: bán khi giá hồi lên MA20 (`close > sma(close, 20)`)
   - **Sideways**: quantile extremes hoặc band edges

3. **Exit**: cross MA20 trở lại hoặc ADX yếu

## Templates

### T10-A: Simple Regime Dip/Rally

Thuần nhất, không filter phụ:
- `bull & (close < ma20)` → long
- `bear & (close > ma20)` → short
- `sideways & (close < lower_q)` → long; `sideways & (close > upper_q)` → short
- Exit: cross MA20 hoặc ADX < exit

### T10-B: Confirmed Regime Entries

Thêm ADX + volume confirmation:
- Bull dip: `close < ma20 & adx > entry & volume > sma(vol)`
- Bear rally: `close > ma20 & adx > entry & volume > sma(vol)`
- Sideways: RSI extremes + low vol

### T10-C: Regime Band Oscillator

Dùng Bollinger Bands thay MA20:
- Bull: `close < lower_band` → long
- Bear: `close > upper_band` → short
- Sideways: channel extremes (wider bands)

## Parameter Tuning

| Parameter | 15m | 30m | 60m |
|-----------|-----|-----|-----|
| ma200_window | 200 | 200 | 200 |
| ma20_window | 20 | 20 | 20 |
| sideways_threshold | 0.03 | 0.02 | 0.02 |
| adx_window | 10 | 14 | 21 |
| adx_entry | 22 | 18 | 16 |
| adx_exit | 15 | 12 | 10 |

## Regime Map

| Template | Regimes | Vol | Rationale |
|----------|---------|-----|-----------|
| T10-A | trending, weak | normal, low | Dip/rally cần xu hướng rõ |
| T10-B | trending | normal, high | Confirmation cần volume + ADX mạnh |
| T10-C | weak, ranging | normal, low | Band trading phù hợp range |

## Files

| File | Location |
|------|----------|
| Template code | `tools/generate_strategies.py` |
| Backtest runner | `backtest/runners/thesis_10.py` |
| Output files | `output/thesis_10_regime_based_mean_reversion/` |

*End of Thesis 10 Design*
