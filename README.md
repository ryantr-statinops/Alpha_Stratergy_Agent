# ALPHA_BOT - Quantitative Strategy Builder Engine

> ## ⚠️ ROUND 2 (ACTIVE) — Fundamental Alpha Arena
>
> Dự án đang ở **Vietnam Quant Challenge 2026 — Round 2**: daily equity research trên 3 universe
> (VN-SMALL-CAP / VN-MID-CAP / VN-LARGE-CAP), 2 mode (time_series / cross_sectional).
>
> **Bắt đầu ở đây (đọc theo thứ tự):**
> 1. `agent/stage_2_guideline.md` — rules chính thức Round 2
> 2. `agent/framework_build_guide.md` — blueprint gen strategy (Level 1-5)
> 3. `agent/GUIDE.md` — onboarding + pipeline
> 4. `template_example/strategy_framework.md` — master spec Round 2
> 5. `syntax/INDEX.md` — shared data + catalog riêng cho `time_series` va `cross_sectional`
>
> **Pipeline:** agent viết strategy → `output/stage_2/<cap>/<mode>/` → `tools/validate_framework.py --strict` →
> `tools/submit_and_check.py --batch --universe VN-...` → `tools/check_results.py`.
> Universe submit: suy từ path cap (hoặc `--universe` để lọc 1 cap).
>
> Các phần bên dưới mô tả vòng 1 (intraday futures VN30F) — **đã archive** tại `output/stage_1/`.

---

## 1. Project Overview & Purpose

Dự án này là môi trường nghiên cứu và phát triển chiến lược đầu tư định lượng (Quantitative Trading) dành riêng cho nền tảng **XNOQuant**.

Mục đích cốt lõi của không gian làm việc này là giúp AI Agent đọc hiểu sâu sắc cấu trúc cú pháp, dữ liệu đầu vào và các hàm chức năng được nền tảng cung cấp. Từ đó, AI có thể tự động hóa quy trình lên ý tưởng (Alpha Generation), lập kế hoạch kiểm thử và viết mã nguồn chiến lược hoàn chỉnh một cách chính xác mà không vi phạm các quy tắc của hệ thống.

---

## 2. Project Structure

```text
ALPHA_BOT/
├── data/                   # Đặc thù thị trường + hướng dẫn chọn feature (Round 2), futures v1 (legacy)
├── syntax/                 # Catalog + usage guide cho data/feature/operations (Round 2)
├── template_example/       # Framework chuẩn + strategy mẫu chạy được trên XNOQuant
│   └── strategy_framework.md   # **Master specification** — đọc đầu tiên
├── idea/                   # Nơi lưu trữ các ý tưởng nghiên cứu (.md)
│   ├── planning_alpha/
│   │   ├── stage_1/        # Idea vòng 1 (futures intraday — archived)
│   │   └── stage_2/        # Idea Round 2 — mỗi alpha ghi 1 file trước khi gen
│   ├── hypothesis/         # Giả thuyết kiểm thử, tiêu chí chấm điểm, design guidelines
│   └── stage_overview/     # Ghi lại tiến độ và lịch sử phiên làm việc
├── output/                 # Mã nguồn chiến lược hoàn chỉnh (.py)
│   ├── index.csv           # Master manifest tra cứu strategy (Round 2: cột universe)
│   └── stage_2/            # Round 2 ACTIVE — daily equity, 3 cap, 2 mode
│       └── <cap>/<mode>/   #   VD vn_small_cap/time_series/ — 1 subdir / cap × mode
├── tools/                  # Tool support (validate/submit/check — Round 2 không có generator)
└── README.md               # Tài liệu hướng dẫn dành cho AI Agent
```

### 8 Thesis Groups (Vòng 1 — ARCHIVED)

