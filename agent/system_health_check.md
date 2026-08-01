# System Health Check — Stage 2

> **Đọc file này khi cần kiểm tra trạng thái hệ thống / mức độ sẵn sàng chạy Stage 2.**
> File hướng dẫn agent thực hiện health check: offline trước, API read-only sau,
> KHÔNG tự động submit hoặc sửa đổi editor nếu user chưa yêu cầu rõ.

---

## 1. Mục đích

- Trả lời câu hỏi: **"Stage 2 có sẵn sàng để chạy không?"**
- Tổng hợp trạng thái theo 3 nhóm:
  - **Offline:** Python, dependencies, `.env`, unittest, tool preflight, CSV.
  - **API read-only:** editor mapping, universe, strategy_id, summary-aggregate.
  - **Live-mutating:** chỉ khi user yêu cầu rõ (PUT/verify/simulate).

## 2. Ràng buộc bắt buộc

- **KHÔNG đọc trực tiếp nội dung `output/**` và `template_example/**`.**
  - Được phép chạy tool hiện có (`validate_framework.py`, dry-run) và đọc kết quả
    tổng hợp (exit code, output) — nhưng không mở/parse source strategy.
- **KHÔNG chạy live submit** (`--batch`, `--test`, `--yes`, `--force`, interactive)
  khi user chỉ yêu cầu "kiểm tra trạng thái". Live smoke phải opt-in riêng.
- **KHÔNG chạy `update_guide_stats.py`** — tool này ghi đè `output/STATS.md`.
- **KHÔNG in token hoặc editor ID đầy đủ.** Chỉ hiển thị dạng rút gọn
  (VD `a1619c25…66dc`) hoặc `present/missing`.
- Không xóa / sửa `backtest/results_stage_2.csv`.

---

## 3. Offline Health Check

Chạy theo thứ tự. Ghi lại exit code của từng lệnh.

### 3.1 Python & dependencies
```bash
python --version
python -c "import requests, dotenv; print('deps OK')"
```
- FAIL nếu thiếu `requests` hoặc `dotenv`.

### 3.2 `.env` — chỉ kiểm tra presence
Cần có đủ (đọc bằng cách kiểm tra biến, KHÔNG in giá trị):

| Biến | Ghi chú |
|------|---------|
| `XNO_TOKEN` | bắt buộc |
| `XNO_EDITOR_ID_SMALL` | editor SMALL |
| `XNO_EDITOR_ID_MID` | editor MID |
| `XNO_EDITOR_ID_LARGE` | editor LARGE |

- Phát hiện fallback legacy `XNO_EDITOR_ID` (chỉ khi thiếu biến per-universe) → cảnh báo.
- Editor ID trùng nhau giữa 2 cap → `UNHEALTHY`.

### 3.3 Unit tests
```bash
python -m unittest discover -s tests
```
- PASS: exit 0. Ghi rõ số test (hiện 48).

### 3.4 Tool syntax / import
```bash
python -c "import sys; sys.path.insert(0,'tools'); import common, validate_framework, submit_and_check, check_results; print('tools import OK')"
```

### 3.5 Stage 2 preflight (chỉ chạy tool, không đọc output/**)
```bash
python tools/validate_framework.py --strict
python tools/submit_and_check.py --batch --dry-run --universe VN-SMALL-CAP
python tools/submit_and_check.py --batch --dry-run --universe VN-MID-CAP
python tools/submit_and_check.py --batch --dry-run --universe VN-LARGE-CAP
```
- Dry-run **không gọi HTTP, không ghi CSV**.
- Xem như lỗi nếu: exit khác 0, "no files", mixed-cap, invalid universe, mapping error.
- Không chạy `--test` (là live), không chạy `update_guide_stats.py`.

### 3.6 Results CSV health
Đọc `backtest/results_stage_2.csv` (chỉ schema/status, không phải source):
- Header đúng 13 cột:
  `timestamp,filepath,filename,universe,mode,status,strategy_id,cagr,sharpe,calmar,max_drawdown,profit_factor,error`
- `universe` ∈ {VN-SMALL-CAP, VN-MID-CAP, VN-LARGE-CAP}, `mode` ∈ {time_series, cross_sectional}.
- `status` ∈ {SIMULATED, UPDATE_FAILED, VERIFY_FAILED, SIMULATE_FAILED, RATE_LIMITED, METRICS_TIMEOUT, NO_STRATEGY_ID}.
- `SIMULATED` phải có đủ 5 metrics dạng số.
- `METRICS_TIMEOUT` / `NO_STRATEGY_ID` → PENDING.
- Key duy nhất theo `(filepath, universe)`.
- Timestamp parse được.

---

## 4. API Read-Only Health Check

Chỉ gọi GET; **không** PUT/POST. Nếu chưa có network permission, bỏ qua và báo `UNKNOWN`.

### 4.1 Editor mapping
Với mỗi editor trong `.env`:
```text
GET https://api.xnoquant.io/xalpha-api/v2/editors/{editor_id}/info
Authorization: Bearer <token>
```
Đối chiếu:

| Biến | Universe mong đợi |
|------|-------------------|
| `XNO_EDITOR_ID_SMALL` | `VN-SMALL-CAP` |
| `XNO_EDITOR_ID_MID` | `VN-MID-CAP` |
| `XNO_EDITOR_ID_LARGE` | `VN-LARGE-CAP` |

- Đọc `data.universe` trong response → khớp universe mong đợi.
- Đọc `data.strategy_ids[0]` → strategy_id hiện tại.
- Phân loại response:
  - HTTP 200 + JSON hợp lệ + universe khớp → PASS
  - HTTP 401/403 → AUTH_ERROR
  - HTTP 404 → editor không tồn tại
  - HTTP 429 → RATE_LIMITED
  - HTTP 5xx / timeout → API_ERROR
  - universe không khớp cap → MAPPING_ERROR

### 4.2 Summary aggregate
Với strategy_id hiện tại của từng editor:
```text
GET https://api.xnoquant.io/xalpha-api/v1/strategies/{strategy_id}/stages/simulate/summary-aggregate
```
- `READY`: HTTP 200 + có đủ 5 metrics (cagr, sharpe, calmar, max_drawdown, profit_factor).
- `PENDING`: HTTP 404 `summary table not found` → summary chưa được sinh (KHÔNG coi là API down).
- `STALE_RISK`: strategy_id trong CSV khác strategy_id hiện tại của editor.
- `INVALID`: metrics thiếu / không phải số.

> **Lưu ý:** response aggregate **không chứa tên cap**. Luôn xác định cap qua
> `/info` của editor tương ứng, không đoán từ response aggregate.

---

## 5. Live Check Guard (chỉ khi user yêu cầu rõ)

Trước khi live submit, agent phải:
1. Trình bày kế hoạch: cap, editor rút gọn, file sẽ chạy, hành động sẽ ghi đè code editor.
2. Gọi `/info` lần cuối để xác nhận universe khớp cap.
3. Yêu cầu xác nhận riêng từ user.
4. Chỉ chạy **một file** (`--test`), không tự `--force` / `--yes`.
5. Sau khi chạy: xác nhận strategy_id mới (không phải ID cũ), kiểm tra CSV + aggregate.

Quy trình chuẩn (xem chi tiết `agent/submit_workflow.md`):
```bash
python tools/validate_framework.py --strict
python tools/submit_and_check.py --batch --dry-run --universe VN-<CAP>
python tools/submit_and_check.py --batch --test --universe VN-<CAP>   # cần confirm
python tools/check_results.py --detail --universe VN-<CAP>
```

---

## 6. Tổng hợp kết quả

### Mức trạng thái
| Mức | Điều kiện |
|-----|-----------|
| `HEALTHY` | offline pass, editor mapping đúng, API reachable, không lỗi CSV nghiêm trọng |
| `DEGRADED` | aggregate PENDING, metrics timeout, result fail threshold, legacy fallback |
| `UNHEALTHY` | tests fail, editor mapping sai, AUTH_ERROR, CSV malformed, validator fail |
| `UNKNOWN` | check bị skip (thiếu permission / network) |

### Report mẫu
```text
Stage 2 System Health: DEGRADED

Offline
- Python: PASS | deps: PASS | unit tests: 48/48 PASS | validator: PASS

Editors
- SMALL: PASS (VN-SMALL-CAP)
- MID:   PASS (VN-MID-CAP)
- LARGE: PASS (VN-LARGE-CAP)

Aggregates
- SMALL: READY
- MID:   PENDING (summary table not found)
- LARGE: READY

Results CSV
- Schema: PASS | Pending rows: 1 | API errors: 0

Live checks
- NOT RUN

Blocking
- MID summary table chưa sẵn sàng
```

---

## 7. Files tham chiếu

Đọc khi cần context chi tiết:
- `agent/stage_2_guideline.md` — rules Round 2
- `agent/submit_workflow.md` — workflow submit + API
- `agent/GUIDE.md` — tổng quan pipeline
- `tools/submit_and_check.py` — editor mapping, status, CSV schema
- `tools/validate_framework.py` — strict validator
- `tools/check_results.py` — review results
- `tools/common.py` — thresholds, is_pass, status_label
- `.env.example` — cấu hình editor
- `backtest/results_stage_2.csv` — dữ liệu kết quả
- `tests/` — unit tests

KHÔNG đọc trực tiếp: `output/**`, `template_example/**`.
