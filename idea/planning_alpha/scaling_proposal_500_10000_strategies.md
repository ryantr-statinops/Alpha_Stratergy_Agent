# Scaling Proposal: 500-10,000 Strategies

**Problem:** Flat `output/` với 10,000 file là không thể quản lý. Cần tổ chức lại để tra cứu nhanh.

---

## 1. Output Structure

```
output/
├── index.csv                          # Tra cứu toàn bộ strategies
├── A_rolling_mean_level/              # Family A: ~200 files
│   ├── A-001_close_gt_mean_3.py
│   ├── A-002_close_lt_mean_3.py
│   └── ...
├── B_rolling_mean_crossover/          # Family B: ~110 files
├── C_mean_confirmation/               # Family C: ~100 files
├── D_rolling_quantile_level/          # Family D: ~180 files
├── E_quantile_channel/                # Family E: ~80 files
├── F_quantile_confirmation/           # Family F: ~80 files
├── G_multi_timeframe/                 # Family G: ~30 files
├── H_vnfuture_specific/               # Family H: ~50 files
├── I_combined_mean_quantile/          # Family I: ~30 files
└── J_advanced_patterns/               # Family J: ~30 files
```

Mỗi thư mục tối đa ~200 files, dễ duyệt.

---

## 2. Naming Convention

Format: `{alpha_id}_{price}_{logic_key}_{params}.py`

Ví dụ:
```
A-009_close_gt_mean_14.py       # close > rolling_mean(14)
C-001_close_mean14_rsi50.py     # close > mean(14) & RSI > 50
I-001_close_q80_mean14_rsi50.py # close > q80 & close > mean(14) & RSI > 50
```

Tên file tự giải thích logic, không cần mở file vẫn biết nội dung.

---

## 3. Index System (`output/index.csv`)

Một CSV để search/filter nhanh:

```csv
alpha_id,family,file,price,window,q,confirmation,direction
A-001,A_rolling_mean_level,A-001_close_gt_mean_3.py,close,3,,,LONG
A-002,A_rolling_mean_level,A-002_close_lt_mean_3.py,close,3,,,SHORT
C-001,C_mean_confirmation,C-001_close_mean14_rsi50.py,close,14,,RSI>50,LONG
I-001,I_combined_mean_quantile,I-001_close_q80_mean14_rsi50.py,close,14,0.8,RSI>50,LONG
```

Có thể mở bằng Excel, Google Sheets, hoặc filter bằng `grep`.

---

## 4. Generator Script (tùy chọn)

Chỉ 1 script duy nhất, đọc alpha doc → tự sinh 10,000 files + index.csv:

```
tools/generate_strategies.py
```

```python
# Cấu trúc đơn giản:
TEMPLATE = """
class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        {feature_code}
        {logic_code}
        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for params in PARAM_GRID:
    code = TEMPLATE.format(**params)
    write_file(path, code)
    append_to_index(alpha_id, path, params)
```

Chạy 1 lần, xong tất cả. Không cần tools khác.

---

## 5. So sánh: Hiện tại vs Sau scaling

| Khía cạnh | Hiện tại | Sau scaling |
|-----------|----------|-------------|
| `output/` | Flat, 1 file | 10 subdirectories + index.csv |
| Tìm strategy | Mở từng file | grep index.csv hoặc duyệt folder |
| Tạo mới | Viết tay từng file | Script hoặc copy template |
| Hiểu logic | Phải đọc code | Tên file + index là đủ |

---

## 6. Effort

| Task | Thời gian |
|------|-----------|
| Restructure output/ (tạo folder + move) | 5 phút |
| Tạo index.csv | 10 phút |
| Tạo generator script | 20 phút |
| **Tổng** | **~35 phút** |

---

*End of Simplified Scaling Proposal*
