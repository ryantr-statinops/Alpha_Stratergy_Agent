# ALPHA_BOT - Quantitative Strategy Builder Engine

## 1. Project Overview & Purpose

Dự án này là môi trường nghiên cứu và phát triển chiến lược đầu tư định lượng (Quantitative Trading) dành riêng cho nền tảng **XNOQuant**.

Mục đích cốt lõi của không gian làm việc này là giúp AI Agent đọc hiểu sâu sắc cấu trúc cú pháp, dữ liệu đầu vào và các hàm chức năng được nền tảng cung cấp. Từ đó, AI có thể tự động hóa quy trình lên ý tưởng (Alpha Generation), lập kế hoạch kiểm thử và viết mã nguồn chiến lược hoàn chỉnh một cách chính xác mà không vi phạm các quy tắc của hệ thống.

---

## 2. Project Structure

```text
ALPHA_BOT/
├── data/                   # Tài liệu về dữ liệu đầu vào (Close, High, Low, Volume, ...)
├── feature/                # Danh mục chỉ báo kỹ thuật (EMA, RSI, BBands, Hikkake, ...)
├── operations/             # Danh mục toán tử xử lý chuỗi thời gian (crossed_above, fillna, ...)
├── template_example/       # Các chiến lược mẫu chạy được trên XNOQuant
├── idea/                   # Nơi lưu trữ các ý tưởng nghiên cứu (.md)
│   ├── planning_alpha/     # Kế hoạch phát triển Alpha theo từng chủ đề
│   └── hypothesis/         # Giả thuyết kiểm thử và ý tưởng thử nghiệm
├── output/                 # Mã nguồn chiến lược hoàn chỉnh (.py)
└── README.md               # Tài liệu hướng dẫn dành cho AI Agent
```

---

## 3. Knowledge Base Reference (AI Onboarding Guide)

Trước khi thực hiện bất kỳ yêu cầu nào từ người dùng, AI Agent **bắt buộc** phải đọc và phân tích các thư mục sau để xây dựng ngữ cảnh (Context) làm việc.

### `data/`

- Hiểu cách truy cập dữ liệu thị trường.
- Ví dụ: `self.data.pv_close`, `self.data.fut_matched_volume_vn30f1m_1d`.
- Không sử dụng tên biến trùng với từ khóa của hệ thống.
  - ✅ `open_price`
  - ❌ `open`

#### Danh sách trường dữ liệu VnFuture (Hợp đồng tương lai VN30F1M)

| Trường | Ý nghĩa |
|--------|---------|
| `fut_matched_volume_vn30f1m_1d` | Khối lượng khớp lệnh |
| `fut_matched_value_vn30f1m_1d` | Giá trị khớp lệnh |
| `fut_agreed_volume_vn30f1m_1d` | Khối lượng thỏa thuận |
| `fut_agreed_value_vn30f1m_1d` | Giá trị thỏa thuận |
| `fut_total_volume_vn30f1m_1d` | Tổng khối lượng (khớp lệnh + thỏa thuận) |
| `fut_total_value_vn30f1m_1d` | Tổng giá trị (khớp lệnh + thỏa thuận) |
| `fut_open_interest_vn30f1m_1d` | Hợp đồng mở (Open Interest) |

Chi tiết xem tại [`data/VnFuture.md`](data/VnFuture.md).

### `feature/`

- Tra cứu toàn bộ các chỉ báo kỹ thuật được nền tảng hỗ trợ.
- Chỉ sử dụng các hàm có sẵn trong thư mục này khi xây dựng chiến lược.

### `operations/`

- Tra cứu các toán tử xử lý dữ liệu chuỗi thời gian.
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

Mọi chiến lược được sinh ra phải:

- Kế thừa từ lớp `CustomStrategy`
- Sử dụng cấu trúc giống các file mẫu
- Định nghĩa logic bên trong:

```python
def __logic__(self):
```

Hoặc tuân thủ hoàn toàn cấu trúc của các file mẫu trong thư mục này.

---

## 4. Operational Workflow

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
idea/planning_alpha/
```

#### Hypothesis Loop

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
  - các hàm trong `feature/`
  - các hàm trong `operations/`
- Tuân thủ tuyệt đối cấu trúc trong:

```text
template_example/
```

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

## 5. Supreme Directive

AI Agent **không được phép**:

- tự ý sử dụng thư viện ngoài
- tự ý thay đổi framework
- tự ý thay đổi cấu trúc `CustomStrategy`

AI Agent **luôn phải**:

1. Kiểm tra tính tương thích với `CustomStrategy`.
2. Chỉ sử dụng các API chính thức của XNOQuant.
3. Tuân thủ cú pháp của `feature/`, `operations/` và `template_example/`.
4. Đảm bảo mã nguồn có thể chạy trực tiếp trên nền tảng.
