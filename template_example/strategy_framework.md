# XNOQuant - Strategy Framework Specification

Tài liệu này định nghĩa **Framework Specification** tiêu chuẩn cho mọi chiến lược giao dịch định lượng trên nền tảng **XNOQuant**.

Mọi AI Agent khi tạo mã nguồn (`.py`) trong thư mục `output/` **phải tuân thủ tuyệt đối** kiến trúc, quy ước và các ràng buộc kỹ thuật được mô tả trong tài liệu này.

---

## Thesis Group Reference

Mỗi strategy thuộc 1 trong 8 thesis groups sau:

| Thesis Group | Data Required | Key Indicators | Timeframes |
|--------------|---------------|----------------|:----------:|
| 01 Momentum | `pv_close`, `pv_volume`, `pv_vn30_close` | `roc`, `rsi`, `mom`, `cmo` | 5, 15, 30, 60 |
| 02 Trend | `pv_close`, `pv_high`, `pv_low` | `ema`, `sma`, `macd`, `adx`, `bbands` | 5, 15, 30, 60 |
| 03 Mean Reversion | `pv_close` | `rolling_quantile`, `rsi`, `bbands`, `rolling_zscore` | 5, 15, 30, 60 |
| 04 Breakout | `pv_close`, `pv_volume`, `pv_high`, `pv_low` | `rolling_quantile`, `rolling_max`, `rolling_min`, `volume` | 5, 15, 30, 60 |
| 05 Cross-Market | `pv_close`, `pv_vn30_*`, `pv_dji_*` | `roc`, `rolling_correlation`, `rolling_zscore` | 15, 30, 60 |
| 06 Volume & Flow | `pv_close`, `fut_*` | `rolling_mean`, `rolling_quantile` | 15, 30, 60 |
| 07 Intraday Session | `pv_open`, `pv_close`, `pv_high`, `pv_low` | `roc`, `rolling_vwap`, `rsi` | 5, 15 |
| 08 Multi-Factor | All of the above | Composite z-score | 15, 30, 60 |

---

# 1. Architecture Overview

Mỗi chiến lược được xây dựng theo pipeline xử lý dữ liệu gồm **4 tầng**.

```text
                 XNOQuant Strategy Pipeline

┌──────────────────────────────────────────────────────────┐
│ Layer 1: Raw Market Data                                │
│ self.data                                                │
│ • OHLCV                                                  │
│ • Open Interest                                          │
│ • Futures Data                                           │
└──────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│ Layer 2: Feature Engineering                             │
│ self.feat                                                │
│ • EMA                                                    │
│ • RSI                                                    │
│ • Rolling Mean                                           │
│ • BBands                                                 │
│ • ATR                                                    │
│ • ...                                                    │
└──────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│ Layer 3: Trading Logic                                   │
│ self.op                                                  │
│ • crossed_above                                          │
│ • crossed_below                                          │
│ • fillna                                                 │
│ • logical operators                                      │
└──────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│ Layer 4: Position Sizing                                 │
│ self.set_positions()                                     │
└──────────────────────────────────────────────────────────┘
```

Mọi chiến lược đều phải đi qua **đúng thứ tự** bốn tầng trên.

---

# 2. Standard Strategy Template

Mọi file chiến lược phải được xây dựng theo cấu trúc sau.

## 2.1 Multi-Timeframe Class Attributes

Class attributes define strategy configuration. **Do not use `__init__`.**

```python
class CustomStrategy(SimpleAlgorithm):

    # Window parameters — scale theo timeframe
    fast_window = 13       # Fast MA / RSI period
    slow_window = 34       # Slow MA period
    vol_window = 20        # Volume moving average

    # Thesis group identifier (for index.csv)
    thesis_group = "momentum"

    # Thresholds
    adx_threshold = 20     # ADX > 20 = trending
    rsi_lower = 30         # Oversold
    rsi_upper = 70         # Overbought
```

Window sizing convention theo timeframe:

| Timeframe | Fast | Slow | RSI | ADX |
|:---------:|:----:|:----:|:---:|:---:|
| 5 min | 8 | 20 | 7 | 7 |
| 15 min | 13 | 34 | 10 | 10 |
| 30 min | 20 | 50 | 14 | 14 |
| 60 min | 30 | 100 | 21 | 21 |

## 2.2 Data Access Patterns

### Core OHLCV
```python
close = self.data.pv_close
high = self.data.pv_high
low = self.data.pv_low
volume = self.data.pv_volume
open_price = self.data.pv_open
```

### VN30 Index (Cross-Market)
```python
vn30_close = self.data.pv_vn30_close
vn30_high = self.data.pv_vn30_high
vn30_low = self.data.pv_vn30_low
vn30_open = self.data.pv_vn30_open
```

### Dow Jones (Global)
```python
dji_close = self.data.pv_dji_close
dji_high = self.data.pv_dji_high
dji_low = self.data.pv_dji_low
dji_open = self.data.pv_dji_open
```

### Futures-Specific (Daily bars — suffix `_1d`)
```python
matched_vol = self.data.fut_matched_volume_vn30f1m_1d
matched_val = self.data.fut_matched_value_vn30f1m_1d
oi = self.data.fut_open_interest_vn30f1m_1d
total_vol = self.data.fut_total_volume_vn30f1m_1d
total_val = self.data.fut_total_value_vn30f1m_1d
```

## 2.3 Template

