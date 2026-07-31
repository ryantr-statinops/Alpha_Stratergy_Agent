# XNOQuant — Strategy Framework Specification (Round 2)

Tài liệu này định nghĩa **Framework Specification** chuẩn cho mọi chiến lược giao dịch định lượng
trên nền tảng **XNOQuant** trong **Round 2 — Fundamental Alpha Arena** (daily equity research).

> **Nguồn tham chiếu chính thức:** `agent/stage_2_guideline.md` (round rules).
> Mọi AI Agent khi tạo mã nguồn (`.py`) trong thư mục `output/` **phải tuân thủ tuyệt đối**
> các quy ước và ràng buộc kỹ thuật được mô tả trong tài liệu này.

---

## Mode Contract

Mỗi strategy **phải dùng đúng 1 mode** — không trộn 2 mode trong cùng 1 strategy.

| Mode | Câu hỏi nghiên cứu | Data shape | Position API | Bounds |
|---|---|---|---|---|
| `time_series` | Khi nào nên giữ mỗi cổ phiếu? | 1 time series mỗi field mỗi symbol | `self.set_positions(...)` | Long-only `[0, +1]` |
| `cross_sectional` | Phân bổ vốn thế nào giữa các cổ phiếu? | panel time × symbol | `self.set_portfolio_positions(...)` | Market-neutral; weight âm/dương đều được |

Quy tắc:

- Tên mode chính xác là `time_series`, không phải `timeseries`.
- Field `time_series` **không có suffix**: `self.data.pv_close`.
- Field `cross_sectional` **luôn có suffix `_panel`**: `self.data.pv_close_panel`.
- **Không trộn** field series và field panel trong cùng strategy.
- Panel luôn có time trên hàng và symbols trên cột — kể cả với universe 1 symbol.

---

## Universes Hợp Lệ

Chỉ 3 universe sau được tính điểm:

| Universe | Segment | Frequency |
|---|---|---|
| `VN-SMALL-CAP` | cổ phiếu small-cap Việt Nam | Daily |
| `VN-MID-CAP` | cổ phiếu mid-cap Việt Nam | Daily |
| `VN-LARGE-CAP` | cổ phiếu large-cap Việt Nam | Daily |

---

# 1. Architecture Overview

Mỗi chiến lược được xây dựng theo pipeline gồm **4 tầng**:

```text
                 XNOQuant Strategy Pipeline (Round 2)

┌──────────────────────────────────────────────────────────┐
│ Layer 1: Raw Data                                        │
│ self.data                                                │
│ • pv_*        (OHLCV + VN30)                             │
│ • fun_is_*    (Income Statement, quarterly/annual)       │
│ • fun_bs_*    (Balance Sheet, quarterly/annual)          │
│ • fun_cf_*    (Cash Flow, quarterly/annual)              │
└──────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│ Layer 2: Feature Engineering                             │
│ self.feat                                                │
│ • time_series:  ema(close, timeperiod=8)                 │
│ • cross_sectional: ema_panel(series)                     │
└──────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│ Layer 3: Trading Logic                                   │
│ self.op                                                  │
│ • time_series:  pct_change, fillna, crossed_above, ...   │
│ • cross_sectional: rank_cs_panel, portfolio_weights_panel│
└──────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│ Layer 4: Position Sizing                                 │
│ • time_series:    self.set_positions(cond, position)     │
│ • cross_sectional: self.set_portfolio_positions(weights) │
└──────────────────────────────────────────────────────────┘
```

Mọi chiến lược phải đi qua **đúng thứ tự** bốn tầng trên.

---

# 2. Standard Strategy Template

Mọi file chiến lược phải theo cấu trúc sau.

## 2.1 Class Structure

```python
class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        ...
```

- **Không dùng `__init__`.**
- Không dùng class attributes window (vòng 1) trừ khi cần — các example Round 2 hard-code
  `timeperiod` ngay trong lời gọi `self.feat.*`.

## 2.2 Data Access Patterns

