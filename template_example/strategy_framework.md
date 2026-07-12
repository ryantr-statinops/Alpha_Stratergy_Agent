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

> Xem chi tiết field tại [`syntax/data_syntax.md`](../syntax/data_syntax.md).

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

Các tài liệu trong `syntax/` có thể chứa:

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

## 5.3 Signal Masking — `& (~exit_setup)`

Ngoài cơ chế Exit→Long→Short priority (section 5.3), một số chiến lược (đặc biệt thesis 10) dùng thêm **safety mask** để đảm bảo bar exit không bị entry override:

```python
exit_setup = (...)  # MA20 cross, ADX threshold, atr_stop
long_setup = dip_long | mr_long
short_setup = rally_short | mr_short

long_signal = long_setup & (~exit_setup)
short_signal = short_setup & (~exit_setup)

self.set_positions(exit_setup, position=0)
self.set_positions(long_signal, position=1)
self.set_positions(short_signal, position=-1)
```

### Tại sao cần cả mask lẫn priority?

Cơ chế priority (Exit→Long→Short) vốn đã xử lý overlap ở **layer position sizing**: gọi `set_positions(exit)` trước, `set_positions(long)` sau — Long override Exit. Nhưng điều này phụ thuộc vào thứ tự gọi, có thể gây bug nếu vô tình đổi thứ tự.

`& (~exit_setup)` là **defense-in-depth ở layer trading logic**: chủ động loại bỏ bar exit khỏi entry signal ngay từ đầu. Điều này:

- Không phụ thuộc vào thứ tự gọi `set_positions`
- Dễ đọc, dễ maintain — intent rõ ràng: "nếu bar này exit thì không vào lệnh"
- Quan trọng nhất với các chiến lược có **nhiều exit conditions OR nhau** (T10 có 5 conditions) — khó đảm bảo mutual exclusivity tuyệt đối

### Khi nào dùng mask?

- **Nên dùng**: chiến lược có exit_setup phức tạp (nhiều OR conditions), đặc biệt khi exit và entry dùng chung indicator reference (MA20, ATR, ADX)
- **Không bắt buộc**: chiến lược đơn giản với 1-2 exit conditions, mutual exclusivity rõ ràng giữa entry và exit

### Lưu ý

```python
# KHÔNG làm thế này — exit_setup bị biến đổi, làm mất intent gốc
long_setup = long_setup & (~exit_setup)
short_setup = short_setup & (~exit_setup)

# LÀM thế này — giữ nguyên long_setup/short_setup gốc, tạo biến mới
long_signal = long_setup & (~exit_setup)
short_signal = short_setup & (~exit_setup)
```

Giữ `long_setup`/`short_setup` gốc giúp:
- Dễ debug (có thể so sánh raw setup vs masked signal)
- Dễ mở rộng (thêm position sizing filter mà không ảnh hưởng logic entry)

---

## 5.4 Position Order Priority

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

## 5.5 Exit Conditions — Không chứa condition mà entry_setup cần

Nếu entry_setup gated bởi một threshold (vd `adx_val > adx_entry`), exit_setup **không được** chứa cùng condition đó — nếu không, `~exit_setup` mask sẽ triệt tiêu entry.

### Sai
```python
long_setup = (adx_val > adx_entry) & (z < -z_entry)
exit_setup = (adx_val > adx_entry) | (abs(z) < z_exit)   # adx > entry REPEATED
long_signal = long_setup & (~exit_setup)                   # → ALWAYS FALSE
```

### Đúng
```python
long_setup = (adx_val > adx_entry) & (z < -z_entry)
exit_setup = (abs(z) < z_exit)                             # không dùng lại adx_val
# Hoặc exit bằng sự kiện, không phải mức:
exit_setup = crossed_below(adx_val, adx_exit) | (abs(z) < z_exit)
```

### Nguyên tắc
- Entry dùng **level** (`adx > entry`, `z > entry`) → exit KHÔNG dùng level đó
- Exit dùng **sự kiện** (`crossed_below`, `crossed_above`) hoặc **threshold khác** (z_exit < z_entry)
- Nếu cần thoát khi thị trường chuyển trend: dùng `crossed_above(adx, adx_entry)` (sự kiện vượt ngưỡng), không dùng `adx > adx_entry` (mức)

---

## 5.6 Trend/Regime Detection — Tách riêng, không nhét vào exit_setup

`trend_up` / `trend_down` / `ranging` / `trending` là **entry GATE**, không phải exit condition.

### Sai
```python
atr_stop = (close < ma20 - mult * atr) | (close > ma20 + mult * atr)
exit_setup = ... | atr_stop          # ATR stop lẫn vào exit → mất khả năng TF entry
```

### Đúng
```python
# Trend detection — dùng để gate entry
trend_up = close > ma20 + mult * atr
trend_down = close < ma20 - mult * atr

# Entry gate: chặn MR ngược chiều trend
mr_long = (z < -z_entry) & (basis_z < -z_entry) & (~trend_down)
mr_short = (z > z_entry) & (basis_z > z_entry) & (~trend_up)
tf_long = trend_up
tf_short = trend_down

# Exit — chỉ chứa tín hiệu đảo chiều/neutral
exit_reversion = (abs(z) < z_exit) | (abs(basis_z) < z_exit)
final_exit = exit_reversion & (~trend_up) & (~trend_down)
```