> Nhóm thesis này thuộc vòng 1 (futures intraday). Round 2 dùng 3 cap daily equity; thesis Round 2 ghi trong `idea/planning_alpha/stage_2/`.

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
**Target (Round 2, per universe):** pass criteria tại `tools/common.py` (`PASS_THRESHOLDS_BY_UNIVERSE`) — SMALL/MID/LARGE có ngưỡng riêng (Sharpe 1.0/1.1/1.2, CAGR 25%/20%/15%, MaxDD -45%/-40%/-35%, PF 1.3/1.25/1.2, Calmar 0.8/1.0/1.1). PASS = đạt cả 5.

> ⚠️ Ngưỡng Round 1 (Sharpe ≥ 1.2, CAGR ≥ 25%...) trong §2 dưới đây là legacy — xem `idea/hypothesis/hypothesis_framework.md` (ARCHIVED).

---

## 3. Knowledge Base Reference (AI Onboarding Guide)

Trước khi thực hiện bất kỳ yêu cầu nào từ người dùng, AI Agent **bắt buộc** phải đọc và phân tích các thư mục sau để xây dựng ngữ cảnh (Context) làm việc.

### `data/`

- Hiểu cách truy cập dữ liệu thị trường.
- Round 2 (equity): `self.data.pv_close`, `self.data.fun_is_eps_basis_quarterly`, `self.data.fun_is_net_profit_loss_after_tax_quarterly_panel`.
- Ví dụ vòng 1 (futures — legacy): `self.data.fut_matched_volume_vn30f1m_1d`.
- Không sử dụng tên biến trùng với từ khóa của hệ thống.
  - ✅ `open_price`
  - ❌ `open`

Chi tiết xem tại [`syntax/data_syntax.md`](syntax/data_syntax.md).

#### Đặc thù thị trường Việt Nam (Round 2 — equity fundamental)

Tài liệu [`data/vietnam_market_characteristics.md`](data/vietnam_market_characteristics.md) (bản Round 2) phân tích chi tiết:
- Retail 80-90% → fundamental mispricing tồn tại lâu, growth-momentum/rank có edge
- Tin nội tại chi phối → biến động quanh ngày công bố BCTC, gap risk
- Thanh khoản tập trung → large/mid cap khả thi, small cap thận trọng
- BCTC công bố chậm → **bắt buộc point-in-time**, `.notna()`, không backfill
- **Feature Selection per cap**: SMALL → growth/earnings; MID → quality/ROE; LARGE → cashflow/value
- **Fields verified theo catalog**: ưu tiên dùng tránh lỗi submit
- Bản v1 (futures VN30F1M intraday) đã chuyển sang [`data/vietnam_market_characteristics_v1.md`](data/vietnam_market_characteristics_v1.md)

#### Danh sách trường VN30 Index (vòng 1 — legacy)

| Trường | Ý nghĩa |
|--------|---------|
| `pv_vn30_open` | VN30 Open |
| `pv_vn30_high` | VN30 High |
| `pv_vn30_low` | VN30 Low |
| `pv_vn30_close` | VN30 Close |
| `pv_vn30_volume` | VN30 Volume |

#### Danh sách trường Dow Jones Index (vòng 1 — legacy)

| Trường | Ý nghĩa |
|--------|---------|
| `pv_dji_open` | DJI Open |
| `pv_dji_high` | DJI High |
| `pv_dji_low` | DJI Low |
| `pv_dji_close` | DJI Close |
| `pv_dji_volume` | DJI Volume |

### `syntax/`

- Tra cứu data, các chỉ báo kỹ thuật và toán tử trong các catalog:
  - `syntax/data_syntax.md`
  - `syntax/time_series/feature_syntax.md, syntax/cross_sectional/feature_syntax.md`
  - `syntax/time_series/operations_syntax.md, syntax/cross_sectional/operations_syntax.md`
- Đọc `syntax/INDEX.md` trước khi code để biết cách chọn nhóm data/hàm/toán tử phù hợp.
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

## 4. Operational Workflow (Vòng 1 — ARCHIVED)

