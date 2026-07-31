# Parameter Reference (Round 2 — Daily Equity)

Round 2 là **daily equity** (small/mid/large-cap). 1 ngày giao dịch = 1 bar.
Bộ tham số dưới đây được suy ra từ 14 examples `template_example/VN-*/` — dùng tạm làm chuẩn,
cần xác nhận lại trên platform khi sample pass điều kiện.

## Section Index

| Group | Jump to |
|---|---|
| Trend / Moving Average | [Trend / Moving Average](#trend--moving-average) |
| Momentum / Oscillator | [Momentum / Oscillator](#momentum--oscillator) |
| Volatility | [Volatility](#volatility) |
| Volume / Flow | [Volume / Flow](#volume--flow) |
| Fundamental Step-Change | [Fundamental Step-Change](#fundamental-step-change) |
| Cross-Sectional (Panel) | [Cross-Sectional (Panel)](#cross-sectional-panel) |

## Quy ước thời gian daily

| Đơn vị | Số bars daily |
|--------|:-------------:|
| 1 tuần | 5 |
| 1 tháng | ~21 |
| 1 quý | ~63 |
| 1 năm | ~252 |

> **Pattern chính:** ratio fast:slow = **1:3** — `(8,24)`, `(12,36)`, `(14,42)`, `(18,54)`, `(30,90)`.

## Trend / Moving Average

| Feature | Parameter | Giá trị | Ghi chú |
|---------|-----------|:-------:|---------|
| ema | timeperiod | 8 | fast (~1.5 tuần) |
| ema | timeperiod | 12 | fast (~2.5 tuần) |
| ema | timeperiod | 24 | slow (1:3 với fast 8) |
| ema | timeperiod | 36 | slow (1:3 với fast 12) |
| sma | timeperiod | 10 | volume base active |
| sma | timeperiod | 20 | volume base stable |
| macd | fastperiod | 8 | theo VnBankActiveRSIMACDQuality |
| macd | slowperiod | 21 | ≈1 tháng |
| macd | signalperiod | 5 | |

## Momentum / Oscillator

| Feature | Parameter | Giá trị | Ghi chú |
|---------|-----------|:-------:|---------|
| rsi | timeperiod | 7 | active |
| rsi | timeperiod | 9 | balanced |

## Volatility

| Feature | Parameter | Giá trị | Ghi chú |
|---------|-----------|:-------:|---------|
| atr | timeperiod | 14 | chuẩn — mọi example |

## Volume / Flow

| Feature | Parameter | Giá trị | Ghi chú |
|---------|-----------|:-------:|---------|
| sma (volume) | timeperiod | 10 | participation active |
| sma (volume) | timeperiod | 20 | participation stable |

## Fundamental Step-Change

Fundamentals daily-aligned chỉ đổi khi report mới công bố. Đo sự thay đổi bằng:

```python
profit_growth = self.op.fillna(self.op.pct_change(net_profit, periods=1), value=0)
```

| Ngưỡng | Giá trị phổ biến | Ghi chú |
|--------|:----------------:|---------|
| Không suy giảm (entry) | `> -0.02` đến `> -0.08` | tuỳ độ chặt |
| Không suy giảm rõ (entry) | `> 0` | strong long |
| Exit khi giảm mạnh | `< -0.05` đến `< -0.15` | tuỳ tolerance |

## Cross-Sectional (Panel)

| Feature / Op | Parameter | Giá trị | Ghi chú |
|--------------|-----------|:-------:|---------|
| `rank_cs_panel` | method | `'average'` | percentile rank mỗi timestamp |
| `winsorize_cs_panel` | lower / upper | `0.02` / `0.98` | |
| `zscore_cs_panel` | ddof | `1` | |
| `portfolio_weights_panel` | method | `'rank_demean_l1'` | market-neutral: net≈0, gross=1 |

## Ghi chú

- Khung 5m/30m/60m **không áp dụng** — Round 2 chỉ daily.
- Session gates **không còn** — bỏ hoàn toàn (so với vòng 1 15min futures).
- Bộ tham số này là **ước lượng từ sample**; khi platform cho phép verify, cần đối chiếu lại.