---

## 5.7 `long_setup` và `short_setup` — Phải Mutually Exclusive

Nếu cả long và short cùng true trên 1 bar, hệ thống sẽ cho short thắng (last-write-wins). Đây là hành vi mặc định, **không được dựa vào nó**.

### Bắt buộc

```python
# Guard — phải có trong __algorithm__ hoặc compute_positions
assert not (long_signal & short_signal).any(), "long và short overlap trên cùng bar"
```

### Các pattern đảm bảo mutual exclusive

```python
# Pattern 1: Z-score đối xứng (tự nhiên exclusive)
long = (z < -z_entry)
short = (z > z_entry)                    # không thể cả 2 cùng đúng

# Pattern 2: Directional split rõ ràng
long = (price > mean) & (rsi > 50)
short = (price < mean) & (rsi < 50)      # price > mean và price < mean không thể đồng thời

# Pattern 3: Dùng regime gate
long = mr_long | tf_long
short = mr_short | tf_short              # mr_long và mr_short exclusive, tf_long và tf_short exclusive
```

### Pattern KHÔNG được dùng

```python
# LỖI — cùng điều kiện, không directional split
long_setup = whale & price_compression & high_vol
short_setup = whale & price_compression & high_vol   # copy-paste → SHORT ONLY
```

---

## 5.8 Không trộn `crossed_*` và Level Condition trên cùng 1 biến giữa Entry và Exit

Nếu entry dùng **level** (`>` , `<`), exit phải dùng **level**, không dùng `crossed_above`/`crossed_below` — và ngược lại.

### Vấn đề
```python
# Entry: level — đúng khi giá > mean
long_setup = close > mean_20

# Exit: crossed — đúng bar giá cắt xuống dưới mean
exit_setup = crossed_below(close, mean_20)
```

Trên bar giá lần đầu vượt lên trên mean: `close > mean = True` (entry), nhưng `crossed_below` cũng True nếu bar trước ở trên → **cả entry và exit cùng true**.

### Giải pháp

```python
# Cách 1: Cả entry và exit đều dùng crossed
long_setup = crossed_above(close, mean_20)
exit_setup = crossed_below(close, mean_20)      # không overlap vì crossed exclusive

# Cách 2: Cả entry và exit đều dùng level + neutral zone
long_setup = (z < -z_entry)                      # z < -2.0
exit_setup = (abs(z) < z_exit)                   # |z| < 1.0  (gap 1.0 → 2.0 tự nhiên)
```

---

## 5.9 Neutral Zone giữa Entry và Exit Threshold

Luôn có một khoảng cách (gap) giữa ngưỡng entry và ngưỡng exit để tránh overlap.

### Đúng

```python
z_entry = 2.0       # vào lệnh khi |z| > 2.0
z_exit = 1.0         # thoát khi |z| < 1.0
# Gap: [1.0, 2.0] — không entry, không exit → giữ position
```

### Sai

```python
z_entry = 2.0       # vào lệnh khi |z| > 2.0
z_exit = 2.0        # thoát khi |z| < 2.0 — SÁT entry
# Nguy cơ: chênh lệch 1 tick là flip-flop entry/exit liên tục
```

---

# 6. AI Agent Compliance Checklist

Trước khi sinh bất kỳ file `.py` nào, AI Agent phải xác nhận đã đáp ứng đầy đủ các điều kiện sau:

- [ ] Đã đọc toàn bộ tài liệu trong `data/`
- [ ] Đã đọc `syntax/data_syntax.md`
- [ ] Đã đọc `syntax/syntax_guide.md`
- [ ] Đã đọc các catalog trong `syntax/`
- [ ] Đã tham khảo `template_example/`
- [ ] Chỉ sử dụng API chính thức của XNOQuant
- [ ] Không sử dụng thư viện hoặc framework ngoài nếu không được yêu cầu
- [ ] Không giữ lại các type hint từ tài liệu (`SeriesT`, `-> SeriesT`, ...)
- [ ] Không sử dụng biến `open`
- [ ] Chỉ sử dụng `self.set_positions()` để đặt lệnh
- [ ] Luôn đặt lệnh `Exit` trước `Long` và `Short`
- [ ] `exit_setup` không chứa condition mà `entry_setup` đang cần (tránh mutual cancellation)
- [ ] Trend/regime signal (`trend_up`, `ranging`, ...) là entry gate, không nhét vào `exit_setup`
- [ ] Có guard mutual exclusion giữa long và short (`assert not (long_signal & short_signal).any()`)
- [ ] Entry và exit không dùng mixed `crossed_*` / level trên cùng 1 biến
- [ ] Có neutral zone giữa entry và exit threshold (`z_exit < z_entry`, `adx_exit < adx_entry`, ...)
- [ ] `long_setup`/`short_setup` gốc được giữ nguyên, signal masked lưu vào biến riêng (`long_signal`, `short_signal`)
- [ ] Mã nguồn có thể chạy trực tiếp trên nền tảng XNOQuant mà không cần chỉnh sửa thêm.
