# ALPHA WORKFLOW ENGINE — Autonomous Generate & Improve Loop

> Status: **ACTIVE** (2026-08-08)
> Mode: `cross_sectional` (`*_panel`, `_cs_panel` ops, `set_portfolio_positions`, `set_portfolio_positions`)
> Universe trọng tâm: **VN-MID-CAP** (mở rộng: SMALL → LARGE)
> Docs liên quan: `MASTER_alpha_planning.md`, `PAIR_COVERAGE_PLAN.md`, `HYPOTHESIS_LIBRARY.md`

---

## 1. Mục tiêu

Workflow này hướng dẫn **agent tự động** vận hành vòng lặp: đọc evidence → đề xuất hypothesis → gen alpha → validate → submit → đo kết quả → **phân loại nguyên nhân → cải thiện → tái submit** → lưu alpha PASS vào `success_alpha/`. Mỗi bước đo được, không gen "mù".

**Nguyên tắc vàng:** một alpha được coi là **PASS** chỉ khi **cả 3 stage — Aggregate, Train, Test — pass riêng lẻ** theo `tools/common.py` (`is_pass()` bắt buộc cả 3) và threshold đúng universe (MID-CAP). Không tổng hợp chỉ dựa trên aggregate.

---

## 2. Bài học đã rút (post-mortem 34-alpha cross_sectional MID-CAP, 2026-08-08)

| # | Hiện tượng | Nguyên nhân đã xác minh | Phòng tránh |
|---|-----------|------------------------|-------------|
| 1 | **Test Sharpe luôn âm** dù train/aggregate dương | `method='demean_l1'` bắt buộc có **short leg**; VN short không hiệu quả + mid-cap illiquid → OOS thiếu hiệu quả | Không ghim vào market-neutral; ưu tiên signal **long-biased**; luôn kiểm tra Test dương trước khi nhận |
| 2 | **Universe trả về rỗng** (metrics toàn 0) | Field không có data trên cap đó (vd `fun_bs_payables_to_suppliers`, `fun_bs_short_term_loans` trên MID) | Chỉ dùng field **đã xác minh có data** trên cap đó (4 file đã bị, thay bằng `trade_accounts_payable`) |
| 3 | **Coverage chập** | Field lẻ dễ bị NaN, mask quá hẹp | `base_eligible` + mask đơn vị đúng cỡ; dùng `.notna` đúng nghĩa |
| 4 | **Tương quan cao → tremble** | Tạo nhiều alpha cùng 1 cơ chế | Rule 3 cặp — đổi cơ chế khi làm 2 alpha cho 1 cặp |

---

## 3. Vòng lặp đóng (THE LOOP) — 9 bước

```
┌───────────────────────────────┐
│ 1. CONTEXT — đọc evidence     │
└──────────────┬────────────────┘
               ▼
┌───────────────────────────────┐
│ 2. HYPOTHESIS — chọn cặp     │
└──────────────┬────────────────┘
               ▼
┌───────────────────────────────┐
│ 3. BUILD — theo template      │
└──────────────┬────────────────┘
               ▼
┌───────────────────────────────┐
│ 4. VALIDATE — --strict        │
└──────────────┬────────────────┘
               ▼
┌───────────────────────────────┐
│ 5. SUBMIT — dry-run → live    │
└──────────────┬────────────────┘
               ▼
┌───────────────────────────────┐
│ 6. MEASURE — results_stage_2  │
└──────────────┬────────────────┘
               ▼
     ┌─────────┴─────────┐
     │ 7. PASS? (3-stage) │
     └─────────┬─────────┘
          NO   │   YES
        ┌──────┴──────┐
        │ 8. TRIAGE   │   9. ARCHIVE → success_alpha/
        │ sửa/loop    │        + HYPOTHESIS update
        └─────────────┘
```

---

## 4. Bước 1 — CONTEXT (luôn chạy trước khi gen)

```bash
# Xem PASS/FAIL hiện tại theo cap
python tools/check_results.py --universe VN-MID-CAP --splits

# Xem trạng thái pair coverage
# → đọc idea/planning_alpha/_framework/PAIR_COVERAGE_PLAN.md
# → đọc idea/planning_alpha/_framework/HYPOTHESIS_LIBRARY.md
# → đọc success_alpha/*.py (mẫu PASS — nguồn evidence tốt nhất)
```

