# LARGE-CAP Quarterly Batch 1 — Pre-registration

> **Date:** 2026-08-05
> **Context:** Pivot sang VN-LARGE-CAP theo quyết định (fresh universe chống overfit từ vòng
> SMALL financial/payout). LARGE là universe mỏng nhất (~30 mã, 0 file qua Gate 1–3 trong
> quét 84 train-pass), nên **quarterly pivot là thay đổi cấu trúc chính** — tăng sample size
> và độ tươi của fundamental, không sinh thêm alpha style cũ.
> **Discipline:** áp đủ 6 gates từ ngày 1; test 2023–24 OOS locked (mỗi file dùng 1 lần).

## Hypothesis (cam kết trước khi xem kết quả)

| # | Giả thuyết | So sánh trực tiếp |
|---|-----------|-------------------|
| H1 | Quarterly beat Annual trên LARGE (sample size + freshness) | `VnLargeCsQFinancialNetPayout` vs `VnLargeCsFinancialNetPayout` (annual, test 0.518) |
| H2 | Financial-only > broad trên LARGE (financial = alpha driver, lặp lại kết quả SMALL) | `VnLargeCsQFinancialNetPayout` vs `VnLargeCsQNetPayoutPersistence` |
| H3 | Quality quarterly (ROA/ROE) trên LARGE qua Gate 1–3 (pattern `VnSmallCsRoaQuality` 5/5) | Gate 1–3 của 2 file quality |

## Files (4, đều cross_sectional, quarterly `_panel`)

| File | Signal | Population | Gate |
|------|--------|-----------|------|
| `VnLargeCsQFinancialNetPayout.py` | net payout yield EMA-smoothed | financial (bank/securities/insurance) | H1+H2 |
| `VnLargeCsQNetPayoutPersistence.py` | net payout yield EMA-smoothed | broad | H2 |
| `VnLargeCsQRoaQuality.py` | ROA quarterly EMA (profit/total_assets) | broad, profit>0 | H3 |
| `VnLargeCsQRoeQuality.py` | ROE quarterly EMA (profit/owners_equity) | broad, profit>0 | H3 |

## Decision rule (cam kết trước kết quả)
- **KEEP** nếu Gate 1–3 PASS (Sharpe dương ≥4/5 năm, 2022≥0, 2024≥0) — qua `fetch_yearly_tables.py`.
- **H1 CONFIRM** nếu Sharpe test của `QFinancialNetPayout` > 0.518 (annual version) AND Gate PASS.
- **H2 CONFIRM** nếu QFinancial > QNetPayoutPersistence (cùng quarterly) về test Sharpe.
- **H3 CONFIRM** nếu ≥ 1 quality file Gate PASS.
- Không retune sau khi thấy test. File FAIL gate → bỏ.

## Lưu ý rủi ro
- LARGE cross-section mỏng → rank nhiễu cao; kỳ vọng Sharpe khiêm tốn hơn SMALL.
- Quarterly dividends spiky (VN trả 1–2 lần/năm) → EMA bắt buộc.
- Nếu toàn bộ batch FAIL gate → bằng chứng thêm rằng LARGE thực sự là môi trường cấu trúc yếu
  (không phải do thiếu effort), và quyết định nguồn lực chuyển hướng.

---

## OUTCOMES (2026-08-05) — 4/4 FAIL, giả thuyết bị bác sạch

| File | Train S | Test S | 2020 | 2021 | 2022 | 2023 | 2024 | Gate |
|------|--------:|-------:|-----:|-----:|-----:|-----:|-----:|:----:|
| QFinancialNetPayout | **−0.31** | −0.42 | 1.29 | −0.62 | −1.01 | −0.90 | −0.30 | FAIL |
| QNetPayoutPersistence | 0.31 | −0.15 | 2.50 | −1.74 | 0.52 | −1.01 | 0.57 | FAIL |
| QRoaQuality | 0.10 | −0.75 | 1.17 | −0.22 | −0.57 | −0.14 | −0.81 | FAIL |
| QRoeQuality | 0.03 | −0.04 | 0.40 | −0.88 | 0.67 | −1.87 | 1.26 | FAIL |

### Kết luận
- **H1 (quarterly > annual) BỊ BÁC sạch:** annual LARGE FinancialNetPayout test 0.518 vs quarterly −0.42. Không chỉ thua mà **âm cả trong train** (−0.31).
- **H2 (financial > broad):** cả 2 đều chết → bác.
- **H3 (quality quarterly qua Gate 1–3):** bác (ROA 1/5, ROE 3/5).
- **Bằng chứng quan trọng:** 3/4 file **âm Sharpe 2021 — năm bull mạnh nhất** nơi annual version kiếm tiền (SMALL RoaQuality 2021 = 2.19). Quarterly fundamental trên platform này sinh signal **nhiễu/anti-momentum**: dữ liệu quarterly khác semantic annual (spiky/sparse/point-in-time), không đơn thuần là "tần suất cao hơn".
- **Quarterly pivot = dead on arrival** trên platform (ít nhất LARGE). Đây là negative result có giá trị: không nên tốn thêm nguồn lực vào hướng quarterly cho fundamental cross-sectional.
- LARGE xác nhận là môi trường cấu trúc yếu nhất: sau 40 file annual + 4 file quarterly, **0 file qua Gate 1–3**.
