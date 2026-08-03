# XNOQuant — Strategy Framework Specification (Round 2)

Tài liệu này định nghĩa **Framework Specification** chuẩn cho mọi chiến lược giao dịch định lượng
trên nền tảng **XNOQuant** trong **Round 2 — Fundamental Alpha Arena** (daily equity research).

> **Nguồn tham chiếu chính thức:** `agent/stage_2_guideline.md` (round rules).
> **Nguồn parameter canonical:** `syntax/time_series/parameters.md` + `syntax/cross_sectional/parameters.md` (profiles + evidence status).
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
financial_expenses = self.data.fun_is_financial_expenses_quarterly
equity = self.data.fun_bs_owners_equity_quarterly
total_assets = self.data.fun_bs_total_assets_quarterly
operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
```

> Chỉ dùng field có trong `syntax/data_syntax.md`. Không dùng
> `fun_is_total_operating_income_*` hoặc `fun_bs_shareholders_equity_*` vì hai
> tên này không tồn tại trong catalog Round 2.

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
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual
        total_assets = self.data.fun_bs_total_assets_annual

        # STEP 2 — Features
        ema8 = self.feat.ema(close, timeperiod=8)
        ema12 = self.feat.ema(close, timeperiod=12)
        ema24 = self.feat.ema(close, timeperiod=24)
        ema36 = self.feat.ema(close, timeperiod=36)

        # STEP 3 — Persistent quality + multi-horizon trend
        roa = net_profit / total_assets
        fundamentals_known = (
            self.op.notna(net_profit)
            & self.op.notna(total_assets)
            & (total_assets > 0)
            & self.op.notna(roa)
        )
        quality = fundamentals_known & (net_profit > 0) & (roa > 0.01)

        weak_long = quality & (close > ema36) & (ema12 > ema36)
        strong_long = weak_long & (ema8 > ema24)
        exit_setup = (close < ema36) | (roa < 0)

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

Vì vậy entry và exit nên được thiết kế **loại trừ nhau** trong phần lớn trường
hợp. Nếu chúng cùng đúng, lệnh Long gọi sau sẽ thắng; không được giả định rằng
`exit_setup` luôn có ưu tiên cao nhất chỉ vì được gọi trước.

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

## 7.4 Exit đơn giản, Entry 3-6 conditions

- **Exit:** tối đa 2-3 điều kiện OR (slow-trend break + persistent quality mất hiệu lực). Ví dụ:
  ```python
  exit_setup = (close < ema36) | (roa < 0)
  ```
- **Entry:** 3-6 conditions là sweet spot — persistent quality + medium trend,
  sau đó thêm fast confirmation cho strong entry:
  ```python
  weak_long = quality & (close > ema36) & (ema12 > ema36)
  strong_long = weak_long & (ema8 > ema24)
  ```

## 7.5 Step-change chỉ là event signal

Fundamentals được forward-fill trên daily timeline, nên `pct_change` chỉ khác 0
ở ngày report mới xuất hiện. Đây là **event signal**, không phải quality state
kéo dài và cũng không phải tăng trưởng ngày-ngày.

```python
profit_growth = self.op.pct_change(net_profit, periods=1)
report_known = self.op.notna(net_profit) & self.op.notna(profit_growth)
report_trigger = report_known & (net_profit > 0) & (profit_growth > 0)
```

- Không `fillna(..., value=0)` cho fundamental; missing là unavailable.
- Không dùng report-step làm hard quality state giữa hai kỳ báo cáo.
- Với EPS/profit có thể âm hoặc đổi dấu, raw `pct_change` có thể đảo nghĩa hoặc
  tạo outlier. Ưu tiên positive-level guard hoặc delta được scale bằng assets /
  equity dương khi luận điểm cho phép.
- Report trigger nên là overlay độc lập; persistent quality nên dùng level/ratio
  như ROA, CFO dương hoặc cash conversion.

## 7.6 Parameter profiles

`syntax/time_series/parameters.md` + `syntax/cross_sectional/parameters.md` là nguồn canonical duy nhất cho period, threshold và
sizing parameter. Tài liệu này không duy trì một danh sách parameter song song.

Quy tắc:

- Chọn profile theo archetype: active momentum, price/volume, balanced
  fundamental, cash-flow quality hoặc stable hold.
- Luôn truyền explicit `timeperiod=`, `window=`, `fastperiod=`, `slowperiod=` và
  `signalperiod=`; không dựa vào implementation default.
- Equity examples là bằng chứng tham khảo, không tự động biến parameter thành
  `PASS`. Dùng evidence labels trong `syntax/time_series/parameters.md` + `syntax/cross_sectional/parameters.md`.
- MACD time-series phải unpack đủ ba outputs theo contract canonical.
- Mỗi ablation chỉ thay một dimension: period, threshold, sizing hoặc exit.

---

# 8. Effective Daily-Equity Framework

Phần này đúc kết từ các example equity Round 2 và kết quả nghiên cứu
VN-LARGE-CAP. Không áp dụng logic intraday futures trong `(Old)vnfuture/`.

## 8.1 Kiến trúc khuyến nghị

```text
Availability
→ Persistent quality
→ Medium trend regime
→ Fast trend confirmation
→ Tiered long-only sizing
→ Slow-trend / quality exit
```

### Layer A — Availability

```python
available = (
    self.op.notna(numerator)
    & self.op.notna(denominator)
    & (denominator > 0)
)
```

Không dùng `fillna(..., value=0)` để làm fundamental trở nên eligible.

### Layer B — Persistent quality

Mỗi strategy chỉ nên chọn một quality thesis chính hoặc một OR có luận điểm:

```python
roa_quality = available & (net_profit > 0) & (roa > 0.01)