Yêu cầu **bắt buộc**: trước khi gen, ghi chú rõ "field verified?" trong viết. Rule: field chưa được dùng thành công ở cap đó → đánh dấu RISKY (kiểm tra `syntax/data_syntax.md` + grep alpha cùng cap).

---

## 5. Bước 2 — Hypothesis

- Chọn 1 **cặp** chưa cover hoặc 1 cơ cho **mới** (khác engine alpha đã có — theo `PAIR_COVERAGE_PLAN rule 6`).
- Viết vào `HYPOTHESIS_LIBRARY.md`: id, hypothesis, cặp, factor, cơ chế kinh tế.
- Mỗi hypothesis trả lời: "điều kiện X tạo ra hiệu gì trên giá Y?"

---

## 3. Bước 3 — BUILD (template chuẩn cross_sectional)

> Tuân thủ template mẫu: `output/stage_2/vn_mid_cap/cross_sectional/VnMidCsAssetDebtBearing.py`
> (pattern: gate → liquidity_rank → factor_rank → trend_rank → `demean_l1`).

```python
"""
name:    VnMidCs<Thesis>            # tên F-start + PascalCase
summary: <1 câu> Buy mid caps when <factor> holds, trend-filtered.
idea:    <pair hoặc thesis kinh tế>, <cơ chế → signal>
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # ---- Layer 0: data._panel (field verified cho cap này) ----
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        # factor field(s) ...

        # ---- Layer 1: primitive ----
        ratio = self.feat.safe_divide_panel(nom, denom)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))

        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = ((in_universe == True) & (close > 0) & (volume > 0)
                         & (total_assets > 0) & (equity > 0)
                         & (capital_strength > 0.15) & <denominator >= 0/ > 0>)
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        factor_rank = self.op.rank_cs_panel(-factor, mask=eligible)
        trend_rank  = self.op.rank_cs_panel(trend, mask=eligible)
        signal = factor_rank + trend_rank

        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
```

### Rules cứng

1. **cross_sectional**: field `_panel`, ops `_cs_panel`, position `set_portfolio_positions`.
2. **Field verified**: chỉ dùng field có trong `syntax/data_syntax.md` + đã dùng thành công trên cap (grep old alpha).
3. **Sign convention CF**: dividends ≤ 0, repurchase ≤ 0, issuance > 0, capex ≤ 0 → dùng `0 - capex` khi cần dương.
4. **Denominator guard**: `safe_divide_panel` + mask denom > 0.
5. **Point-in-time**: missing = unavailable (`.notna`), không backfill.
6. **Không dùng `.abs()`** trên panel (không hỗ trợ) → dùng `ratio * ratio` hoặc `max(f, -f)` khi cần magnitude.
7. **Một vòng rank cuối**: không pre-winsorize/rank trước `demean`.
8. Class `CustomStrategy(SimpleAlgorithm)`, `__algorithm__`. Không `import pandas`, không `SeriesT`, không tên biến trùng keyword.

### Checklist trước VALIDATE

- [ ] Docstring có `name/summary/idea` giải thích cơ chế rõ.
- [ ] Mỗi ratio `.safe_divide_panel` có mask denom.
- [ ] Field name trùng chính xác `data_syntax.md`.
- [ ] Không `.abs()`, không `**`.
- [ ] `method=` phải ∈ {`'demean_l1'`, `'rank_demean_l1'`}.

---

## 7. Bước 4 — VALIDATE

```bash
python tools/validate_framework.py --strict
```
- **Bắt buộc**: `No errors` (warnings = chưa đăng ký index → chấp nhận).
- Có error → sửa trước, không submit.

---

## 8. Bước 5 — SUBMIT

```bash
# Dry-run trước
python tools/submit_and_check.py --files output/stage_2/vn_mid_cap/cross_sectional/<Name>.py \
           --universe VN-MID-CAP --parallel --workers 10 --force --dry-run

# Live (nộp theo batch nhỏ)
python tools/submit_and_check.py --files output/stage_2/vn_mid_cap/cross_sectional/<Name>.py \
           --universe VN-MID-CAP --parallel --workers 10 --force --yes
```
> Nộp từng đợt nhỏ (1–5 file) để review metric từng file — không nộp 30 file cùng lúc.

---

## 9. Bước 6-7 — MEASURE & PASS

- Sau submit metrics xuất hiện ở `backtest/results_stage_2.csv` (đầy đủ `train_`/`test_`).
- **PASS = cả 3 stage riêng lẻ** (chính là `tools/common.py::is_pass`):

