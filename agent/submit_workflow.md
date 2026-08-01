# Submit Workflow — Paste Code lên XNOQuant

> Xem thêm: [`tools/INDEX.md`](../tools/INDEX.md) để biết tổng quan tất cả tools.
>
> **Round 2 (ACTIVE):** API giống vòng 1 nhưng script quét `output/stage_2/`, kết quả
> ghi vào `backtest/results_stage_2.csv`, và pass criteria **theo universe** (xem §2 Round 2 bên dưới).
> Các mục đánh dấu (vòng 1) là reference archived.

## Tổng quan

Quy trình submit 1 strategy lên `https://alpha.xnoquant.io/build` qua API:

```
PUT  /editors/{id}/update                                          # gửi code (body: {"code": "..."})
POST /editors/{id}/verify                                          # check syntax (empty body)
POST /editors/{id}/simulate                                        # chạy backtest (empty body)
GET  /editors/{id}/info                                            # lấy strategy_id
GET  /strategies/{id}/stages/simulate/summary-aggregate            # lấy metrics (CAGR, Sharpe, ...)
```

Auth: `Authorization: Bearer <token>`

---

## Round 2 — submit strategy daily equity

```bash
# 0. Validate strict (bắt warning) trước khi submit
python tools/validate_framework.py --strict

# 1. Xem trước editor/universe/files — KHÔNG gọi API (an toàn)
python tools/submit_and_check.py --batch --dry-run --universe VN-SMALL-CAP

# 2. Chọn đúng universe trên giao diện XNOQuant (thủ công, UI KHÔNG đổi qua API)
#    rồi live test 1 file đầu:
python tools/submit_and_check.py --batch --test --universe VN-SMALL-CAP

# 3. Submit cả cap (single editor => một cap mỗi lần chạy)
python tools/submit_and_check.py --batch --universe VN-SMALL-CAP

# Review kết quả (backtest/results_stage_2.csv), PASS/FAIL theo universe
python tools/check_results.py --detail --universe VN-SMALL-CAP
```

**Bộ tiêu chí pass Round 2 (theo universe):**

| Universe | Sharpe | CAGR | MaxDD | PF | Calmar |
|----------|:------:|:----:|:-----:|:--:|:------:|
| VN-SMALL-CAP | ≥ 1.0 | ≥ 25% | ≥ -45% | ≥ 1.3 | ≥ 0.8 |
| VN-MID-CAP | ≥ 1.1 | ≥ 20% | ≥ -40% | ≥ 1.25 | ≥ 1.0 |
| VN-LARGE-CAP | ≥ 1.2 | ≥ 15% | ≥ -35% | ≥ 1.2 | ≥ 1.1 |