> Quy trình 5 bước dưới đây thuộc vòng 1 (idea/hypothesis loop + generator).
> **Round 2** dùng pipeline ở §5 + `agent/GUIDE.md` §Round 2 (viết trực tiếp → validate → submit → check).

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
idea/planning_alpha/stage_1/
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
  - các field trong `syntax/data_syntax.md`
  - các hàm trong `syntax/time_series/feature_syntax.md, syntax/cross_sectional/feature_syntax.md`
  - các hàm trong `syntax/time_series/operations_syntax.md, syntax/cross_sectional/operations_syntax.md`
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

## 5. Batch Submission (XNOQuant API — Round 2)

> Pipeline Round 2: agent viết strategy trực tiếp → `output/stage_2/` → validate → submit → check.
> Các mục "Batch Submission vòng 1" (thesis_*/generator/hardcoded editor) đã archive — không dùng.

### API Endpoints (Discovered via DevTools Network)

| Step | Method | URL | Body |
|------|--------|-----|------|
| **Send code** | PUT | `/editors/{id}/update` | `{"code": "..."}` |
| **Verify syntax** | POST | `/editors/{id}/verify` | (empty) |
| **Run backtest** | POST | `/editors/{id}/simulate` | (empty) |
| Fetch metrics | GET | `/strategies/{strategy_id}/stages/simulate/summary-aggregate` | — |

**Auth:** `Authorization: Bearer <token>` — lấy từ `.env` (`XNO_EDITOR_ID`, `XNO_TOKEN`)

> ⚠️ **Universe KHÔNG được thiết lập qua API.** Editor universe được chọn thủ công trên giao diện XNOQuant.
> `submit_and_check.py` chỉ lọc file theo cap và yêu cầu xác nhận trước live submit.
> `--dry-run` hiển thị editor + universe + files mà không gọi API.
> `--test` = live submit file đầu tiên của cap (KHÔNG phải dry-run).

### Workflow (Round 2)

1. Agent viết strategy vào `output/stage_2/<cap>/<mode>/` (VD `vn_small_cap/time_series/`) + ghi `output/index.csv` (cột `filepath` = `<cap>/<mode>/<file>.py`)
2. **`python tools/validate_framework.py --strict`** — check compliance (mode contract, point-in-time, bounds, manifest consistency)
3. **`python tools/submit_and_check.py --batch --dry-run --universe VN-<CAP>`** — xem trước editor/universe/files (không gọi API)
   - Chọn đúng universe trên XNOQuant (thủ công) → **`python tools/submit_and_check.py --batch --universe VN-<CAP>`**
   - `--test` = live submit 1 file đầu của cap; `.env` bắt buộc cho live
4. **`python tools/check_results.py --detail --universe VN-<CAP>`** — review PASS/FAIL theo ngưỡng từng cap

> Lưu ý: `--universe` là bộ lọc cap, không phải tag override. Universe ghi vào CSV luôn suy từ path.
> Không submit nhiều cap trong một lần chạy (single editor).

### Kết quả

- Metrics lưu tại `backtest/results_stage_2.csv` (có cột `universe`)

---

## 6. Supreme Directive

AI Agent **không được phép**:

- tự ý sử dụng thư viện ngoài
- tự ý thay đổi framework
- tự ý thay đổi cấu trúc `CustomStrategy`

AI Agent **luôn phải**:

1. Đọc `template_example/strategy_framework.md` trước khi code.
2. Kiểm tra tính tương thích với `CustomStrategy`.
3. Chỉ sử dụng các API chính thức của XNOQuant.
4. Tuân thủ cú pháp của `syntax/` và `template_example/`.
5. Round 2: dùng pass criteria theo cap tại `tools/common.py` (`PASS_THRESHOLDS_BY_UNIVERSE`) — không dùng hypothesis_framework vòng 1 (ARCHIVED).
6. Đảm bảo mã nguồn có thể chạy trực tiếp trên nền tảng.

---

## 7. Where to Look When...