cash_quality = (
    cash_available
    & (operating_cash_flow > 0)
    & (net_profit > 0)
    & (cash_conversion > 0.5)
)

quality = roa_quality | cash_quality
```

Không bắt buộc ROA, cash conversion, capital ratio, EPS growth và volume cùng
đúng trong một entry. Quá nhiều AND làm signal thưa và khó xác định nguồn alpha.

### Layer C — Multi-horizon trend

```python
ema8 = self.feat.ema(close, timeperiod=8)
ema12 = self.feat.ema(close, timeperiod=12)
ema24 = self.feat.ema(close, timeperiod=24)
ema36 = self.feat.ema(close, timeperiod=36)

fast_trend = ema8 > ema24
medium_trend = ema12 > ema36
price_regime = close > ema36
```

Multi-horizon trend là baseline ưu tiên cho large-cap: signal liên tục, ít phụ
thuộc report-day và giảm false breakout so với một indicator đơn lẻ.

### Layer D — Sizing và exit

```python
weak_long = quality & medium_trend & price_regime
strong_long = weak_long & fast_trend
exit_setup = (close < ema36) | quality_failure

self.set_positions(exit_setup, position=0)
self.set_positions(weak_long, position=0.5)
self.set_positions(strong_long, position=1)
```

- `0.5`: quality hợp lệ + medium trend.
- `1.0`: thêm fast trend confirmation.
- `0.0`: slow trend hoặc persistent quality thật sự mất hiệu lực.
- Volume chỉ nên là optional sizing/entry confirmation; không exit chỉ vì một
  ngày volume dưới SMA, tránh churn `0.5 ↔ 1.0`.

## 8.2 Sector awareness

VN-LARGE-CAP gồm bank, bảo hiểm, chứng khoán và non-financial. Không áp một hard
threshold kế toán cho mọi ngành:

- Non-financial: CFO/net profit, ROA, cash return phù hợp hơn.
- Bank: tránh dùng CFO generic làm hard requirement; ưu tiên profitability và
  capital field có ý nghĩa ngân hàng khi catalog hỗ trợ.
- Bảo hiểm: premium, claims, insurance/investment profit.
- Chứng khoán: fee, commission, derivatives/FVTPL income và expense pressure.

Nếu không có sector mask, ưu tiên quality có ý nghĩa rộng hoặc tạo strategy
riêng theo accounting archetype.

## 8.3 Complexity limits

- Base entry: tối đa 4 điều kiện kinh tế chính.
- Strong entry: thêm tối đa 2 confirmation.
- Exit: tối đa 3 nhánh OR.
- ATR chỉ dùng khi có vai trò risk/volatility cụ thể; `atr > 0` chỉ là data guard,
  không phải alpha.
- Volume là confirmation, không thay thế quality hoặc trend.

## 8.4 Research workflow bắt buộc

1. Xây baseline đơn giản (ví dụ dual trend).
2. Thêm đúng một component mỗi iteration.
3. Chạy ablation: baseline → +ROA → +cash conversion → +volume sizing.
4. So sánh CAGR, Sharpe, Calmar, MaxDD, Profit Factor và turnover nếu có.
5. Chỉ giữ component nếu cải thiện risk-adjusted metrics ổn định.
6. Chọn canonical profile và robustness range từ `syntax/time_series/parameters.md` + `syntax/cross_sectional/parameters.md`; không
   copy một parameter family sang archetype khác nếu chưa có ablation.
7. Không tối ưu đồng thời period, threshold, sizing và exit.
8. Không đảo chiều hoặc thêm điều kiện chỉ để cứu một backtest.

---

# 9. Example Reference (Round 2)

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

# 10. AI Agent Compliance Checklist

Trước khi sinh bất kỳ file `.py` nào, AI Agent phải xác nhận:

- [ ] Đã đọc `agent/stage_2_guideline.md`
- [ ] Đã đọc `syntax/data_syntax.md`, `syntax/time_series/feature_syntax.md`, `syntax/time_series/operations_syntax.md`, `syntax/cross_sectional/feature_syntax.md`, `syntax/cross_sectional/operations_syntax.md`
- [ ] Đã đọc `syntax/time_series/parameters.md` + `syntax/cross_sectional/parameters.md` và chọn đúng canonical profile cho archetype
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
- [ ] Fundamental level/ratio dùng làm persistent quality; report-step chỉ là event overlay
- [ ] Entry không quá 4 điều kiện kinh tế chính; strong thêm tối đa 2 confirmation
- [ ] Đã chạy ablation trước khi giữ component mới
- [ ] Đã kiểm tra sector meaning của accounting ratio
- [ ] Mọi period/window đều explicit; không dựa vào default implementation
- [ ] MACD time-series unpack `(macd, macd_signal, histogram)` đúng contract
- [ ] Không giữ type hints từ tài liệu (`SeriesT`, `PanelT`, ...)
- [ ] Không dùng biến `open`
- [ ] `time_series`: chỉ dùng `self.set_positions()`, bounds `[0, +1]`, thứ tự Exit → Long
- [ ] `cross_sectional`: chỉ dùng `self.set_portfolio_positions()`, market-neutral
- [ ] Metadata docstring nêu luận điểm kinh tế, không mô tả lại code
- [ ] Tránh turnover cao (fees bị phạt nặng)
- [ ] Mã nguồn chạy được trên nền tảng XNOQuant không cần chỉnh sửa thêm