> Catalog đầy đủ tại [`syntax/data_syntax.md`](../syntax/data_syntax.md).

### Price / Volume (time_series — không suffix)
```python
close = self.data.pv_close
high = self.data.pv_high
low = self.data.pv_low
volume = self.data.pv_volume
```

### Fundamentals (time_series — không suffix)
```python
net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly
eps = self.data.fun_is_eps_basis_quarterly
operating_income = self.data.fun_is_total_operating_income_quarterly
financial_expenses = self.data.fun_is_financial_expenses_quarterly
equity = self.data.fun_bs_shareholders_equity_quarterly
total_assets = self.data.fun_bs_total_assets_quarterly
operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
```

### Cross-Sectional (cross_sectional — có `_panel` suffix)
```python
close = self.data.pv_close_panel
net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly_panel
```

## 2.3 Template — time_series mode

```python
"""
name:    VnXxxYyy
summary: <một câu mô tả chiến lược ngắn>
idea:    <luận điểm kinh tế thực sự, không phải mô tả lại code>
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # STEP 1 — Raw data
        close = self.data.pv_close
        volume = self.data.pv_volume

        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly
        eps = self.data.fun_is_eps_basis_quarterly

        # STEP 2 — Features
        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)
        volume_base = self.feat.sma(volume, timeperiod=10)

        # STEP 3 — Trading logic (fundamentals step on report updates)
        profit_growth = self.op.fillna(self.op.pct_change(net_profit, periods=1), value=0)
        eps_growth = self.op.fillna(self.op.pct_change(eps, periods=1), value=0)

        weak_long = (close > ema_slow) & (ema_fast > ema_slow) & (profit_growth > -0.02) & (eps_growth > -0.02)
        strong_long = weak_long & (profit_growth > 0) & (eps_growth > 0) & (volume > volume_base)
        exit_setup = (ema_fast < ema_slow) | (profit_growth < -0.05)

        # STEP 4 — Position sizing (exit first, then half, then full)
        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
```

---

# 3. Framework Layers

## Layer 1 — Raw Data (`self.data`)

Chỉ được lấy dữ liệu từ `self.data`. Không tự sinh dữ liệu ngoài framework.

## Layer 2 — Feature Engineering (`self.feat`)

Toàn bộ chỉ báo phải gọi từ `self.feat`. Không tự viết lại indicator.

## Layer 3 — Trading Logic (`self.op`)

Logic giao dịch chỉ dùng:

- toán tử Bitwise (`&`, `|`, `~`)
- toán tử so sánh
- các hàm trong `self.op`

## Layer 4 — Position Sizing

- `time_series`: chỉ dùng `self.set_positions(condition, position)`.
- `cross_sectional`: chỉ dùng `self.set_portfolio_positions(weights)`.

Không dùng bất kỳ API đặt lệnh nào khác.

---

# 4. Position Sizing Rules

## 4.1 `time_series` — `self.set_positions`

| Position | Trạng thái | Mô tả |
|-----------|-----------|-------|
| `1.0` | Full Long | 100% vốn vào vị thế Long |
| `0.5` | Partial Long | 50% Long |
| `0.0` | Flat / Exit | Thoát toàn bộ |

> Bounds: **Long-only `[0, +1]`**. Không dùng `-1`/`-0.5` trong Round 2 time_series.

### Thứ tự gọi bắt buộc: Exit → Long

```python
self.set_positions(exit_setup, position=0)     # exit trước
self.set_positions(weak_long, position=0.5)    # half size
self.set_positions(strong_long, position=1)    # full size — override
```

Long được gọi sau exit để override khi điều kiện vào lệnh thoả.

## 4.2 `cross_sectional` — `self.set_portfolio_positions`

- Market-neutral: cả weight âm và dương đều hợp lệ.
- Nên xây qua `self.op.portfolio_weights_panel(signal, method='rank_demean_l1', mask=...)`.
- Symbol ngoài universe nhận weight 0; net exposure ≈ 0; gross exposure chuẩn hoá về 1.