| Stage | MID-CAP threshold |
|---|---|
| Aggregate | Sharpe ≥ 1.10, CAGR ≥ 20%, MaxDD ≥ -40%, PF ≥ 1.25, Calmar ≥ 1.00 |
| Train (70%) | cùng ngưỡng trên |
| Test (30%) | cùng ngưỡng trên — **bắt buộc** |

**Bổ sung discriminator mạnh (khuyến nghị trước khi coi PASS):**
- Sharpe **2022 (crash) ≥ 0** và **2024 ≥ 0** (dùng `fetch_yearly_tables.py` nếu có).
- Test Sharpe dương **rõ ràng** (cách 0 xa; gần 0 = rủi ro sinh lời thấp).

---

## 10. Bước 8 — TRIAGE & IMPROVE (khi FAIL)

| Triệu chứng (từ CSV) | Điều trị |
|-----------------------|----------|
| Agg/Train dương, Test âm | **Overfit trend**: signal bắt overfitting xu hướng — thêm **flat gate** `close < ema_slow → weights=0` (long 0), hoặc giảm weight trend. |
| 3 stage đều 0 / rõ ràng rỗng | Universe empty: field không data trên cap → **đổi cặp/field** (vd payables→trade_accounts_payable). Resubmit. |
| Test âm nhẹ (> -0.5) | Cải chính: đổi window rank / thêm persistent sman (loại bật noise). |
| 2022/2024 Sharpe âm | Cần mask khi market crash → thêm flat/trend gate. |
| Correlation với alpha có > 0.6 | Cơ chế trùng — đổi factor hoặc mechanism (đừng "buff" lại). |

**Quy tắc vòng sửa:** tối đa **2–3 lần thử** cho 1 hypothesis trước khi loại (tránh overfit bằng sửa bừa). Mỗi lần sửa: ghi note `(v2: ...)` trong docstring hoặc tạo file `<Name>V2.py` (không đè file gốc — giữ trace). Sau 3 lần vẫn Test âm → **RAW FAIL** — bỏ, chuyển mechanic/cặp khác.

---

## 11. Bước 9 — ARCHIVE (PASS)

Khi `is_pass(...) == True` (aggregate + train + test riêng lẻ):
1. **Copy file → `success_alpha/`** (thư viện PASS reference).
2. Cập nhật `HYPOTHESIS_LIBRARY.md`: chuyển dòng sang **PASS evidence** (ghép metric trích xuất).
3. Cập nhật `output/index.csv` cột status (nếu có).
4. Có thể đề xuất commit (agent không tự commit).

---

## 12. Quyết định theo hướng gen

| Hướng | Điều kiện | Cách |
|---|---|---|
| Phủ pair mới | Pair trong `PAIR_COVERAGE_PLAN` còn trống | 1 alpha/cặp theo mẫu |
| Improve FAIL | Alpha có, Test âm < -0.5 | Sửa 1 nuance → `<Name>V2.py` → resubmit |
| Retry / thay thẻ | Test âm nặng (< -1) hoặc universe rỗng | Đổi cặp/field, không sửa |
| Archive | is_pass True | Copy → success/ + hypothesis update |

---

## 13. Tài liệu bắt buộc đọc trước khi BUILD

- `idea/planning_alpha/_framework/PAIR_COVERAGE_PLAN.md` — 28 cặp, batching
- `idea/planning_alpha/_framework/MASTER_alpha_planning.md` — 7-layer, factor recipes
- `idea/planning_alpha/_framework/HYPOTHESIS_LIBRARY.md` — evidence + universe status
- `success_alpha/*.py` — template/hạt nhân PASS (đọc trước khi viết)
- `syntax/INDEX.md` + `syntax/cross_sectional/*` — ops/feature hợp lệ
- `tools/validate_framework.py`, `tools/submit_and_check.py`, `tools/check_results.py` — pipeline

---

## 14. KPIs

| Metric | Cách đo | Action khi thấp |
|---|---|---|
| PASS rate | pass / submitted | < 10% → giảm expectation, tăng gate |
| Test Sharpe | median của PASS | Không dương → loại |
| Retention | pass-train → pass-test | < 10% → thêm trend/flat gate |
| Pair coverage | covered / tổng | Chưa đủ → expand |

---

*Agent tự đọc file này một lần trước mỗi BUILD/BATCH hoạt động mới.*