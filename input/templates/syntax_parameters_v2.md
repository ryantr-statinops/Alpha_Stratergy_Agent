# syntax_parameters_v2 — Bộ tham số chuẩn Round 2 (daily equity)

> **Mục đích:** Bộ tham số chuẩn cho **daily equity** (thay cho khung 15m/futures vòng 1).
> **Nguồn:** phân tích 14 examples `template_example/VN-*/` + `agent/stage_2_guideline.md`.
> **Quy ước khung:** Round 2 là **daily** — 1 ngày giao dịch = 1 bar. Không còn khái niệm
> "1 session ≈ 10 bars" như vòng 1.

## Quy ước thời gian daily (trading days)

| Đơn vị | Số bars daily |
|--------|:-------------:|
| 1 tuần | 5 |
| 1 tháng | ~21 |
| 1 quý | ~63 |
| 1 năm | ~252 |

## Quy tắc chung (phát hiện từ examples)

- **Ratio fast:slow = 1:3** là pattern ổn định nhất: `(8,24)`, `(12,36)`, `(14,42)`, `(18,54)`, `(30,90)`.
- Fast EMA: **8-12** (~1.5-2.5 tuần). Slow EMA: **24-36** (~1.2-1.7 tháng).
- Volume base (SMA): **10** (active) hoặc **20** (stable).
- RSI: **7** (active) hoặc **9** (balanced). ATR: **14** (chuẩn).
- Fundamental step-change dùng `pct_change(x, periods=1)` + `fillna(value=0)`.

---

## Trend / Moving Average

| Feature | Parameter | Giá trị | Ghi chú |
|---------|-----------|:-------:|---------|
| `ema` | timeperiod | 8 | fast — ~1.5 tuần |
| `ema` | timeperiod | 12 | fast — ~2.5 tuần |
| `ema` | timeperiod | 24 | slow (1:3 với fast 8) |
| `ema` | timeperiod | 36 | slow (1:3 với fast 12) |
| `sma` | timeperiod | 10 | volume base active |
| `sma` | timeperiod | 20 | volume base stable |
| `macd` | fastperiod | 8 | VnBankActiveRSIMACDQuality |
| `macd` | slowperiod | 21 | ≈1 tháng |
| `macd` | signalperiod | 5 | |

## Momentum / Oscillator

| Feature | Parameter | Giá trị | Ghi chú |
|---------|-----------|:-------:|---------|
| `rsi` | timeperiod | 7 | active (VnInsuranceRSIPremiumRecovery) |
| `rsi` | timeperiod | 9 | balanced (VnBankActiveRSIMACDQuality) |

## Volatility

| Feature | Parameter | Giá trị | Ghi chú |
|---------|-----------|:-------:|---------|
| `atr` | timeperiod | 14 | chuẩn — mọi example dùng 14 |

## Volume / Flow

| Feature | Parameter | Giá trị | Ghi chú |
|---------|-----------|:-------:|---------|
| `sma` (volume) | timeperiod | 10 | participation filter active |
| `sma` (volume) | timeperiod | 20 | participation filter stable |

---

## Tham số cross_sectional (panel)

| Parameter | Giá trị mới | Ghi chú |
|-----------|-------------|---------|
| `rank_cs_panel` | `method='average'` | percentile rank mỗi timestamp |
| `winsorize_cs_panel` | `lower=0.02, upper=0.98` | clip quantile |
| `zscore_cs_panel` | `ddof=1` | |
| `portfolio_weights_panel` | `method='rank_demean_l1'` | market-neutral: net≈0, gross=1 |

## Ghi chú thêm

- Timeframe 5m/30m/60m **không còn áp dụng** — Round 2 chỉ có **daily**.
- Session gates (`position_open_ranges`, ...) **không còn** — bỏ hoàn toàn.
- Nếu cần smooth fundamental (tránh step-change), dùng `self.feat.sma(series, timeperiod=...)`
  trên chính field fundamental — nhưng ví dụ chuẩn dùng `pct_change` + `fillna`.