| Khi bạn cần… | Đọc file này |
|--------------|-------------|
| **Hiểu tổng quan dự án, workflow 5 bước** | `README.md` (file này) |
| **Context chi tiết phiên làm việc trước** | `context_session/session_context.md` |
| **Onboarding nhanh cho AI Agent** | `agent/GUIDE.md` |
| **Rules chính thức Round 2** | `agent/stage_2_guideline.md` |
| **Blueprint gen strategy Round 2** | `agent/framework_build_guide.md` |
| **Master spec: class structure, compliance checklist** | `template_example/strategy_framework.md` |
| **Đặc thù thị trường VN Round 2 → chọn feature** | `data/vietnam_market_characteristics.md` |
| **Data fields (PV/IS/BS/CF, 496 fields)** | `syntax/data_syntax.md` |
| **Syntax index** | `syntax/INDEX.md` |
| **Feature functions (panel features)** | `syntax/time_series/feature_syntax.md, syntax/cross_sectional/feature_syntax.md` |
| **Operator functions (cross_sectional ops)** | `syntax/time_series/operations_syntax.md, syntax/cross_sectional/operations_syntax.md` |
| **Parameter daily Round 2** | `syntax/time_series/parameters.md, syntax/cross_sectional/parameters.md` |
| **Submit Round 2 → review** | `tools/submit_and_check.py` → `tools/check_results.py` |
| **Validate Round 2 output** | `tools/validate_framework.py` |
| **Pass criteria theo cap** | `tools/common.py` (`PASS_THRESHOLDS_BY_UNIVERSE`) |
| **Tool reference (chọn đúng tool cho từng task)** | `tools/INDEX.md` |
| **Acceptance criteria, scorecard (vòng 1)** | `idea/hypothesis/hypothesis_framework.md` |
| **Hypothesis docs (30 hypotheses)** | `idea/hypothesis/hyp_thesis_01_momentum.md` → `08_multifactor.md` |
| **Idea Round 2 (trước khi gen)** | `idea/planning_alpha/stage_2/` |
| **Planning docs (vòng 1 — enhancements, alpha ideas)** | `idea/planning_alpha/stage_1/` |
| **— Sharpe improvement plan (3 phases)** | `idea/planning_alpha/stage_1/enhancement_return_roll_tiered_session.md` |
| **— ~890 alpha variants reference** | `idea/planning_alpha/stage_1/alpha_generation_rolling_mean_quantile.md` |
| **— Scaling proposal 500→10000** | `idea/planning_alpha/stage_1/scaling_proposal_500_10000_strategies.md` |
| **— Strategy design mẫu đầu tiên** | `idea/planning_alpha/stage_1/strategy_001_mean_quantile_rsi.md` |
| **Generator code (vòng 1 — sửa generator, không sửa output)** | `tools/generate_strategies.py` |
| **Backtest plan, decision rules (vòng 1)** | `idea/planning_alpha/stage_1/backtest_plan.md` |

### Debug Flow

```
Round 2: alpha không đạt / lỗi submit?
  → Đọc data/vietnam_market_characteristics.md §6 (Debug nhanh Round 2)
  → Kiểm tra: field có trong catalog? point-in-time? mode contract? threshold theo cap?
  → Chạy python tools/validate_framework.py

Round 2: review kết quả?
  → python tools/check_results.py --universe VN-<CAP>

Vòng 1 (futures intraday — ARCHIVED):
  → Đọc data/vietnam_market_characteristics_v1.md §5 (Sharpe Rules)
  → Kiểm tra: ADX filter? return_roll? volume? asymmetric exit? session gating?
  
Strategy không publish được?
  → Đọc template_example/strategy_framework.md §Checklist
  → Kiểm tra: docstring thesis? position bounds? no look-ahead? valid execution?
  
Generator ra code sai (vòng 1)?
  → Sửa tools/generate_strategies.py
  → Chạy python tools/generate_strategies.py
  → Chạy python tools/validate_framework.py
  → KHÔNG patch output files trực tiếp

Cần thêm template mới (vòng 1)?
  → Đọc tools/generate_strategies.py search TEMPLATES
  → Thêm vào TEMPLATES dict, thêm parameter variants
  → Thêm vào inject_filters() nếu cần post-processing
```
