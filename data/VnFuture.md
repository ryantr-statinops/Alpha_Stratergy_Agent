# Dữ liệu VnFuture (Hợp đồng tương lai VN30)

## Cách truy cập

Sử dụng `self.data.<tên_trường>` để truy cập dữ liệu.

## Danh sách các trường dữ liệu

### Group 1: Khối lượng & Giá trị khớp lệnh (Matched)

| Trường | Mô tả |
|--------|-------|
| `fut_matched_volume_vn30f1m_1d` | Khối lượng khớp lệnh hợp đồng tương lai VN30F1M |
| `fut_matched_value_vn30f1m_1d` | Giá trị khớp lệnh hợp đồng tương lai VN30F1M |

### Group 2: Thỏa thuận (Agreed)

| Trường | Mô tả |
|--------|-------|
| `fut_agreed_volume_vn30f1m_1d` | Khối lượng thỏa thuận hợp đồng tương lai VN30F1M |
| `fut_agreed_value_vn30f1m_1d` | Giá trị thỏa thuận hợp đồng tương lai VN30F1M |

### Group 3: Tổng hợp (Total)

| Trường | Mô tả |
|--------|-------|
| `fut_total_volume_vn30f1m_1d` | Tổng khối lượng (khớp lệnh + thỏa thuận) |
| `fut_total_value_vn30f1m_1d` | Tổng giá trị (khớp lệnh + thỏa thuận) |

### Group 4: Hợp đồng mở (Open Interest)

| Trường | Mô tả |
|--------|-------|
| `fut_open_interest_vn30f1m_1d` | Số lượng hợp đồng mở (Open Interest) |

## Quy ước đặt tên

```
fut_<loại>_<mã_hợp_đồng>_<khung_thời_gian>
```

- `fut_`: prefix chỉ thị trường tương lai
- `<loại>`: matched_volume, matched_value, agreed_volume, agreed_value, total_volume, total_value, open_interest
- `<mã_hợp_đồng>`: vn30f1m (VN30 Future 1 month)
- `<khung_thời_gian>`: 1d (Daily)

## Lưu ý

- Không sử dụng tên biến trùng với từ khóa hệ thống (ví dụ: tránh `open`, `volume` một mình).
- Các trường `fut_matched_volume` và `fut_matched_value` là dữ liệu phổ biến nhất cho phân tích thanh khoản.
- `fut_open_interest` quan trọng cho phân tích dòng tiền và tâm lý thị trường.
