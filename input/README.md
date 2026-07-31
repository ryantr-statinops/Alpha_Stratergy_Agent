# input/ — Thư mục tạm cho Migration V2

Thư mục này dùng để đặt các file strategy đã viết theo **data model mới (vòng 2)** trước khi migrate sang form chuẩn ở `output/stage_2/`.

Xem kế hoạch đầy đủ tại [`agent/migration_plan_v2.md`](../agent/migration_plan_v2.md).

## Quy trình

1. Đặt file `.py` viết theo data model mới vào đây.
2. `tools/migrate_stage2.py` đọc từng file, chuẩn hoá form chuẩn (4-layer pipeline, Exit→Long→Short, session gates, no forbidden patterns).
3. Xuất kết quả vào `output/stage_2/` + ghi `output/index.csv`.

> **Lưu ý:** Thư mục này chỉ là tạm — file ở đây chưa được validate. Sau khi migrate xong, file nguồn có thể được xoá hoặc archive.
