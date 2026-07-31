# Migration Plan V2 — Chuyển sang Data Model Mới (Vòng 2)

> **Trạng thái:** AWAITING APPROVAL — Phase A chưa thực thi.
> **Mục tiêu:** Archive vòng 1, dựng khung `stage_2`, migrate file new-data từ `input/` theo form chuẩn.

---

## 1. Bối cảnh

- **Vòng 1 (hiện tại):** 782 strategy file trên data model cũ — 22 data fields, 183 features, 30 operators.
- **Vòng 2:** XNOQuant giới thiệu loại data + syntax mới (`self.data.*`, `self.feat.*`, `self.op.*` đều thay đổi).
- **Yêu cầu:** chuẩn bị toàn bộ pipeline cho vòng thi mới, tận dụng các file đã viết theo data mới.

---

## 2. Cấu trúc output mới

```text
output/
├── stage_1/          # ARCHIVE vòng 1 (nguyên trạng: index.csv, STATS.md, mọi thesis_*/, alpha dirs)
├── stage_2/          # ACTIVE vòng 2 (tạo trống, điền dần sau migrate)
├── index.csv         # (mới) manifest vòng 2
└── INDEX.md          # phân biệt stage_1 = archive, stage_2 = active

input/                # Thư mục tạm — user đặt file new-data vào đây để migrate
```

---

## 3. Các Phase

### Phase A — Archive vòng 1
- `git mv` toàn bộ `output/*` → `output/stage_1/` (giữ lịch sử, rollback được).
- Không xoá bất kỳ file nào.
- **Output:** cấu trúc thư mục mới + `output/INDEX.md`.

### Phase B — Syntax mới
- User cung cấp tài liệu syntax mới → thay thế toàn bộ `syntax/*.md`.
- Lập **Migration Map**: bảng `field/func cũ → mới`.

### Phase C — Chuẩn bị `input/` + migrate
- User đặt file new-data vào `input/`.
- `tools/migrate_stage2.py`: đọc `input/` → chuẩn hoá form → xuất `stage_2/` + ghi `index.csv` mới.
- Mở rộng `validate_framework.py` theo rule mới.

### Phase D — Documentation
- Cập nhật `agent/GUIDE.md`, `README.md`, `tools/INDEX.md`.
- File này là nguồn tham chiếu chính.

---

## 4. Migration Map (bảng ánh xạ cũ → mới)

> Điền sau khi có tài liệu syntax mới từ user.

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

- [ ] **Phase A:** cấu trúc stage_1/stage_2
- [ ] **Phase B:** syntax mới + migration map
- [ ] **Phase C:** migrate `input/` → `stage_2/`
- [ ] **Phase D:** docs sync

---

## 6. Rủi ro & Lưu ý

- `output/index.csv` vòng 1 đang stale (chỉ 428/1,705 rows khớp file) — archive nguyên trạng, không sửa.
- Không xoá dữ liệu vòng 1 cho đến khi vòng 2 chạy ổn định.
- Mọi thay đổi framework tuân theo `template_example/strategy_framework.md` và supreme directive trong `README.md`.
