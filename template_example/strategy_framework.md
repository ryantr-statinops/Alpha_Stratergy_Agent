# XNOQuant - Strategy Framework Specification

Tài liệu này định nghĩa **Framework Specification** tiêu chuẩn cho mọi chiến lược giao dịch định lượng trên nền tảng **XNOQuant**.

Mọi AI Agent khi tạo mã nguồn (`.py`) trong thư mục `output/` **phải tuân thủ tuyệt đối** kiến trúc, quy ước và các ràng buộc kỹ thuật được mô tả trong tài liệu này.

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