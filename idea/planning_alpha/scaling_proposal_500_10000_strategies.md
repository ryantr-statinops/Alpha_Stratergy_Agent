# Scaling Proposal: 500-10,000 Strategies

**Problem hiện tại:**
- `output/` là flat folder — 10,000 file trong 1 thư mục là không thể quản lý
- Không có index để tra cứu strategy
- Phải gen từng file thủ công
- Không có hệ thống test batch

---

## 1. Cấu trúc thư mục mới

```
ALPHA_BOT/
├── output/                          # Chiến lược hoàn chỉnh (.py)
│   ├── index.csv                    # Master manifest (tra cứu toàn bộ)
│   ├── family_a_mean_level/         # Family A: 200 strategies
│   │   ├── A-001_close_gt_mean_3.py
│   │   ├── A-002_close_lt_mean_3.py
│   │   └── ...
│   ├── family_b_mean_crossover/     # Family B: 110 strategies
│   ├── family_c_mean_confirmation/  # Family C: 100 strategies
│   ├── family_d_quantile_level/     # Family D: 180 strategies
│   ├── family_e_quantile_channel/   # Family E: 80 strategies
│   └── ...
│
├── tools/                           # Scripts automation
│   ├── generate_all.py              # Gen strategies tự động từ alpha doc
│   ├── validate_all.py              # Validate syntax tất cả file
│   └── update_index.py              # Cập nhật index.csv
│
├── tests/                           # Testing pipeline
│   ├── config.yaml                  # Backtest config
│   ├── runner.py                    # Batch test runner
│   └── results/                     # Kết quả test
│       ├── summary.csv
│       └── detailed/
│
└── template_example/
    └── strategy_framework.md        # (Đã có)
```

---

## 2. Index System (`output/index.csv`)

Một file CSV master để tra cứu bất kỳ strategy nào:

```csv
alpha_id,family,file_path,price_source,window,q_value,confirmation,direction,status,created_date
A-001,A,family_a_mean_level/A-001_close_gt_mean_3.py,close,3,,,LONG,pending,2026-07-01
A-002,A,family_a_mean_level/A-002_close_lt_mean_3.py,close,3,,,SHORT,pending,2026-07-01
C-001,C,family_c_mean_confirmation/C-001_mean_rsi_14.py,close,14,,RSI>50,LONG,pending,2026-07-01
...
```

**Cột `status`:** `pending` → `generated` → `validated` → `live` → `deprecated`

---

## 3. Batch Generation (`tools/generate_all.py`)

Script đọc alpha doc param grid và tự động sinh file `.py`:

```python
# Pseudo-code
PARAM_GRID = {
    "A": {
        "price_sources": ["close", "typical_price", ...],
        "windows": [3, 5, 8, 10, 14, 20, ...],
        "directions": ["LONG", "SHORT"],
    },
    "C": {
        "price_sources": ["close"],
        "windows": [14, 20, 50],
        "confirmations": ["RSI>50", "ADX>20", "MACD>Signal", ...],
    },
    ...
}

def generate_strategy(family_id, params):
    template = load_template(family_id)
    code = template.render(**params)
    write_file(f"output/family_{family_id}/{filename}.py", code)
    append_to_index(alpha_id, family_id, filepath, params)

for family, grid in PARAM_GRID.items():
    for combo in product(**grid):
        generate_strategy(family, combo)
```

**Lợi ích:**
- 10,000 strategies = 1 lần chạy script (vài phút)
- Đảm bảo format đồng bộ
- Index tự động cập nhật

---

## 4. Batch Validation (`tools/validate_all.py`)

Kiểm tra toàn bộ strategies cùng lúc:

```bash
python tools/validate_all.py
```

**Chức năng:**
- Syntax check (`ast.parse`) tất cả file .py
- Check compliance với strategy_framework.md
- Báo cáo file lỗi → output/errors.csv

---

## 5. Testing Pipeline (`tests/`)

Chạy backtest hàng loạt, so sánh kết quả:

```
tests/
├── config.yaml          # Chung: timeframe, slippage, commission, date range
├── runner.py            # Đọc index.csv → backtest từng strategy → ghi kết quả
└── results/
    ├── summary.csv      # Tất cả strategies sorted by Sharpe, Win Rate, PF
    └── detailed/        # Chi tiết từng strategy
        ├── A-001_report.json
        ├── C-001_report.json
        └── ...
```

**`summary.csv` output:**
```csv
alpha_id,win_rate,profit_factor,sharpe,max_dd,trades,status
A-009,0.55,1.35,0.92,0.12,45,VALIDATED
C-001,0.52,1.20,0.78,0.14,38,VALIDATED
...
```

---

## 6. Workflow cho 10,000 Strategies

```
Bước 1: Sinh strategies
  python tools/generate_all.py              # Tạo 10,000 file .py
  python tools/validate_all.py               # Validate syntax

Bước 2: Batch backtest
  python tests/runner.py                     # Chạy tất cả

Bước 3: Sàng lọc
  Dựa vào summary.csv → chọn top 5-10%
  → Cần tối thiểu: Sharpe > 0.5, Win Rate > 50%, PF > 1.2

Bước 4: Deep test (từ hypothesis_framework.md)
  Chỉ test kỹ các strategy đã qua sàng lọc:
  - Multi-timeframe check
  - Market regime test
  - Walk-forward validation

Bước 5: Deploy
  output/index.csv status = live
```

---

## 7. Tổng kết thay đổi

| Component | Hiện tại | Sau scaling |
|-----------|----------|-------------|
| `output/` | Flat (1 file) | 10+ subdirectories + index.csv |
| Sinh strategy | Thủ công | Script `tools/generate_all.py` |
| Validate | Thủ công | Script `tools/validate_all.py` |
| Test | Không có | `tests/runner.py` + `tests/results/` |
| Tra cứu | Không có | `output/index.csv` |

---

## 8. Effort ước tính

| Task | Thời gian |
|------|-----------|
| Tạo `tools/generate_all.py` | ~30 phút |
| Tạo `tools/validate_all.py` | ~15 phút |
| Tạo `tests/runner.py` | ~30 phút |
| Restructure `output/` | ~10 phút |
| **Tổng** | **~1.5 giờ** |

---

*End of Scaling Proposal*
