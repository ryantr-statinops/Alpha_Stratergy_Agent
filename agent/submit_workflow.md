# Submit Workflow — Paste Code lên XNOQuant

## Tổng quan

Quy trình submit 1 strategy lên `https://alpha.xnoquant.io/build` qua API:

```
PUT  /editors/{id}/update                                          # gửi code (body: {"code": "..."})
POST /editors/{id}/verify                                          # check syntax (empty body)
POST /editors/{id}/simulate                                        # chạy backtest (empty body)
GET  /editors/{id}/info                                            # lấy strategy_id
GET  /v1/strategies/{id}/stages/train/summary-aggregate            # lấy metrics (CAGR, Sharpe, ...)
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

## Dùng script `tools/submit_and_check.py`

### 1. Update config

Mở `tools/submit_and_check.py`, sửa 2 dòng đầu:

```python
EDITOR_ID = "a1619c25-f370-4461-9d47-ddfd2deb66dc"  # UUID mới nhất
TOKEN = "xq_pnLDPtb8VvmwVYPMnVDZehjSqsx1K8hr2vU"   # Token hiện tại
```

### 2. Interactive mode — submit từng file

```bash
python tools/submit_and_check.py
```

Sau khi chạy:
- Nhập đường dẫn file `.py` cần submit (vd: `output/single_feat_alpha/SF_RSI_15min.py`)
- Script sẽ: submit → verify → simulate → đợi 10s → fetch metrics → lưu vào CSV
- Nhập `done` để kết thúc
- Nhập `help` để xem lại hướng dẫn

### 3. Batch mode — submit tất cả file

```bash
python tools/submit_and_check.py --batch      # submit tất cả
python tools/submit_and_check.py --batch --test  # submit 1 file để test
```

### 4. Kết quả

Metrics tự động lưu vào `backtest/results.csv`:

```csv
timestamp,filename,status,cagr,sharpe,calmar,max_drawdown,profit_factor
2026-07-15T15:50,SF_RSI_15min.py,OK,0.12,0.45,0.30,-0.40,1.10
2026-07-15T15:51,SF_CCI_15min.py,OK,-0.05,-0.20,-0.10,-0.50,0.90
```

Lưu ý:
khi user yêu cầu trích kết quả pass, tức là trích ra các file chạy thỏa các mục tiêu sau:
- Sharpe Ratio:  ≥ 1.3
- CAGR: ≥ 15%
- Max Drawdown: ≥ -35%
- Profit factor: ≥ 1.2
- Calmar: ≥ 1.1
---

## API Response Codes

| Code | Ý nghĩa | Xử lý |
|------|---------|-------|
| **200** | Thành công | ✅ |
| **201** | Created | ✅ |
| **204** | No Content | ✅ |
| **400** | Lỗi syntax code | Sửa template, regenerate |
| **429** | Rate limit | Tăng DELAY lên 10-15s, retry |
| **500** | Server error | Thử lại sau, check nếu code quá phức tạp |

### Debug 400 — Verify fail

Nguyên nhân thường gặp:
- Dùng `self.op.sub()`, `self.op.div()` — không tồn tại; thay bằng Python operators (`a - b`, `a / b`)
- Biến `open` — bị từ khóa hệ thống; dùng `open_price`
- Dùng `self.feat.sub()`, `self.feat.div()` — có thể không được platform hỗ trợ

Cách fix:
1. Sửa code trong file `.py`
2. Chạy lại script

---

## Workflow tối ưu

```
1. Gen/sửa file alpha trong output/single_feat_alpha/
2. python tools/submit_and_check.py --batch --test  # test 1 file
3. Kiểm tra metrics trong console + backtest/results.csv
4. python tools/submit_and_check.py --batch          # submit full batch
5. Mở backtest/results.csv để review tất cả kết quả
```
