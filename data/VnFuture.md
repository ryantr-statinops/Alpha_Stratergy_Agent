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

---

### Group 5: VN30 Index (`pv_vn30_*`)

Dữ liệu chỉ số VN30 cơ sở — dùng để so sánh tương quan với hợp đồng tương lai.

| Trường | Mô tả |
|--------|-------|
| `pv_vn30_open` | Giá mở cửa chỉ số VN30 |
| `pv_vn30_high` | Giá cao nhất chỉ số VN30 |
| `pv_vn30_low` | Giá thấp nhất chỉ số VN30 |
| `pv_vn30_close` | Giá đóng cửa chỉ số VN30 |
| `pv_vn30_volume` | Khối lượng chỉ số VN30 |

---

### Group 6: Dow Jones Index (`pv_dji_*`)

Dữ liệu chỉ số Dow Jones — dùng cho phân tích cross-market và global momentum spillover.

| Trường | Mô tả |
|--------|-------|
| `pv_dji_open` | Giá mở cửa Dow Jones |
| `pv_dji_high` | Giá cao nhất Dow Jones |
| `pv_dji_low` | Giá thấp nhất Dow Jones |
| `pv_dji_close` | Giá đóng cửa Dow Jones |
| `pv_dji_volume` | Khối lượng Dow Jones |

---

## Ứng dụng theo Thesis Group

| Thesis Group | Data Fields Chính |
|--------------|-------------------|
| Momentum / Trend Following | `pv_close`, `pv_high`, `pv_low` |
| Mean Reversion | `pv_close` + quantiles |
| Breakout | `pv_close`, `pv_volume`, `fut_*` |
| Cross-Market | `pv_close`, `pv_vn30_*`, `pv_dji_*` |
| Volume & Flow | `fut_matched_volume`, `fut_open_interest`, `fut_total_volume` |
| Intraday Session | `pv_open`, `pv_close`, `pv_high`, `pv_low` |
| Multi-Factor Composite | Tất cả fields |

---

## Lưu ý

- Không sử dụng tên biến trùng với từ khóa hệ thống (ví dụ: tránh `open`, `volume` một mình).
- Các trường `fut_matched_volume` và `fut_matched_value` là dữ liệu phổ biến nhất cho phân tích thanh khoản.
- `fut_open_interest` quan trọng cho phân tích dòng tiền và tâm lý thị trường.
- `pv_vn30_close` và `pv_dji_close` dùng cho cross-market relative strength analysis.
- Dữ liệu `pv_vn30_*` và `pv_dji_*` có cùng khung thời gian với `pv_close` (theo config của strategy).
