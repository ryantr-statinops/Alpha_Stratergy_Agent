# syntax_operations_v2 — Template cung cấp operators mới

> **Mục đích:** Bạn điền danh sách các toán tử (`self.op.*`) mới của vòng 2.
> File này sẽ được dùng để viết lại `syntax/operations_syntax.md`.
> **Tham chiếu:** [`agent/migration_plan_v2.md`](../../agent/migration_plan_v2.md) — Phase B.

## Cách điền

1. Liệt kê **tất cả** operators mới, chia theo nhóm (Cross/Event, Lag/Time, Mask/Conditional, Signal Persistence, Boolean).
2. Cột `Operator` = tên chính xác dùng trong code (`self.op.<name>`).
3. Cột `Usage` = cú pháp + tham số (vd `crossed_above(a, b)`).
4. Cột `Return` = kiểu trả về (vd `Series[bool]`).
5. Cột `Mới?` = ❌ giữ nguyên / ✅ mới / ⚠️ đổi behaviour.

---

## 1. Cross / Event

| Operator | Usage | Return | Mới? |
|----------|-------|:------:|:----:|
| *(vd: `crossed_above`)* | *(vd: `crossed_above(a, b)`)* | *(vd: Series[bool])* | *(vd: ❌)* |
| | | | |

## 2. Lag / Time

| Operator | Usage | Return | Mới? |
|----------|-------|:------:|:----:|
| | | | |

## 3. Range / Mask / Conditional

| Operator | Usage | Return | Mới? |
|----------|-------|:------:|:----:|
| | | | |

## 4. Signal Persistence

| Operator | Usage | Return | Mới? |
|----------|-------|:------:|:----:|
| | | | |

## 5. Boolean Logic

| Operator | Usage | Return | Mới? |
|----------|-------|:------:|:----:|
| | | | |

---

## Ghi chú thêm (nếu có)

- Operator nào bị xoá / deprecated ở vòng 2:
- Ràng buộc causal-safety mới (shift/diff/pct_change...):
- Operator mới thay thế pattern cũ nào:
