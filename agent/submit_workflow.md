# Submit Workflow — Paste Code lên XNOQuant

## Tổng quan

Quy trình submit 1 strategy lên `https://alpha.xnoquant.io/build` qua API:

```
PUT  /editors/{id}/update   # gửi code (body: {"code": "..."})
POST /editors/{id}/verify   # check syntax (empty body)
POST /editors/{id}/simulate # chạy backtest (empty body)
```

Auth: `Authorization: Bearer <token>`

---

## Cách lấy EDITOR_ID và TOKEN

1. Mở `https://alpha.xnoquant.io/build` trong Chrome
2. Mở DevTools → tab **Network** → filter **Fetch/XHR**
3. Paste 1 dòng code bất kỳ vào editor trên web
4. Tìm request **method PUT**, tên `update`
5. Right-click → **Copy → Copy as cURL (bash)**

Từ cURL đó lấy:
- **EDITOR_ID**: UUID sau `/editors/` và trước `/update`
  - Ví dụ: `a1619c25-f370-4461-9d47-ddfd2deb66dc`
- **TOKEN**: chuỗi sau `Bearer` trong header `authorization`
  - Ví dụ: `xq_pnLDPtb8VvmwVYPMnVDZehjSqsx1K8hr2vU`

---

## Dùng script `tools/submit_all.py`

### 1. Update config
Mở `tools/submit_all.py`, sửa 2 dòng đầu:

```python
EDITOR_ID = "a1619c25-f370-4461-9d47-ddfd2deb66dc"  # UUID mới nhất
TOKEN = "xq_pnLDPtb8VvmwVYPMnVDZehjSqsx1K8hr2vU"   # Token hiện tại
```

### 2. Test 1 variant
```bash
python tools/submit_all.py --test
```

### 3. Chạy full
```bash
python tools/submit_all.py
```

### Filter template muốn submit
Có thể sửa thủ công trong script hoặc dùng glob:

```python
# Chỉ submit T30-T38
files = sorted(glob.glob("output/thesis_3*/**/*.py", recursive=True))
# Hoặc chỉ 1 template
files = sorted(glob.glob("output/thesis_36_candle_body_ratio/*.py", recursive=True))
```

---

## API Response Codes

| Code | Ý nghĩa | Xử lý |
|------|---------|-------|
| **200** | Thành công | ✅ |
| **201** | Created | ✅ |
| **204** | No Content | ✅ |
| **400** | Lỗi syntax code | Sửa template trong `tools/generate_strategies.py`, regenerate |
| **429** | Rate limit | Tăng DELAY lên 10-15s, retry |
| **500** | Server error | Thử lại sau, check nếu code quá phức tạp |

### Debug 400 — Verify fail

Nguyên nhân thường gặp:
- Dùng `self.op.sub()`, `self.op.div()` — không tồn tại trong `self.op.*`; thay bằng Python operators (`a - b`, `a / b`)
- Biến `open` — bị từ khóa hệ thống; dùng `open_price`
- Dùng `self.feat.sub()`, `self.feat.div()` — có thể không được platform hỗ trợ; thay bằng Python operators

Cách fix:
1. Sửa template code string trong `tools/generate_strategies.py`
2. Chạy `python tools/generate_strategies.py` (regenerate)
3. Test lại với script

---

## Commit Rule

Sau mỗi lần sửa generator hoặc tạo file mới:

```bash
git add tools/generate_strategies.py
git commit -m "fix: mô tả ngắn gọn thay đổi"
git push
```

Không commit file trong `output/` (đã trong `.gitignore`).

---

## Workflow tối ưu

```
1. Sửa template trong generate_strategies.py
2. python tools/generate_strategies.py     # regenerate
3. python tools/submit_all.py --test       # test 1 variant
4. Kiểm tra trên web
5. python tools/submit_all.py              # submit full batch (delay 10s)
6. git add + git commit + git push         # commit generator changes
```