---

# 5. Point-in-Time Rules cho Fundamental Data

Fundamentals được align theo market timeline bởi **ngày công bố** (publication date).
Observation mới nhất được forward-fill tới khi có report mới hơn.

Bắt buộc:

1. **Chỉ dùng report sau khi nó được công bố.**
2. **Không giả định** số liệu cuối quý đã biết tại ngày cuối quý.
3. **Không bao giờ** shift fundamental data backward; không backfill.
4. **Xem missing fundamentals là unavailable, không phải zero** — dùng `.notna()`.
5. **Dùng ratio** khi so sánh các công ty khác quy mô.
6. **Tính rõ stale fundamentals** trong research thesis.
7. Trước khi xây ratio: yêu cầu `.notna()` và **denominator dương**; không chia cho 0
   hoặc denominator âm nếu không có lý do kinh tế rõ ràng.
8. **Lưu ý ngành:** bank, bảo hiểm, chứng khoán, và công ty phi tài chính có quy ước
   kế toán khác nhau — không giả định 1 raw accounting ratio so sánh được giữa mọi ngành.

---

# 6. Strategy & Sandbox Rules

**Được phép:**

- Signal logic deterministic, vectorized, causal (chỉ dùng quá khứ).
- Các primitive được tài liệu hoá: `self.data`, `self.feat`, `self.op`.

**Không được phép:**

- Row-by-row loops, comprehensions, lambdas, helper functions.
- Import Pandas, NumPy, Polars, networking, filesystem libraries.
- `print`, `open`, `eval`, `exec`, hoặc bất kỳ hidden runtime access.
- Negative shifts, backfill, centered rolling windows, hoặc bất kỳ future observation.
- Global aggregations như `.mean()`, `.rank()`, `.quantile()`, `.sort_values()`.

**Ngoài ra:**

- Tránh rebalance quá mức — turnover và fees ảnh hưởng trực tiếp tới score.
- Docstring metadata phải nêu **luận điểm kinh tế thực sự**, không mô tả lại code.

---

# 7. Strict Technical Guardrails

## 7.1 Variable Naming

Không bao giờ đặt biến `open`. Dùng `open_price` hoặc `op_price`.

## 7.2 Bỏ Documentation Type Hints

Các tài liệu trong `syntax/` có thể chứa `SeriesT`, `PanelT`, `-> SeriesT` — các ký hiệu này
**chỉ dùng cho tài liệu**, không được xuất hiện trong mã nguồn sinh ra.

Ví dụ: `self.feat.ema(close, timeperiod=8)` — không viết `ema(source: SeriesT = None)`.

## 7.3 Position Order Priority

Trong `time_series`, thứ tự gọi `set_positions()` luôn là **Exit → Long** (xem §4.1).
Không đảo thứ tự này.

## 7.4 Exit đơn giản, Entry 3-4 conditions

- **Exit:** tối đa 2-3 điều kiện OR (trend break + profit/eps giảm mạnh). Ví dụ:
  ```python
  exit_setup = (ema_fast < ema_slow) | (profit_growth < -0.05)
  ```
- **Entry:** 3-6 conditions là sweet spot — kết hợp price trend + fundamental growth + volume.
  Ví dụ từ `VnTop30SimpleFundamentalTrend.py`:
  ```python
  weak_long = (close > ema_slow) & (ema_fast > ema_slow) & (profit_growth > -0.02) & (eps_growth > -0.02)
  ```

## 7.5 Ngưỡng Step-change cho Fundamentals

Vì fundamentals step-change trên daily timeline (chỉ đổi khi có report mới), dùng
`self.op.pct_change(series, periods=1)` + `self.op.fillna(..., value=0)` để đo sự thay đổi
khi giá trị mới được công bố — **không phải** tăng trưởng ngày-ngày thực sự.

```python
profit_growth = self.op.fillna(self.op.pct_change(net_profit, periods=1), value=0)
```

