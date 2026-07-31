# syntax_feature_v2 — Template cung cấp feature functions mới

> **Mục đích:** Bạn điền danh sách các hàm chỉ báo (`self.feat.*`) mới của vòng 2.
> File này sẽ được dùng để viết lại `syntax/feature_syntax.md`.
> **Tham chiếu:** [`agent/migration_plan_v2.md`](../../agent/migration_plan_v2.md) — Phase B.

## Cách điền

1. Liệt kê **tất cả** feature functions mới, chia theo nhóm (Trend, Momentum, Volatility, ...).
2. Cột `Function` = tên chính xác dùng trong code (`self.feat.<name>`).
3. Cột `Signature` = đầy đủ tham số (vd `close, timeperiod=14`).
4. Cột `Return` = `series` / `tuple` (nếu tuple, ghi rõ thứ tự output).
5. Cột `Mới?` = ❌ giữ nguyên / ✅ mới / ⚠️ đổi signature.

---

## 1. Trend & Moving Average

| Function | Signature | Return | Mới? |
|----------|-----------|:------:|:----:|
| *(vd: `sma`)* | *(vd: `close, timeperiod=10`)* | *(vd: series)* | *(vd: ❌)* |
| | | | |

## 2. Momentum / Oscillator

| Function | Signature | Return | Mới? |
|----------|-----------|:------:|:----:|
| | | | |

## 3. Volatility

| Function | Signature | Return | Mới? |
|----------|-----------|:------:|:----:|
| | | | |

## 4. Volume / Flow

| Function | Signature | Return | Mới? |
|----------|-----------|:------:|:----:|
| | | | |

## 5. Rolling Statistics

| Function | Signature | Return | Mới? |
|----------|-----------|:------:|:----:|
| | | | |

## 6. Candlestick Patterns

| Function | Signature | Return | Mới? |
|----------|-----------|:------:|:----:|
| | | | |

## 7. Price Normalization / Khác

| Function | Signature | Return | Mới? |
|----------|-----------|:------:|:----:|
| | | | |

---

## Ghi chú thêm (nếu có)

- Hàm nào bị xoá / deprecated ở vòng 2:
- Hàm nào đổi return type (series ↔ tuple):
- Quy ước tham số mới (nếu có):
