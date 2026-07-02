# ALPHA_BOT - Quantitative Strategy Builder Engine

## 1. Project Overview & Purpose

Dự án này là môi trường nghiên cứu và phát triển chiến lược đầu tư định lượng (Quantitative Trading) dành riêng cho nền tảng **XNOQuant**.

Mục đích cốt lõi của không gian làm việc này là giúp AI Agent đọc hiểu sâu sắc cấu trúc cú pháp, dữ liệu đầu vào và các hàm chức năng được nền tảng cung cấp. Từ đó, AI có thể tự động hóa quy trình lên ý tưởng (Alpha Generation), lập kế hoạch kiểm thử và viết mã nguồn chiến lược hoàn chỉnh một cách chính xác mà không vi phạm các quy tắc của hệ thống.

---

## 2. Project Structure

```text
ALPHA_BOT/
├── data/                   # Tài liệu về dữ liệu đầu vào (OHLCV, Futures, VN30, DJI)
├── feature/                # Danh mục chỉ báo kỹ thuật (EMA, RSI, BBands, Hikkake, ...)
├── operations/             # Danh mục toán tử xử lý chuỗi thời gian (crossed_above, fillna, ...)
├── template_example/       # Framework chuẩn + strategy mẫu chạy được trên XNOQuant
│   └── strategy_framework.md   # **Master specification** — đọc đầu tiên
├── idea/                   # Nơi lưu trữ các ý tưởng nghiên cứu (.md)
│   ├── planning_alpha/     # Kế hoạch phát triển Alpha theo từng chủ đề
│   ├── hypothesis/         # Giả thuyết kiểm thử, tiêu chí chấm điểm, design guidelines
│   └── stage_overview/     # Ghi lại tiến độ và lịch sử phiên làm việc
├── output/                 # Mã nguồn chiến lược hoàn chỉnh (.py) — theo thesis group / timeframe
│   ├── index.csv           # Master manifest tra cứu strategy
│   ├── thesis_01_momentum/      # Momentum strategies (5, 15, 30, 60 min)
│   ├── thesis_02_trend/         # Trend following strategies
│   ├── thesis_03_mean_reversion/ # Mean reversion strategies
│   ├── thesis_04_breakout/      # Breakout strategies
│   ├── thesis_05_cross_market/  # Cross-market (VN30, DJI) strategies
│   ├── thesis_06_volume_flow/   # Volume & flow strategies
│   ├── thesis_07_intraday_session/ # Intraday session strategies
│   └── thesis_08_multifactor/   # Multi-factor composite strategies
├── tools/                  # Batch generator scripts
│   └── generate_strategies.py
└── README.md               # Tài liệu hướng dẫn dành cho AI Agent
```

### 8 Thesis Groups

| # | Thesis | Target | Timeframes |
|:-:|--------|--------|:----------:|
| 01 | **Momentum** | Giá tiếp diễn xu hướng ngắn hạn — ROC, price acceleration, VN30 confirm | 5, 15, 30, 60 |
| 02 | **Trend Following** | Giao dịch cùng xu hướng đã xác nhận — MA crossover, MACD, ADX filter | 5, 15, 30, 60 |
| 03 | **Mean Reversion** | Giá quay về trung bình — quantile extremes, RSI, BBands | 5, 15, 30, 60 |
| 04 | **Breakout** | Phá vỡ vùng tích lũy — quantile breakout, Donchian, range expansion | 5, 15, 30, 60 |
| 05 | **Cross-Market** | VN30 + DJI ảnh hưởng VN30F1M — relative strength, global spillover | 15, 30, 60 |
| 06 | **Volume & Flow** | Institutional flow signals — OI, matched volume/value | 15, 30, 60 |
| 07 | **Intraday Session** | Hành vi giá đặc thù theo phiên — open drive, lunch revert, close squeeze | 5, 15 |
| 08 | **Multi-Factor** | Kết hợp nhiều tín hiệu — z-score composite, multi-layer confirmation | 15, 30, 60 |

### Competition Context

Dự án hướng tới **Vietnam Quant Challenge 2026** trên nền tảng XNOQuant.  
**Target:** 500+ chiến lược Published đạt Sharpe ≥ 1.2, CAGR ≥ 25%, Sortino ≥ 1.5, Calmar ≥ 0.9.  
**Cách tính điểm:** Sharpe > CAGR > Sortino > Calmar > Max DD > VaR > CVaR > Ulcer Index > Cost > Correlation.

---

## 3. Knowledge Base Reference (AI Onboarding Guide)

Trước khi thực hiện bất kỳ yêu cầu nào từ người dùng, AI Agent **bắt buộc** phải đọc và phân tích các thư mục sau để xây dựng ngữ cảnh (Context) làm việc.

### `data/`

- Hiểu cách truy cập dữ liệu thị trường.
- Ví dụ: `self.data.pv_close`, `self.data.fut_matched_volume_vn30f1m_1d`.
- Không sử dụng tên biến trùng với từ khóa của hệ thống.
  - ✅ `open_price`
  - ❌ `open`

#### Danh sách trường dữ liệu VnFuture (Hợp đồng tương lai VN30F1M)

| Trường | Ý nghĩa |
|--------|---------|
| `fut_matched_volume_vn30f1m_1d` | Khối lượng khớp lệnh |
| `fut_matched_value_vn30f1m_1d` | Giá trị khớp lệnh |
| `fut_agreed_volume_vn30f1m_1d` | Khối lượng thỏa thuận |
| `fut_agreed_value_vn30f1m_1d` | Giá trị thỏa thuận |
| `fut_total_volume_vn30f1m_1d` | Tổng khối lượng (khớp lệnh + thỏa thuận) |
| `fut_total_value_vn30f1m_1d` | Tổng giá trị (khớp lệnh + thỏa thuận) |
| `fut_open_interest_vn30f1m_1d` | Hợp đồng mở (Open Interest) |

Chi tiết xem tại [`data/VnFuture.md`](data/VnFuture.md).

#### Đặc thù thị trường Việt Nam

Tài liệu [`data/vietnam_market_characteristics.md`](data/vietnam_market_characteristics.md) phân tích chi tiết:
- Retail 80-90% → herding, overreaction, panic sell
- Đòn bẩy phái sinh 1:6-1:8 → margin call cascade, forced momentum
- Session microstructure → pre-cash, lunch dead zone, ATC manipulation
- Basis volatility → cross-market signal
- **Mapping table**: đặc thù → signal → entry/exit rule → templates áp dụng
- **Sharpe optimization rules**: công thức đạt Sharpe ≥ 2.0
- **Parameter guidelines**: regime detection, tham số từng chế độ thị trường

#### Danh sách trường VN30 Index

| Trường | Ý nghĩa |
|--------|---------|
| `pv_vn30_open` | VN30 Open |
| `pv_vn30_high` | VN30 High |
| `pv_vn30_low` | VN30 Low |
| `pv_vn30_close` | VN30 Close |
| `pv_vn30_volume` | VN30 Volume |

#### Danh sách trường Dow Jones Index

| Trường | Ý nghĩa |
|--------|---------|
| `pv_dji_open` | DJI Open |
| `pv_dji_high` | DJI High |
| `pv_dji_low` | DJI Low |
| `pv_dji_close` | DJI Close |
| `pv_dji_volume` | DJI Volume |

### `feature/`

- Tra cứu toàn bộ các chỉ báo kỹ thuật được nền tảng hỗ trợ.
- Chỉ sử dụng các hàm có sẵn trong thư mục này khi xây dựng chiến lược.

### `operations/`

- Tra cứu các toán tử xử lý dữ liệu chuỗi thời gian.
- Khi sinh mã nguồn, loại bỏ các khai báo kiểu dữ liệu nội bộ của hệ thống như:

```python
: SeriesT = None
```

Ví dụ:

```python
# Không sử dụng
def EMA(source: SeriesT = None):

# Sử dụng
EMA(source)
```

### `template_example/`

Đây là framework chuẩn của XNOQuant.

**File quan trọng nhất:** [`template_example/strategy_framework.md`](template_example/strategy_framework.md) — định nghĩa toàn bộ cấu trúc, quy ước, guardrails mà AI Agent phải tuân thủ khi sinh strategy.

Mọi chiến lược được sinh ra phải:

- Kế thừa từ lớp `CustomStrategy(SimpleAlgorithm)`
- Sử dụng cấu trúc giống các file mẫu
- Định nghĩa logic bên trong:

```python
def __algorithm__(self):
```

Tham khảo thêm các file mẫu `.py` trong thư mục này.

---

## 4. Operational Workflow

AI Agent phải tuân thủ nghiêm ngặt quy trình gồm **5 bước** dưới đây.

### Bước 1. Alpha Generation

- Tiếp nhận yêu cầu hoặc ý tưởng giao dịch từ người dùng.
- Chuyển từng ý tưởng thành các tài liệu Markdown.
- Lưu các tài liệu này vào thư mục:

```text
idea/
```

---

### Bước 2. Planning & Hypothesis

#### Planning

- Phân tích từng ý tưởng.
- Lập kế hoạch phát triển Alpha.
- Lưu vào:

```text
idea/planning_alpha/
```

#### Hypothesis Loop

Sử dụng framework kiểm thử tại [`idea/hypothesis/hypothesis_framework.md`](idea/hypothesis/hypothesis_framework.md) — tài liệu này định nghĩa:

- **Acceptance Criteria:** Sharpe ≥ 1.2, CAGR ≥ 25%, Sortino ≥ 1.5, PF ≥ 1.7, Calmar ≥ 0.9, Max DD ≥ -40%, VaR ≥ -5%, CVaR ≥ -6%, Ulcer Index ≤ 12, Cost ≤ 1%, Correlation ≤ 0.8
- **Multi-Stage Validation:** Train 70% → Test 30% (bắt buộc)
- **Hard Rules:** Risk, drawdown, signal validation
- **Scorecard:** Chấm điểm 10 metrics, PASS = đạt ≥ 8/10