```python
class CustomStrategy(SimpleAlgorithm):

    fast_window = 13
    slow_window = 34
    vol_window = 5

    def __algorithm__(self):
        """
        Stage 2
        Core Strategy Logic
        """

        # =====================================================
        # STEP 1
        # Raw Market Data
        # =====================================================

        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        open_price = self.data.pv_open

        oi = self.data.fut_open_interest_vn30f1m_1d


        # =====================================================
        # STEP 2
        # Feature Engineering
        # =====================================================

        mean_fast = self.feat.rolling_mean(
            close,
            window=self.fast_window
        )

        mean_slow = self.feat.rolling_mean(
            close,
            window=self.slow_window
        )

        mean_vol = self.feat.rolling_mean(
            volume,
            window=self.vol_window
        )


        # =====================================================
        # STEP 3
        # Trading Logic
        # =====================================================

        price_cross_above = self.op.crossed_above(
            close,
            mean_fast
        )

        price_cross_below = self.op.crossed_below(
            close,
            mean_fast
        )

        trend_filter = mean_fast > mean_slow

        volume_filter = volume > mean_vol

        long_setup = (
            price_cross_above
            & trend_filter
            & volume_filter
        )

        short_setup = (
            price_cross_below
            & (~trend_filter)
            & volume_filter
        )

        exit_setup = self.op.crossed_below(
            close,
            mean_slow
        )


        # =====================================================
        # STEP 4
        # Position Sizing
        # =====================================================

        self.set_positions(
            exit_setup,
            position=0
        )

        self.set_positions(
            long_setup,
            position=1.0
        )

        self.set_positions(
            short_setup,
            position=-1.0
        )
```

---

# 3. Framework Layers

## Layer 1 — Raw Data (`self.data`)

Chỉ được lấy dữ liệu từ đối tượng `self.data`.

Ví dụ:

```python
close = self.data.pv_close
high = self.data.pv_high
low = self.data.pv_low
volume = self.data.pv_volume

open_price = self.data.pv_open

oi = self.data.fut_open_interest_vn30f1m_1d
```

Không tự sinh dữ liệu ngoài framework.

---

## Layer 2 — Feature Engineering (`self.feat`)

Toàn bộ chỉ báo kỹ thuật phải được gọi từ `self.feat`.

Ví dụ:

```python
ema = self.feat.ema(close)

rsi = self.feat.rsi(close)

mean = self.feat.rolling_mean(close)

atr = self.feat.atr(high, low, close)
```

Không tự viết lại indicator nếu hệ thống đã hỗ trợ.

---

## Layer 3 — Trading Logic (`self.op`)

Logic giao dịch chỉ sử dụng:

- toán tử Bitwise (`&`, `|`, `~`)
- toán tử so sánh
- các hàm trong `self.op`

Ví dụ:

```python
cross_up = self.op.crossed_above(close, ema)

cross_down = self.op.crossed_below(close, ema)

entry = cross_up & trend_filter

exit = cross_down
```

---

## Layer 4 — Position Sizing

Việc đặt lệnh chỉ thông qua:

```python
self.set_positions(condition, position)
```

Không sử dụng bất kỳ API đặt lệnh nào khác.

---

# 4. Position Sizing Rules

| Position | Trading State | Description |
|-----------|---------------|-------------|
| `1.0` | Full Long | 100% vốn vào vị thế Long |
| `0.5` | Partial Long | 50% Long |
| `0.0` | Flat / Exit | Thoát toàn bộ vị thế |
| `-0.5` | Partial Short | 50% Short |
| `-1.0` | Full Short | 100% Short |

---

# 5. Strict Technical Guardrails

## 5.1 Variable Naming

Không bao giờ đặt:

```python
open = ...
```

Luôn sử dụng:

```python
open_price = ...
```

hoặc

```python
op_price = ...
```

---

## 5.2 Remove Documentation Type Hints

Các tài liệu trong `feature/` và `operations/` có thể chứa:

```python
SeriesT = None
```

hoặc

```python
-> SeriesT
```

Các ký hiệu này **chỉ dùng cho tài liệu**, không được xuất hiện trong mã nguồn sinh ra.

Ví dụ:

Không hợp lệ:

```python
EMA(source: SeriesT = None)
```

Hợp lệ:

```python
EMA(source)
```

---

## 5.3 Position Order Priority

Trong `__logic__`, thứ tự gọi `set_positions()` phải luôn là:

```python
Exit

↓

Long

↓

Short
```

Ví dụ:

```python
self.set_positions(exit_setup, position=0)

self.set_positions(long_setup, position=1.0)

self.set_positions(short_setup, position=-1.0)
```

Không được đảo thứ tự này nhằm tránh xung đột trạng thái trong quá trình Backtest.

---

# 6. AI Agent Compliance Checklist

Trước khi sinh bất kỳ file `.py` nào, AI Agent phải xác nhận đã đáp ứng đầy đủ các điều kiện sau:

- [ ] Đã đọc toàn bộ tài liệu trong `data/`
- [ ] Đã đọc toàn bộ tài liệu trong `feature/`
- [ ] Đã đọc toàn bộ tài liệu trong `operations/`
- [ ] Đã tham khảo `template_example/`
- [ ] Chỉ sử dụng API chính thức của XNOQuant
- [ ] Không sử dụng thư viện hoặc framework ngoài nếu không được yêu cầu
- [ ] Không giữ lại các type hint từ tài liệu (`SeriesT`, `-> SeriesT`, ...)
- [ ] Không sử dụng biến `open`
- [ ] Chỉ sử dụng `self.set_positions()` để đặt lệnh
- [ ] Luôn đặt lệnh `Exit` trước `Long` và `Short`
- [ ] Mã nguồn có thể chạy trực tiếp trên nền tảng XNOQuant mà không cần chỉnh sửa thêm.