# Migration Plan V2 — Chuyển sang Data Model Mới (Vòng 2)

> **Trạng thái:** PHASE A+B DONE — Phase C chưa thực thi.
> **Mục tiêu:** Archive vòng 1, dựng khung `stage_2`, AI agent viết trực tiếp strategy Round 2 vào `stage_2/` theo guide.

---

## 1. Bối cảnh

- **Vòng 1 (archive):** 782 strategy file trên data model cũ — intraday VN30 futures (22 data fields, 183 features, 30 operators).
- **Vòng 2 (active):** **Round 2 — Fundamental Alpha Arena**, daily equity research trên 3 universe
  (VN-SMALL-CAP / VN-MID-CAP / VN-LARGE-CAP). Data mới: 496 fields (PV 10 + IS 130 + BS 271 + CF 85),
  36 panel features, 6 cross-sectional ops.
- **Nguồn chuẩn:** `agent/stage_2_guideline.md` (round rules) — **khác hẳn vòng 1** (daily, long-only,
  fundamentals point-in-time).
- **Yêu cầu:** chuẩn bị toàn bộ pipeline cho vòng thi mới.

---

## 2. Cấu trúc output mới

```text
output/
├── stage_1/          # ARCHIVE vòng 1 (nguyên trạng: index.csv, STATS.md, mọi thesis_*/, alpha dirs)
├── stage_2/          # ACTIVE vòng 2 (code mới viết trực tiếp theo guide)
├── index.csv         # manifest vòng 2
└── INDEX.md          # phân biệt stage_1 = archive, stage_2 = active
```

---

## 3. Các Phase

### Phase A — Archive vòng 1
- `git mv` toàn bộ `output/*` → `output/stage_1/` (giữ lịch sử, rollback được).
- Không xoá bất kỳ file nào.
- **Output:** cấu trúc thư mục mới + `output/INDEX.md`.

### Phase B — Syntax mới ✅ DONE
- User cung cấp tài liệu syntax mới → đã thay thế toàn bộ `syntax/*.md`.
- **Migration Map** đã lập: `input/templates/migration_map_v2.md` (bảng `field/func cũ → mới`).
- Kết quả:
  - `syntax/data_syntax.md` — 496 fields + mode contract (time_series / cross_sectional).
  - `syntax/feature_syntax.md` — 36 panel features + time_series family.
  - `syntax/operations_syntax.md` — 7 cross-sectional ops + time_series ops.
  - `template_example/strategy_framework.md` — master spec Round 2 (viết lại hoàn toàn).

### Phase C — Sinh strategy Round 2 ⏳ PENDING
- Code strategy Round 2 do **AI agent viết trực tiếp** theo `agent/framework_build_guide.md` — KHÔNG có tool sinh code kiểu vòng 1.
- File viết mới hoàn toàn (không migrate), đẩy thẳng vào `output/stage_2/` + cập nhật `index.csv` (không cần bước `input/` trung gian, không cần `migrate_stage2.py`).
- Cập nhật `tools/validate_framework.py` V2 theo rule mới (mode contract, point-in-time, long-only, bounds).
- **Audit đầy đủ các vị trí cần sửa:** xem [`agent/v2_tool_readiness.md`](v2_tool_readiness.md) — từng file + dòng.

### Phase D — Documentation
- Cập nhật `agent/GUIDE.md`, `README.md`, `tools/INDEX.md`.
- File này là nguồn tham chiếu chính.

---

## 4. Migration Map (bảng ánh xạ cũ → mới)

> ✅ Đã điền đầy đủ tại [`input/templates/migration_map_v2.md`](../input/templates/migration_map_v2.md).
> Tóm tắt: `pv_*` giữ nguyên (time_series không suffix / cross_sectional `_panel`); DJI & futures & session
> gates **xoá**; fundamentals `fun_*` **mới**. Chiến lược futures vòng 1 không migrate tự động — viết lại
> theo `template_example/VN-*/`.

| Field/Func cũ | Field/Func mới | Ghi chú |
|---------------|----------------|---------|
| `pv_close` | ? | ? |
| `pv_high` | ? | ? |
| `pv_low` | ? | ? |
| `pv_open` | ? | ? |
| `pv_volume` | ? | ? |
| `pv_vn30_close` | ? | ? |
| `pv_dji_close` | ? | ? |
| `fut_matched_volume_vn30f1m_1d` | ? | ? |
| `fut_open_interest_vn30f1m_1d` | ? | ? |
| `self.feat.sma` | ? | ? |
| `self.feat.adx` | ? | ? |
| `self.feat.rsi` | ? | ? |
| `self.op.crossed_above` | ? | ? |
| `self.op.pct_change` | ? | ? |
| ... | ... | ... |

---

## 5. Checklist Approve

- [x] **Phase A:** cấu trúc stage_1/stage_2 + INDEX.md ✅
- [x] **Phase B:** syntax mới + migration map ✅
- [ ] **Phase C:** agent viết trực tiếp strategy Round 2 → `stage_2/` + `index.csv`, cập nhật validator V2
- [ ] **Phase D:** docs sync

## 6. Rủi ro & Lưu ý

- Vòng 2 là **sản phẩm khác hoàn toàn** (futures intraday → equity daily): file vòng 1 **không dùng lại được**, code Round 2 viết mới hoàn toàn theo `agent/framework_build_guide.md`.
- `output/stage_1/index.csv` vòng 1 đang stale (chỉ 428/1,705 rows khớp file) — archive nguyên trạng, không sửa.
- Không xoá dữ liệu vòng 1 cho đến khi vòng 2 chạy ổn định.
- Mọi thay đổi framework tuân theo `template_example/strategy_framework.md` (đã viết lại cho Round 2) và
  `agent/stage_2_guideline.md`.
