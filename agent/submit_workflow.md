# Submit Workflow — Paste Code lên XNOQuant

> Xem thêm: [`tools/INDEX.md`](../tools/INDEX.md) để biết tổng quan tất cả tools.

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

### 1. Config — `.env` file

Tạo file `.env` ở project root (đã có `.gitignore`, không lo lộ token):

```env
XNO_EDITOR_ID="<paste-editor-uuid-here>"
XNO_TOKEN="<paste-bearer-token-here>"
```

Hoặc copy từ mẫu: `cp .env.example .env` và điền giá trị.

> **Cách lấy EDITOR_ID và TOKEN:** xem mục "Cách lấy EDITOR_ID và TOKEN" bên dưới.

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

Batch mode tự động đọc `backtest/results.csv` và **bỏ qua** các file
đã đạt cả 5 tiêu chí pass trước đó:
- Sharpe ≥ 1.3, CAGR ≥ 15%, MaxDD ≥ -35%, PF ≥ 1.2, Calmar ≥ 1.1

File bị skip hiển thị dòng `Skipped N file(s) (da pass all 5 tieu chi)` ở cuối.
Để submit lại file đã pass, dùng interactive mode.

### 3c. Interactive mode — cảnh báo file đã pass

Khi nhập path của file đã pass, script hỏi xác nhận:
```
[!] 'SF_KAMA_15min.py' da pass all 5 tieu chi truoc do. Submit lai? (y/N):
```
Nhập `y` để submit lại, `N` để bỏ qua.

> **Lưu ý quan trọng:**
> - Batch mode sẽ **không bao giờ** submit lại file đã pass cả 5 tiêu chí (trừ khi xoá dòng trong CSV hoặc dùng interactive)
> - `results.csv` là append-only, không ghi đè — dòng cuối cùng của mỗi file là kết quả mới nhất
> - Nếu muốn force resubmit tất cả: xoá file `backtest/results.csv` hoặc dùng interactive cho từng file

### 4. Kết quả

Metrics tự động lưu vào `backtest/results.csv`. Dùng `check_results.py` để review:

```bash
python tools/check_results.py --detail        # Full 5-metric table
python tools/check_results.py --pass          # PASS files only
python tools/check_results.py --prefix MF     # Filter by prefix
python tools/check_results.py --today         # Today's submissions
```

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
