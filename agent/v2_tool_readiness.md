# V2 Tool Readiness — Audit toàn bộ vị trí cần sửa trước khi viết tool Round 2

> **Mục đích:** Liệt kê từng file + dòng còn gắn vòng 1 (futures intraday VN30F) cần sửa / thay /
> đánh dấu archived, để pipeline Round 2 (viết code → validate → submit → review) chạy sạch.
> **Ngày audit:** 2026-08-01. **Trạng thái:** đã dò toàn bộ `tools/`, `backtest/`, `agent/`, `README.md`.

---

## 1. Kết luận rút gọn

| Nhóm | File | Phân loại cho V2 |
|------|------|------------------|
| **Đã sửa xong** | `tools/submit_and_check.py`, `tools/common.py`, `tools/check_results.py`, `tools/update_guide_stats.py` | stage_2 + universe + CSV tách |
| **Đã làm xong** | `tools/validate_framework.py` (V2), `agent/GUIDE.md` (round-2 first), `agent/framework_build_guide.md`, `agent/migration_plan_v2.md` | ✅ |
| **Vòng 1 (archived, không dùng V2)** | `tools/generate_strategies.py`, `tools/gen_single_feat.py`, `backtest/*` (toàn bộ), `data/*`, `idea/*` | Giữ nguyên, không chạm |

---

## 2. Tools cần SỬA cho V2

### 2.1 `tools/check_results.py` — hiển thị + pass criteria
| Dòng | Vấn đề | Sửa |
|------|--------|-----|
| 23 | `is_pass` dựa `PASS_THRESHOLDS` vòng 1 (Sharpe≥1.3, CAGR≥15%...) | Round 2 chưa có bộ tiêu chí chính thức → dùng tạm, ghi rõ source |
| 67 | Header cứng `S=1.3 C=0.15 MD=-0.35 PF=1.2 CA=1.1` | Lấy từ `PASS_THRESHOLDS` thay vì hardcode |
| 34 | `--csv` mặc định `backtest/results.csv` | Vòng 2 nên tách `backtest/results_v2.csv` (tránh trộn với dữ liệu vòng 1) |

### 2.2 `tools/update_guide_stats.py` — đếm strategy
| Dòng | Vấn đề | Sửa |
|------|--------|-----|
| 16 | `OUTPUT_DIR = output/` — giờ output/ chứa stage_1+stage_2 | Quét `output/stage_2/` riêng cho V2 |
| 27-31 | Chỉ nhận diện `thesis_*` (vòng 1) | Stage_2 dùng index.csv làm nguồn đếm, không dựa tên folder |
| 47 | `total = thesis + single_feat + multi_feat` | Đổi sang đếm theo index.csv rows |

### 2.3 `tools/common.py` — shared helpers
| Dòng | Vấn đề | Sửa |
|------|--------|-----|
| 5-11 | `PASS_THRESHOLDS` = 5 tiêu chí vòng 1 | Round 2 scoring khác (best-scoring + net-of-fee + stability). Cần xác định bộ tiêu chí V2 hoặc để trống đợi platform |
| 30,37 | `load_results_csv` / `load_previous_results` mặc định `backtest/results.csv` | Cho phép truyền path tách vòng |

### 2.4 `tools/submit_and_check.py` — lõi API giữ nguyên, chỉ sửa discovery
| Dòng | Vấn đề | Sửa |
|------|--------|-----|
| 177 | `roots = ["output", "success_alpha"]` — sẽ quét luôn stage_1 + success_alpha | Thêm flag `--stage stage_2` hoặc chỉ quét `output/stage_2/` |
| 33-34 | Hardcode EDITOR_ID/TOKEN fallback | Vẫn được phép (fallback), nhưng nên bỏ khỏi source → chỉ đọc `.env` |
| 232 | Thông báo `output/ hoac success_alpha/` | Cập nhật message cho stage_2 |

> **API contract (không đổi giữa vòng):** `PUT /editors/{id}/update` → `POST verify` → `POST simulate` → `GET info` → `GET summary-aggregate`. Round 2 vẫn dùng chung editor flow. Chỉ khác là strategy code (daily equity, 2 mode) — script không cần biết nội dung code.

---

## 3. Tool ĐÃ XONG (không cần chạm)

- `tools/validate_framework.py` — **V2 hoàn tất**: quét `stage_2/`, detect mode, bounds, point-in-time, `index.csv` mới. ✅
- `agent/GUIDE.md` — round-2 reading order đầu, vòng 1 archived. ✅ (phần Generator Usage dòng 199-224 là vòng 1, đã nằm dưới mục archived)
- `agent/framework_build_guide.md` — blueprint + roadmap đã đổi đúng (agent viết code trực tiếp). ✅
- `agent/migration_plan_v2.md` — Phase A/B done, C mô tả đúng. ✅

---

## 4. Vòng 1 ARCHIVED — không chạm, không dùng cho V2