AI cần thực hiện vòng lặp nghiên cứu:

1. Đọc các giả thuyết hiện có trong:

```text
idea/hypothesis/
```

2. Chọn các kịch bản kiểm thử phù hợp.

3. Đề xuất thêm:

- tiêu chí kiểm thử
- edge case
- giả thuyết mới
- điều kiện thất bại

4. Quay lại cập nhật kế hoạch Alpha.

5. Hoàn thiện phương án cuối cùng.

---

### Bước 3. User Review

Trước khi viết mã nguồn, AI phải:

- Trình bày đầy đủ logic chiến lược.
- Giải thích ý tưởng.
- Mô tả logic toán học.
- Trình bày kế hoạch kiểm thử.

Sau đó:

- tiếp nhận phản hồi
- chỉnh sửa
- lặp lại

Cho đến khi người dùng chính thức **Approve**.

---

### Bước 4. Chain-of-Thought & Coding

Sau khi được phê duyệt:

- Chuyển logic thành mã Python.
- Chỉ sử dụng:
  - các hàm trong `feature/`
  - các hàm trong `operations/`
- Tuân thủ tuyệt đối cấu trúc trong [`template_example/strategy_framework.md`](template_example/strategy_framework.md):
  - Class `CustomStrategy(SimpleAlgorithm)`, method `__algorithm__`
  - Exit → Long → Short order
  - Không `import pandas`, không `SeriesT`, không biến `open`
- Dùng compliance checklist ở cuối `strategy_framework.md` để self-verify trước khi output.

Không tự ý thay đổi framework.

---

### Bước 5. Output

- Sinh từng file chiến lược riêng biệt (`.py`).
- Lưu vào:

```text
output/
```

Các file xuất ra phải:

- sạch
- có thể copy trực tiếp
- chạy được trên XNOQuant
- sẵn sàng để Simulate

---

## 5. Supreme Directive

AI Agent **không được phép**:

- tự ý sử dụng thư viện ngoài
- tự ý thay đổi framework
- tự ý thay đổi cấu trúc `CustomStrategy`

AI Agent **luôn phải**:

1. Đọc `template_example/strategy_framework.md` trước khi code.
2. Kiểm tra tính tương thích với `CustomStrategy`.
3. Chỉ sử dụng các API chính thức của XNOQuant.
4. Tuân thủ cú pháp của `feature/`, `operations/` và `template_example/`.
5. Tham chiếu acceptance criteria trong `idea/hypothesis/hypothesis_framework.md` khi thiết kế logic.
6. Đảm bảo mã nguồn có thể chạy trực tiếp trên nền tảng.

---

## 6. Where to Look When...

| Khi bạn cần… | Đọc file này |
|--------------|-------------|
| **Hiểu tổng quan dự án, workflow 5 bước** | `README.md` (file này) |
| **Context chi tiết phiên làm việc trước** | `context_session/session_context.md` |
| **Onboarding nhanh cho AI Agent** | `.agent/GUIDE.md` |
| **Master spec: class structure, compliance checklist** | `template_example/strategy_framework.md` |
| **Đặc thù thị trường VN → thiết kế strategy** | `data/vietnam_market_characteristics.md` |
| **Data fields (OHLCV, futures, VN30, DJI)** | `data/VnFuture.md` |
| **Feature functions (140+ indicators)** | `feature/feature_syntax.md` |
| **Operator functions (30+ operators)** | `operations/operations_syntax.md` |
| **Acceptance criteria, scorecard** | `idea/hypothesis/hypothesis_framework.md` |
| **Hypothesis docs (30 hypotheses)** | `idea/hypothesis/hyp_thesis_01_momentum.md` → `08_multifactor.md` |
| **Planning docs (enhancements, alpha ideas)** | `idea/planning_alpha/` |
| **Generator code (sửa generator, không sửa output)** | `tools/generate_strategies.py` |
| **Validate output files** | `tools/validate_framework.py` |
| **Backtest plan, decision rules** | `idea/planning_alpha/backtest_plan.md` |

### Debug Flow

```
Sharpe < target?
  → Đọc data/vietnam_market_characteristics.md §5 (Sharpe Rules)
  → Kiểm tra: ADX filter? return_roll? volume? asymmetric exit? session gating?
  
Strategy không publish được?
  → Đọc template_example/strategy_framework.md §Checklist
  → Kiểm tra: docstring thesis? position bounds? no look-ahead? valid execution?
  
Generator ra code sai?
  → Sửa tools/generate_strategies.py
  → Chạy python tools/generate_strategies.py
  → Chạy python tools/validate_framework.py
  → KHÔNG patch output files trực tiếp

Cần thêm template mới?
  → Đọc tools/generate_strategies.py search TEMPLATES
  → Thêm vào TEMPLATES dict, thêm parameter variants
  → Thêm vào inject_filters() nếu cần post-processing
```