- File Round 2 không khai báo universe trong code — **universe ghi vào CSV luôn suy từ path** `output/stage_2/<cap>/...` (VD `vn_small_cap/` → `VN-SMALL-CAP`). `--universe` chỉ là FILTER chọn cap, KHÔNG ghi đè universe của file.
- Nếu submit `--files` cho vài file riêng lẻ: `python tools/submit_and_check.py --files a.py b.py --universe VN-LARGE-CAP` (tất cả phải cùng cap).

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
XNO_EDITOR_ID_SMALL="<editor-uuid-cho-VN-SMALL-CAP>"
XNO_EDITOR_ID_MID="<editor-uuid-cho-VN-MID-CAP>"
XNO_EDITOR_ID_LARGE="<editor-uuid-cho-VN-LARGE-CAP>"
XNO_TOKEN="<paste-bearer-token-here>"
```

Hoặc copy từ mẫu: `cp .env.example .env` và điền giá trị.

> **Khuyến nghị: 1 editor / cap** — mỗi editor set cố định đúng universe trên UI
> (`alpha.xnoquant.io/build`). Tool tự chọn editor theo cap folder, không cần đổi
> UI giữa các lần submit. Còn lại `XNO_EDITOR_ID` (legacy, 1 editor dùng chung)
> làm fallback nếu thiếu ID per-universe.

> **Cách lấy EDITOR_ID và TOKEN:** xem mục "Cách lấy EDITOR_ID và TOKEN" bên dưới.

### 2. Interactive mode — submit từng file (vòng 1)

```bash
python tools/submit_and_check.py
```

Sau khi chạy:
- Nhập đường dẫn file `.py` cần submit (vd: `output/single_feat_alpha/SF_RSI_15min.py`)
- Script sẽ: submit → verify → simulate → đợi 10s → fetch metrics → lưu vào CSV
- Nhập `done` để kết thúc
- Nhập `help` để xem lại hướng dẫn

### 3. Batch mode — submit tất cả file (vòng 1)

```bash
python tools/submit_and_check.py --batch      # submit tất cả
python tools/submit_and_check.py --batch --test  # submit 1 file để test
```

> (vòng 1) Batch mode tự động đọc `backtest/results.csv` và **bỏ qua** các file
> đã đạt cả 5 tiêu chí pass trước đó:
> - Sharpe ≥ 1.3, CAGR ≥ 15%, MaxDD ≥ -35%, PF ≥ 1.2, Calmar ≥ 1.1

File bị skip hiển thị dòng `Skipped N file(s) (da pass all 5 tieu chi)` ở cuối.
Để submit lại file đã pass, dùng interactive mode.

### 3c. Interactive mode — cảnh báo file đã pass

Khi nhập path của file đã pass, script hỏi xác nhận:
```
[!] 'SF_KAMA_15min.py' da pass all 5 tieu chi truoc do. Submit lai? (y/N):
```
Nhập `y` để submit lại, `N` để bỏ qua.

> **Lưu ý quan trọng (vòng 1):**
> - Batch mode sẽ **không bao giờ** submit lại file đã pass cả 5 tiêu chí (trừ khi xoá dòng trong CSV hoặc dùng interactive)
> - `results.csv` là append-only, không ghi đè — dòng cuối cùng của mỗi file là kết quả mới nhất
> - Nếu muốn force resubmit tất cả: xoá file `backtest/results.csv` hoặc dùng interactive cho từng file

### 4. Kết quả

**Round 2:** metrics tự động lưu vào `backtest/results_stage_2.csv` (có cột `universe`, `filepath`, `status`, `strategy_id`). Review:

```bash
python tools/check_results.py --detail                    # Full 5-metric table
python tools/check_results.py --pass --universe VN-SMALL-CAP   # PASS + theo universe
python tools/check_results.py --prefix VnTop              # Filter by prefix
python tools/check_results.py --today                     # Today's submissions
```

```csv
timestamp,filepath,filename,universe,mode,status,strategy_id,cagr,sharpe,calmar,max_drawdown,profit_factor,error
2026-08-01T15:50,vn_small_cap/time_series/VnTop30Trend.py,VnTop30Trend.py,VN-SMALL-CAP,time_series,SIMULATED,s123,0.30,1.40,1.00,-0.30,1.60,
```

Status: `SIMULATED` / `UPDATE_FAILED` / `VERIFY_FAILED` / `SIMULATE_FAILED` / `RATE_LIMITED` / `METRICS_TIMEOUT` / `NO_STRATEGY_ID`.

(vòng 1) Dữ liệu cũ nằm ở `backtest/results.csv` — trích pass theo tiêu chí:
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

**Round 2:**
```
1. Agent viết strategy theo agent/framework_build_guide.md → output/stage_2/<cap>/<mode>/ + index.csv
2. python tools/validate_framework.py --strict                         # check compliance
3. python tools/submit_and_check.py --batch --dry-run --universe VN-SMALL-CAP  # xem trước (no HTTP)
4. Chọn VN-SMALL-CAP trên UI XNOQuant → python tools/submit_and_check.py --batch --test --universe VN-SMALL-CAP
5. Kiểm tra metrics trong console + backtest/results_stage_2.csv
6. python tools/submit_and_check.py --batch --universe VN-SMALL-CAP    # submit full batch (cùng cap)
7. python tools/check_results.py --detail --universe VN-SMALL-CAP      # review
```

(vòng 1) Workflow cũ — đã archive:
```
1. Gen/sửa file alpha trong output/single_feat_alpha/
2. python tools/submit_and_check.py --batch --test  # test 1 file
3. Kiểm tra metrics trong console + backtest/results.csv
4. python tools/submit_and_check.py --batch          # submit full batch
5. Mở backtest/results.csv để review tất cả kết quả
```