---

# 8. Example Reference (Round 2)

| Universe folder | File | Luận điểm chính |
|---|---|---|
| `VN-TOP10-BANK/` | `VnBankActiveEarningsTrend.py` | earnings + price trend |
| `VN-TOP10-BANK/` | `VnBankActiveRSIMACDQuality.py` | RSI/MACD + quality |
| `VN-TOP10-BANK/` | `VnBankPriceFundamentalMomentum.py` | price + fundamental momentum |
| `VN-TOP10-BANK/` | `VnBankPriceVolumeBreakout.py` | price/volume breakout |
| `VN-TOP10-BANK/` | `VnBankPriceVolumeTrend.py` | price/volume trend |
| `VN-TOP10-INSURANCE/` | `VnInsurancePremiumMomentum.py` | premium growth + price |
| `VN-TOP10-INSURANCE/` | `VnInsurancePremiumQualityHold.py` | premium quality hold |
| `VN-TOP10-INSURANCE/` | `VnInsuranceRSIPremiumRecovery.py` | RSI recovery + premium guardrail |
| `VN-TOP10-SECURITIES/` | `VnSecuritiesCommissionMomentum.py` | commission/derivatives + profit |
| `VN-TOP10-SECURITIES/` | `VnSecuritiesFastIncomeTurnover.py` | faster income filter + trend |
| `VN-TOP30/` | `VnTop30SimpleFundamentalTrend.py` | profit + EPS + trend |
| `VN-TOP30/` | `VnTop30QualityLeverageSpread.py` | profit vs leverage spread |
| `VN-TOP30/` | `VnTop30QualityBreakout.py` | price breakout + quality |
| `VN-TOP30/` | `VnTop30CashFlowAcceleration.py` | cash flow + earnings acceleration |

> Các example vòng 1 (`(Old)vnfuture/`) là intraday futures — **không dùng làm chuẩn cho Round 2**.
> Round 2 là daily equity, long-only, fundamentals point-in-time.

---

# 9. AI Agent Compliance Checklist

Trước khi sinh bất kỳ file `.py` nào, AI Agent phải xác nhận:

- [ ] Đã đọc `agent/stage_2_guideline.md`
- [ ] Đã đọc `syntax/data_syntax.md`, `syntax/feature_syntax.md`, `syntax/operations_syntax.md`
- [ ] Đã tham khảo `template_example/VN-*/`
- [ ] Chỉ dùng 1 mode: `time_series` hoặc `cross_sectional` — không trộn
- [ ] Field đúng mode: time_series không suffix / cross_sectional có `_panel`
- [ ] Universe hợp lệ: VN-SMALL-CAP / VN-MID-CAP / VN-LARGE-CAP
- [ ] Chỉ dùng API chính thức của XNOQuant
- [ ] Không import thư viện ngoài, không loops/lambdas/helper functions
- [ ] Không dùng global aggregations (`.mean()`, `.rank()`, ...)
- [ ] Không dùng future observation / backfill / negative shift
- [ ] Fundamentals chỉ dùng sau ngày công bố (point-in-time)
- [ ] Missing fundamentals xử lý bằng `.notna()`, không phải zero
- [ ] Ratio: yêu cầu denominator dương; dùng `safe_divide_panel` nếu cross_sectional
- [ ] Không giữ type hints từ tài liệu (`SeriesT`, `PanelT`, ...)
- [ ] Không dùng biến `open`
- [ ] `time_series`: chỉ dùng `self.set_positions()`, bounds `[0, +1]`, thứ tự Exit → Long
- [ ] `cross_sectional`: chỉ dùng `self.set_portfolio_positions()`, market-neutral
- [ ] Metadata docstring nêu luận điểm kinh tế, không mô tả lại code
- [ ] Tránh turnover cao (fees bị phạt nặng)
- [ ] Mã nguồn chạy được trên nền tảng XNOQuant không cần chỉnh sửa thêm
