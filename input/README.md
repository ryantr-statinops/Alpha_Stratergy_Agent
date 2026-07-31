# input/ — Thư mục Migration V2 (Hướng dẫn cung cấp thông tin)

Thư mục này là nơi bạn (user) cung cấp **toàn bộ nguyên liệu** cho migration vòng 2:

1. **Syntax/data model mới** → điền vào `templates/`
2. **File strategy new-data** → đặt trực tiếp vào `input/`

Xem kế hoạch đầy đủ: [`agent/migration_plan_v2.md`](../agent/migration_plan_v2.md)

---

## A. Bạn cần cung cấp những gì?

### A.1. Syntax mới — điền vào 5 file template

> Mỗi file template đã có sẵn khung bảng + ví dụ dòng đầu. Bạn chỉ cần điền **thêm dòng vào các hàng trống**.

| # | Template | Bạn điền gì vào? | Vì sao cần? |
|:-:|----------|------------------|-------------|
| 1 | `templates/syntax_data_v2.md` | Danh sách **data fields** mới của vòng 2 (mọi `self.data.*`) | Để viết lại `syntax/data_syntax.md` — biết field nào dùng được, tên chính xác |
| 2 | `templates/syntax_feature_v2.md` | Danh sách **feature functions** mới (mọi `self.feat.*`) + signature + return type | Để viết lại `syntax/feature_syntax.md` — biết chỉ báo nào có, tham số gì |
| 3 | `templates/syntax_operations_v2.md` | Danh sách **operators** mới (mọi `self.op.*`) + cú pháp | Để viết lại `syntax/operations_syntax.md` — biết toán tử nào có |
| 4 | `templates/syntax_parameters_v2.md` | Bộ **tham số chuẩn** mới theo từng timeframe (15m quan trọng nhất) | Để viết lại `syntax/parameters.md` — biết dùng window/threshold nào |
| 5 | `templates/migration_map_v2.md` | **Bảng ánh xạ cũ → mới** (mọi field/func/op vòng 1 → vòng 2, trạng thái giữ/đổi/xoá) | Để `migrate_stage2.py` biết cách convert code cũ sang mới tự động |

**Mức độ bắt buộc:**
- `migration_map_v2.md` và `syntax_data_v2.md` → **bắt buộc** (không có thì không migrate được)
- `syntax_feature_v2.md`, `syntax_operations_v2.md` → bắt buộc nếu features/operators có thay đổi
- `syntax_parameters_v2.md` → cần nếu tham số chuẩn thay đổi

### A.2. File strategy new-data — đặt trực tiếp vào `input/`

- Các file `.py` bạn **đã viết sẵn theo data model mới của vòng 2**
- Đặt trực tiếp vào `input/` (cùng cấp với `README.md` và `templates/`)
- Tôi sẽ đọc, chuẩn hoá form, xuất sang `output/stage_2/`

---

## B. Trạng thái hiện tại

| Hạng mục | Trạng thái |
|----------|-----------|
| File template | ✅ Tạo sẵn 5 file trong `templates/` |
| Bạn điền syntax mới | ✅ Đã điền: `syntax_data_v2.md` (496 fields), `syntax_feature_v2.md` (36), `syntax_operations_v2.md` (7) |
| `syntax/*.md` đã viết lại | ✅ `data_syntax.md`, `feature_syntax.md`, `operations_syntax.md` (theo data bạn điền) |
| `template_example/strategy_framework.md` | ✅ Viết lại cho Round 2 (time_series + cross_sectional) |
| `migration_map_v2.md` | ✅ Đã điền (PV giữ, futures/session gates xoá, fundamentals mới) |
| Bạn đặt file strategy new-data | ⏳ Chờ bạn đặt vào `input/` (hoặc đặt thẳng theo template VN-*) |
| `tools/migrate_stage2.py` | ⏳ Tạo khi bạn giao strategy new-data |
| Phase A (archive vòng 1) | ⏳ Chờ bạn approve |

> **Lưu ý Round 2:** chiến lược vòng 1 (futures intraday) không migrate tự động được — sản phẩm, khung
> thời gian, direction đều đổi. File mới nên viết theo `template_example/VN-*/`.

---

## C. Quy trình sau khi bạn cung cấp xong

```
1. Bạn điền 5 template + đặt file .py vào input/
2. Tôi viết lại syntax/*.md theo dữ liệu bạn điền
3. Tôi viết tools/migrate_stage2.py (đọc migration_map + chuẩn hoá form)
4. Chạy migrate: input/*.py → output/stage_2/ + ghi output/index.csv
5. Validate bằng tools/validate_framework.py (mở rộng rule mới)
```

> **Lưu ý:** Thư mục này chỉ là tạm — file ở đây chưa được validate. Sau khi migrate xong, file nguồn có thể được xoá hoặc archive.
