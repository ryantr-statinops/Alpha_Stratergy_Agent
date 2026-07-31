# syntax_data_v2 — Template cung cấp data fields mới

> **Mục đích:** Bạn điền danh sách data fields mới của vòng 2 (data model mới trên XNOQuant).
> File này sẽ được dùng để viết lại `syntax/data_syntax.md`.
> **Tham chiếu:** [`agent/migration_plan_v2.md`](../../agent/migration_plan_v2.md) — Phase B.

## Cách điền

1. Liệt kê **tất cả** data fields mới theo nhóm.
2. Cột `Field` = tên chính xác dùng trong code (`self.data.<field>`).
3. Cột `Ý nghĩa` = mô tả ngắn.
4. Cột `Timeframe` = timeframe khả dụng (vd `15m`, `1d`, `all`).
5. Đánh dấu field nào là field mới (chưa từng có ở vòng 1).

---

## 1. Core OHLCV

| Field | Ý nghĩa | Timeframe | Mới? |
|-------|---------|-----------|:----:|
| *(vd: `pv_close`)* | *(vd: giá đóng cửa)* | *(vd: all)* | *(vd: ❌ giữ nguyên / ✅ mới / ⚠️ đổi tên)* |
| | | | |
| | | | |

## 2. VN30 Index

| Field | Ý nghĩa | Timeframe | Mới? |
|-------|---------|-----------|:----:|
| | | | |

## 3. Dow Jones Index

| Field | Ý nghĩa | Timeframe | Mới? |
|-------|---------|-----------|:----:|
| | | | |

## 4. Futures / Phái sinh

| Field | Ý nghĩa | Timeframe | Mới? |
|-------|---------|-----------|:----:|
| | | | |

## 5. Macro / Khác

| Field | Ý nghĩa | Timeframe | Mới? |
|-------|---------|-----------|:----:|
| | | | |

---

## Ghi chú thêm (nếu có)

- Quy ước đặt tên field mới: *(vd: `fut_<type>_<contract>_<tf>`)*
- Field nào bị xoá / deprecated ở vòng 2:
- Điểm khác biệt so với vòng 1 (nếu có):
