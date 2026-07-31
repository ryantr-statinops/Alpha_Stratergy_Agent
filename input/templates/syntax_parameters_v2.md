# syntax_parameters_v2 — Template cung cấp parameters mới

> **Mục đích:** Bạn điền bộ tham số chuẩn mới cho từng timeframe (đặc biệt 15m) theo data model mới.
> File này sẽ được dùng để viết lại `syntax/parameters.md`.
> **Tham chiếu:** [`agent/migration_plan_v2.md`](../../agent/migration_plan_v2.md) — Phase B.

## Cách điền

1. Chọn timeframe cần điền (mặc định **15m** cho VNFuture; thêm 5m/30m/60m nếu có).
2. Cột `Feature` = tên chỉ báo.
3. Cột `Parameter` = tên tham số (vd `timeperiod`, `window`, `fastperiod`).
4. Cột `Giá trị` = giá trị chuẩn theo data model mới.
5. Cột `Ghi chú` = lý do / nguồn tham chiếu.

---

## Timeframe: 15m (VNFuture)

| Feature | Parameter | Giá trị | Ghi chú |
|---------|-----------|:-------:|---------|
| *(vd: `adx`)* | *(vd: `timeperiod`)* | *(vd: `10`)* | *(vd: theo vòng 1)* |
| | | | |

## Timeframe: 5m

| Feature | Parameter | Giá trị | Ghi chú |
|---------|-----------|:-------:|---------|
| | | | |

## Timeframe: 30m

| Feature | Parameter | Giá trị | Ghi chú |
|---------|-----------|:-------:|---------|
| | | | |

## Timeframe: 60m

| Feature | Parameter | Giá trị | Ghi chú |
|---------|-----------|:-------:|---------|
| | | | |

---

## Tham số phiên (session gates) mới

| Parameter | Giá trị mới | Ghi chú |
|-----------|-------------|---------|
| *(vd: `position_open_ranges`)* | *(vd: `["02:00-04:30", "06:00-07:20"]`)* | *(vd: UTC)* |
| | | |

## Ghi chú thêm (nếu có)

- Timeframe nào có cấu trúc phiên khác so với vòng 1:
- Tham số default nào bị thay đổi do data model mới:
