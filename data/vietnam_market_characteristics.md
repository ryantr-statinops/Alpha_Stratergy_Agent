# Vietnam Market Characteristics (Round 2) — Feature Selection Guide

> Tài liệu tham chiếu đặc thù thị trường cổ phiếu Việt Nam → chọn nhanh
> **features/fields** phù hợp khi thiết kế strategy Round 2 (equity fundamental,
> daily, 3 cap segments). Đọc trước khi code, cùng `syntax/data_syntax.md`,
> `syntax/feature_syntax.md`, `syntax/operations_syntax.md`.
>
> Bản v1 (VN30F1M futures intraday) đã chuyển sang `vietnam_market_characteristics_v1.md`.

---

## 1. Bức tranh chung thị trường cổ phiếu VN

| Đặc điểm | Mô tả | Hệ quả cho thiết kế Round 2 |
|----------|-------|------------------------------|
| **Retail chiếm 80-90%** | Nhà đầu tư cá nhân áp đảo, hay herding/FOMO | Fundamental mispricing tồn tại lâu hơn — rank-based (cross_sectional) và growth-momentum có edge |
| **Tin nội tại chi phối** | KQKD, tin doanh nghiệp, chính sách thay đổi đột ngột | Biến động ngay quanh ngày công bố báo cáo; gap risk cao |
| **Thanh khoản tập trung** | Chỉ cổ phiếu lớn (large/mid cap) có thanh khoản tốt | Small-cap: thận trọng volume filter, rủi ro thiếu tính khả thi khi đặt lệnh |
| **Dòng tiền luân chuyển nhanh** | Retail xoay vòng theo nhóm ngành theo tin tức | Trend nhiều nhịp ngắn; cần trend filter + điểm vào sau xác nhận |
| **Báo cáo tài chính** | BCTC quý công bố chậm sau kỳ (thường T+15→45 ngày) | **Bắt buộc point-in-time**: dùng report sau ngày publish, missing = `.notna()`, không backfill |
| **Cơ cấu nhà đầu tư theo cap** | Large: tổ chức/ngoại nhiều; Small: retail chiếm áp đảo | Large-cap hiệu quả định giá cao → ưu tiên chất lượng/cash flow; Small-cap → earnings surprise/growth |

---

## 2. Đặc thù theo 3 cap segment → chọn features

Bảng này là **core reference** cho quyết định "dùng field/feature nào cho alpha ở cap nào".

| Segment | Đặc thù | Features/Fields nên ưu tiên | Features tránh | Luận điểm mẫu |
|---------|---------|------------------------------|----------------|----------------|
| **VN-SMALL-CAP** | Coverage phân tích thấp, retail đuổi tin, fundamentals ít được định giá | EPS q/q growth (`fun_is_eps_basis_quarterly`), net profit growth, price momentum + volume xác nhận | Quality tĩnh (ROE cao không phải lý do nhỏ cap tăng) | Re-rating khi EPS cải thiện; cross-sectional rank theo EPS growth |
| **VN-MID-CAP** | Tăng trưởng chu kỳ, nhạy với ROE và đòn bẩy | ROE (`net_profit / owners_equity`), capital ratio (`equity/assets`), profit growth + trend | Giá trị tĩnh đơn thuần (cheap ≠ tăng) | Quality + trend trung hạn; rank theo ROE |
| **VN-LARGE-CAP** | Tổ chức/ngoại tham gia nhiều, định giá kỹ hơn | Operating cash flow (`fun_cf_net_cash_inflows_outflows_from_operating_activities_annual`), margin stability, value (`eps/close`) + momentum | Growth thuần (đã priced in) | Stable cash flow + hợp lý định giá; composite value+momentum |

**Nguyên tắc chung:**
- Mọi alpha đều bắt đầu từ price/volume (`pv_close`, `pv_volume`) làm nền — fundamentals thêm độc lập.
- Chọn field **đúng nhóm nghiệp vụ**: Income Statement → profitability/growth; Balance Sheet → capital strength/leverage; Cash Flow → earnings quality/cash conversion.
- Ưu tiên field **quarterly** để phản ánh nhịp biến động gần nhất; `_annual` chỉ dùng cho đại lượng ổn định (VD operating cash flow hàng năm).

---

## 3. Thư viện fields thực dụng (đã verify trong catalog)

> Danh sách đầy đủ: `syntax/data_syntax.md` (496 fields). Dưới đây là các field
> **đã verify tồn tại trong catalog** — ưu tiên dùng để tránh lỗi submit.

### 3.1. Price / Volume (cả 2 mode)

| time_series (bỏ `_panel`) | cross_sectional (`_panel`) |
|---|---|
| `pv_close`, `pv_volume` | `pv_close_panel`, `pv_volume_panel` |

### 3.2. Income Statement — Quarterly

| time_series | cross_sectional | Ý nghĩa |
|---|---|---|
| `fun_is_eps_basis_quarterly` | `fun_is_eps_basis_quarterly_panel` | EPS (tăng trưởng, value) |
| `fun_is_net_profit_loss_after_tax_quarterly` | `fun_is_net_profit_loss_after_tax_quarterly_panel` | Lợi nhuận sau thuế |

### 3.3. Balance Sheet — Quarterly

| time_series | cross_sectional | Ý nghĩa |
|---|---|---|
| `fun_bs_owners_equity_quarterly` | `fun_bs_owners_equity_quarterly_panel` | Vốn chủ sở hữu (ROE, leverage) |
| `fun_bs_total_assets_quarterly` | `fun_bs_total_assets_quarterly_panel` | Tổng tài sản (ROA, margin) |

### 3.4. Cash Flow — Annual

| time_series | cross_sectional | Ý nghĩa |
|---|---|---|
| `fun_cf_net_cash_inflows_outflows_from_operating_activities_annual` | `fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel` | Dòng tiền hoạt động (earnings quality) |

> ⚠️ **KHÔNG dùng** `fun_bs_shareholders_equity_*`, `fun_is_total_operating_income_*`
> — không có trong catalog (example v1 vẫn dùng nhưng Round 2 chỉ dùng field verified).

---

## 4. Features cross_sectional hữu dụng (đã verify)

| Feature | Syntax | Dùng khi |
|---|---|---|
| `safe_divide_panel` | `self.feat.safe_divide_panel(num, den)` | Mọi tỷ số (ROE, ROA, E/P) — an toàn chia 0/âm |
| `ema_panel` / `sma_panel` | `self.feat.ema_panel(close)` | Trend trong panel (không có timeperiod — dùng default) |
| `rolling_zscore_panel` | `self.feat.rolling_zscore_panel(series)` | Value/momentum theo rolling window |
| `delta_panel` | `self.feat.delta_panel(series)` | Thay đổi fundamentals (EPS growth rank) |
| `returns_panel` / `log_returns_panel` | `self.feat.returns_panel(series)` | Price return trong panel |

Cross-sectional operators: `rank_cs_panel`, `zscore_cs_panel`, `winsorize_cs_panel`,
`portfolio_weights_panel(signal, method='rank_demean_l1', mask=...)` — market-neutral,
net ≈ 0, gross = 1. `mask` dùng để loại symbol thiếu fundamentals:
`eligible = self.op.notna(net_profit) & (equity > 0)`.

---

## 5. Pipeline Round 2 (nhắc lại)

1. **Khai báo batch** (rule GUIDE.md): mỗi lần gen `n` alpha phải nêu alpha → cap → mode → level trước.
2. **Chọn fields theo segment** (§2 bảng trên) → viết code trực tiếp vào `output/stage_2/`.
3. **Mode contract**: time_series (long-only `[0,+1]`, field không suffix) / cross_sectional (market-neutral, field `_panel`).
4. **Point-in-time**: report chỉ dùng sau ngày publish; missing = `.notna()`; cấm global aggregation/backfill.
5. **Validate** `python tools/validate_framework.py` → **Submit** `python tools/submit_and_check.py --batch --universe <CAP>`.

---

## 6. Debug nhanh khi alpha không đạt

| Triệu chứng | Nguyên nhân thường gặp | Hướng xử lý |
|---|---|---|
| Sharpe < ngưỡng cap | Signal nhiễu / không có trend filter / threshold quá chặt | Thêm price trend filter (close > ema), nới threshold, kết hợp 2-3 feature |
| MaxDD quá sâu | Exit quá chậm / thiếu chất lượng lọc | Thêm exit khi trend break (ema), quality floor (ROE/margin) |
| Cross_sectional lỗi "bounds" | Trộn mode / dùng `set_positions` trong panel | Dùng `set_portfolio_positions` + `portfolio_weights_panel` |
| Lỗi field khi submit | Dùng field không có trong catalog | Chỉ dùng field verified (§3) hoặc tra `syntax/data_syntax.md` |
| Kết quả không ổn định theo thời gian | Phụ thuộc 1 feature, phạm point-in-time | Diversify feature, tôn trọng report date |

---

## 7. Tóm tắt chọn nhanh

```
Feature Selection Fast-path (Round 2):
  1. Xác định cap: SMALL → growth/earnings; MID → quality/ROE; LARGE → cashflow/value
  2. Chọn mode: "phân bổ vốn giữa các cp" → cross_sectional; "chỉ long 1 cp" → time_series
  3. Bắt đầu bằng price/volume + 1 fundamental theo segment
  4. Dùng safe_divide_panel cho tỷ số (cross_sectional) hoặc / với fillna (time_series)
  5. Thêm trend filter + mask notna; point-in-time nghiêm túc
```