| File/Thư mục | Lý do |
|--------------|-------|
| `tools/generate_strategies.py` | Generator vòng 1 (TEMPLATES dict, inject_filters). V2 không có tool sinh code — agent viết trực tiếp |
| `tools/gen_single_feat.py` | Sinh `SF_*_15min` — tham số/field vòng 1 |
| `backtest/` toàn bộ (run.py, backtest.py, evaluate.py, regime.py, runners/, features/, data/, check_duplicate.py) | Local backtest engine VN30F futures 5m/15m — Round 2 dùng backtest trên nền tảng XNOQuant, không local |
| `data/vietnam_market_characteristics_v1.md`, `data/VnFuture.md` | Phân tích VN market futures vòng 1 (bản v1 đã chuyển sang `_v1.md`; VnFuture.md đánh dấu legacy) |
| `idea/hypothesis/`, `idea/planning_alpha/stage_1/` | Acceptance criteria + ideas vòng 1 (stage_2/ là idea Round 2 — ACTIVE) |
| `backtest/results.csv`, `backtest/strategy_index.json` | Kết quả vòng 1 |
| `template_example/(Old)vnfuture/` | Framework vòng 1 |
| `output/stage_1/` | Toàn bộ strategy vòng 1 đã archive |

---

## 5. Docs cần cập nhật song song

| File | Vị trí | Việc |
|------|--------|------|
| `README.md` | Dòng 15-55 (structure 8 thesis, VN30/DJI fields), 285-366 (batch submission vòng 1) | Thêm banner "vòng 1 archived", chỉ thêm phần V2 — không xoá phần vòng 1 (làm reference) |
| `tools/INDEX.md` | Bảng quick reference + pipeline | Đã cập nhật validate_framework; cập nhật thêm `submit --stage`, `check_results` v2 csv |
| `agent/submit_workflow.md` | Dòng 73-114 (5 tiêu chí pass), 141-149 (workflow vòng 1) | Ghi rõ "vòng 1", thêm section Round 2 khi có tiêu chí chính thức |
| `backtest/INDEX.md` | Toàn bộ | Đã ghi rõ "VN30F futures engine" — thêm dòng "Round 2 không dùng local backtest" |

---

## 6. Điểm đã có câu trả lời (cập nhật 2026-08-01)

1. **Bộ tiêu chí pass Round 2** ✅ — user cung cấp, theo universe (đã ghi vào `tools/common.py` `PASS_THRESHOLDS_BY_UNIVERSE`):
   - **VN-SMALL-CAP:** Sharpe ≥ 1.0, CAGR ≥ 25%, MaxDD ≥ -45%, PF ≥ 1.3, Calmar ≥ 0.8
   - **VN-MID-CAP:** Sharpe ≥ 1.1, CAGR ≥ 20%, MaxDD ≥ -40%, PF ≥ 1.25, Calmar ≥ 1.0
   - **VN-LARGE-CAP:** Sharpe ≥ 1.2, CAGR ≥ 15%, MaxDD ≥ -35%, PF ≥ 1.2, Calmar ≥ 1.1
   - `check_results.py` + `common.py` dùng `is_pass(row)` theo cột `universe` + `status` của row (PASS chỉ khi `SIMULATED` + đủ 5 metrics). Universe lạ/trống → `KeyError` (fail-closed).

2. **Token** ✅ — `submit_and_check.py` đã bỏ hardcode, chỉ đọc `.env` (`XNO_EDITOR_ID`, `XNO_TOKEN`), báo lỗi nếu thiếu. User tạo `.env` ở root (đã có `.gitignore` chặn).

3. **Kết quả CSV** ✅ — tách riêng `backtest/results_stage_2.csv` (không trộn với `results.csv` vòng 1).

4. **Discovery** ✅ — `submit_and_check.py` quét `output/stage_2/` (không quét output gốc + success_alpha). Universe **tự suy từ path** `output/stage_2/<cap>/...` (`resolve_universe`), **`--universe` chỉ là FILTER chọn 1 cap — KHÔNG ghi đè universe** (single editor: không submit nhiều cap cùng lúc). Thêm `--dry-run` (xem trước, không gọi API), `--test` = live 1 file đầu, poll metrics timeout 90s, skip theo `(filepath, universe)`. `.env` bắt buộc cho live.

---

## 7. Roadmap hành động (thứ tự đề xuất)

| # | Việc | File | Trạng thái |
|:-:|------|------|------------|
| 1 | Tách CSV + `--universe` filter + bỏ hardcode token + `--dry-run` + poll timeout + idempotency `(filepath, universe)` | `submit_and_check.py`, `common.py`, `check_results.py` | ✅ DONE |
| 2 | Cập nhật stats cho stage_2 (Total / By Universe / Matrix universe×mode) | `update_guide_stats.py` | ✅ DONE |
| 3 | Siết validator: manifest + mode contract + `--strict` + forbidden mới (import/comprehension/print/eval/exec/open), CS bắt buộc weights/mask, fundamental guard | `validate_framework.py` | ✅ DONE |
| 4 | Unittest 46 cases (validate/submit/results) | `tests/` | ✅ DONE |
| 5 | Cập nhật docs (README banner, tools/INDEX, submit_workflow, GUIDE tree) | `README.md`, `tools/INDEX.md`, `agent/submit_workflow.md`, `agent/GUIDE.md` | ✅ DONE |
| 6 | Xác định PASS criteria V2 (theo universe, fail-closed) | `common.py`, `check_results.py` | ✅ DONE (user cung cấp) |
| 7 | Agent viết strategy Level 1-5 → `output/stage_2/` | code mới | ✅ 6 alpha Batch 1 |
| 8 | Preflight + dry-run 3 cap + live smoke (cần user chọn universe trên UI) | `submit_and_check.py`, `check_results.py` | ⏳ NEXT |
