# Framework Build Guide — Round 2 (Fundamental Alpha Arena)

> **Mục tiêu:** Hướng dẫn **build framework chuẩn** để **sinh ra các strategy từ dễ đến khó**
> theo yêu cầu, đúng paradigm Round 2 (daily equity, fundamentals point-in-time, 2 mode).
> File này là **plan + blueprint** cho pipeline gen strategy — không phải tài liệu tra cứu field.

---

## 1. Vì sao cần file này?

Các file `input/templates/*.md` và `syntax/*.md` hiện tại chỉ là **nguyên liệu tham khảo**
(catalog data/feature/op/parameters). Chưa có một **quy trình chuẩn** để:

1. Chọn luận điểm (thesis) → chọn mode → chọn field → viết strategy.
2. Sinh file `.py` có độ khó tăng dần (dễ trước, khó sau) mà vẫn pass validation.
3. Tự chọn đúng mode (nền tảng XNOQuant có cơ chế tự chọn mode, nhưng ta vẫn gen rõ cả 2).

File này định nghĩa **cấu trúc framework sinh strategy** đó.

---

## 2. Kiến trúc Framework Gen Strategy

```text
┌───────────────────────────────────────────────────────────────┐
│ L0. Yêu cầu (user / thesis)                                   │
│     "gen 5 strategy trend + fundamental cho VN-LARGE-CAP"     │
└──────────────────────────┬────────────────────────────────────┘
                           ▼
┌───────────────────────────────────────────────────────────────┐
│ L1. Thesis Selector                                           │
│     → chọn thesis group (momentum/trend/quality/... )         │
└──────────────────────────┬────────────────────────────────────┘
                           ▼
┌───────────────────────────────────────────────────────────────┐
│ L2. Mode + Data Selector                                      │
│     → time_series (không suffix)  HOẶC cross_sectional (_panel)│
│     → chọn field từ syntax/data_syntax.md                     │
└──────────────────────────┬────────────────────────────────────┘
                           ▼
┌───────────────────────────────────────────────────────────────┐
│ L3. Level Selector (độ khó 1→5)                               │
│     → chọn template theo level + parameters theo syntax/       │
│       parameters.md (daily, ratio 1:3)                        │
└──────────────────────────┬────────────────────────────────────┘
                           ▼
┌───────────────────────────────────────────────────────────────┐
│ L4. Code Renderer                                            │
│     → render .py theo template + compliance checklist          │
│       (strategy_framework.md)                                 │
└──────────────────────────┬────────────────────────────────────┘
                           ▼
┌───────────────────────────────────────────────────────────────┐
│ L5. Validator + Submit                                        │
│     → validate_framework.py + submit_and_check.py             │
└───────────────────────────────────────────────────────────────┘
```

---

## 3. Chọn Thesis (Luận Điểm)

Mỗi strategy cần **1 luận điểm kinh tế thực sự** (metadata docstring), không mô tả lại code.

### 3.1 Thesis Groups Round 2 (daily equity + fundamentals)

| # | Thesis Group | Data cốt lõi | Chỉ báo / thao tác | Level đề xuất |
|:-:|--------------|--------------|--------------------|:----:|
| 01 | Earnings Momentum | `fun_is_net_profit_loss_after_tax_*`, `pv_close` | `pct_change` step + `ema` trend | 1-2 |
| 02 | Trend + Fundamental Confirm | `pv_close`, `pv_volume`, `fun_is_*` | `ema` 1:3 + volume + profit step | 1-3 |
| 03 | Quality / Profitability | `fun_is_*`, `fun_bs_*` | ratio (ROE, margin) + `.notna()` | 2-4 |
| 04 | Leverage / Balance-Sheet | `fun_bs_total_assets`, `fun_bs_owners_equity` | equity/assets, leverage spread | 2-4 |
| 05 | Cash-Flow Quality | `fun_cf_*`, `fun_is_*` | CFO positive, cash conversion | 3-5 |
| 06 | Value (cross-sectional) | `fun_is_eps_basis_*`, `pv_close_*_panel` | `rank_cs_panel`, `portfolio_weights_panel` | 4-5 |
| 07 | Sector-Specific (bank/ins/sec) | `fun_is_*_insurance`, `fun_is_*_commission` | premium/commission growth | 3-5 |
| 08 | Multi-Factor Composite | nhiều field | z-score + tổng hợp | 5 |

> Nguyên tắc: bắt đầu thesis đơn giản (1 nhóm data), tăng dần độ phức tạp.

---

## 4. Chọn Mode + Data

### 4.1 Mode Contract (bắt buộc)

| Mode | Suffix | Position API | Bounds | Dùng khi |
|------|--------|--------------|-------|----------|
| `time_series` | không | `self.set_positions(cond, pos)` | `[0, +1]` | "khi nào nên giữ cổ phiếu này" |
| `cross_sectional` | `_panel` | `self.set_portfolio_positions(weights)` | market-neutral | "phân bổ vốn thế nào giữa các cp" |

**Không trộn 2 mode trong 1 strategy.**

### 4.2 Quy tắc chọn field

- `time_series`: `self.data.pv_close`, `self.data.fun_is_net_profit_loss_after_tax_quarterly` (không `_panel`).
- `cross_sectional`: `self.data.pv_close_panel`, `self.data.fun_is_net_profit_loss_after_tax_quarterly_panel` (có `_panel`).
- Field phải nằm trong 496 fields (`syntax/data_syntax.md`).
- Fundamenta dùng `_quarterly` (báo cáo quý) cho các tín hiệu tăng trưởng; `_annual` cho bộ lọc chất lượng dài hạn.

### 4.3 Universes

Chỉ dùng: `VN-SMALL-CAP`, `VN-MID-CAP`, `VN-LARGE-CAP`.

---

## 5. Level Selector (Độ Khó 1 → 5)

Framework sinh strategy **từ dễ đến khó**. Mỗi level tăng thêm 1 lớp phức tạp nhưng vẫn pass.

| Level | Tên | Mode | Số condition | Vị thế | Ví dụ reference |
|:-----:|-----|------|:---:|--------|-----------------|
| **1** | Single-Signal | time_series | 2-3 | 0 / 1 | `VnBankPriceVolumeTrend` |
| **2** | Trend + Fundamental | time_series | 3-4 | 0 / 1 | `VnTop30SimpleFundamentalTrend`, `VnInsurancePremiumMomentum` |
| **3** | Tiered Sizing | time_series | 3-6 | 0 / 0.5 / 1 | `VnSecuritiesCommissionMomentum`, `VnTop30QualityBreakout` |
| **4** | Cross-Sectional Rank | cross_sectional | 3-4 + rank | market-neutral | *(chưa có sample — dựng mới)* |
| **5** | Multi-Factor Panel | cross_sectional | composite | `portfolio_weights_panel` | *(chưa có sample — dựng mới)* |

### 5.1 Mô tả từng Level

**Level 1 — Single-Signal:** giá + volume. 1 xu hướng (ema/sma), 1 bộ lọc khối lượng. `position=1` khi đủ điều kiện, `0` khi thoát.

**Level 2 — Trend + Fundamental:** thêm fundamentals làm bộ lọc chất lượng. Dùng `pct_change(periods=1)` + `fillna(0)` để đo step-change khi report mới.

**Level 3 — Tiered Sizing:** tách weak/strong long. `0.5` trước, `1` khi xác nhận mạnh hơn. Thường có volume/quality confirmation riêng.

**Level 4 — Cross-Sectional Rank:** dùng `_panel` fields + `rank_cs_panel`/`zscore_cs_panel`, `portfolio_weights_panel(signal, method='rank_demean_l1')`.

**Level 5 — Multi-Factor Panel:** composite signal từ nhiều nhóm (quality + value + momentum), rank và kết hợp → portfolio weights.

---

## 6. Parameters (Daily, Ratio 1:3)

> Chi tiết tại `syntax/time_series/parameters.md`. Round 2 là **daily** — 1 ngày = 1 bar.

| Feature | Tham số chuẩn | Ghi chú |
|---------|---------------|---------|
| `ema` fast | 8-12 | ~1.5-2.5 tuần |
| `ema` slow | 24-36 | 1:3 với fast |
| `sma` volume | 10 / 20 | active / stable |
| `rsi` | 7 / 9 | active / balanced |
| `atr` | 14 | chuẩn |
| `macd` | 8/21/5 | theo sample |
| fundamental step | `pct_change(x, periods=1)` + `fillna(0)` | |

> **Lưu ý:** bộ tham số này là **ước lượng từ sample** — khi platform xác nhận sample pass,
> cần đối chiếu lại (cơ chế xác minh sẽ được bổ sung sau).

---

## 7. Code Renderer — Template chuẩn

### 7.1 Template time_series (Level 1-3)

```python
"""
name:    <TênStrategy>
summary: <một câu mô tả ngắn>
idea:    <luận điểm kinh tế, KHÔNG mô tả lại code>
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # STEP 1 — Raw data
        close = self.data.pv_close
        volume = self.data.pv_volume
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly

        # STEP 2 — Features (daily params, ratio 1:3)
        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)
        volume_base = self.feat.sma(volume, timeperiod=10)

        # STEP 3 — Trading logic (fundamentals step on report updates)
        profit_growth = self.op.fillna(self.op.pct_change(net_profit, periods=1), value=0)

        long_setup = (close > ema_slow) & (ema_fast > ema_slow) & (profit_growth > -0.05)
        exit_setup = (ema_fast < ema_slow) | (profit_growth < -0.15)

        # STEP 4 — Position (exit first, then long)
        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
```

### 7.2 Template cross_sectional (Level 4-5)

```python
"""
name:    <TênStrategy>
summary: <mô tả ngắn>
idea:    <luận điểm: phân bổ vốn theo rank>
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # STEP 1 — Panel data (có _panel suffix)
        close = self.data.pv_close_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel

        # STEP 2 — Features panel
        roa = self.feat.safe_divide_panel(net_profit, total_assets)
        ema_fast = self.feat.ema_panel(close)

        # STEP 3 — Signal + mask (loại missing fundamentals)
        eligible = self.op.notna(net_profit) & (total_assets > 0)
        signal = roa

        # STEP 4 — Portfolio weights (market-neutral)
        weights = self.op.portfolio_weights_panel(signal, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
```

---

## 8. Validator + Submit

Sau khi viết code theo template ở §7, chạy:

```bash
python tools/validate_framework.py      # check compliance (mode contract, point-in-time, bounds)
python tools/submit_and_check.py        # submit + verify trên nền tảng
```

Checklist bắt buộc (đầy đủ tại `template_example/strategy_framework.md` §9):

- [ ] Chỉ 1 mode — không trộn series/panel
- [ ] Field đúng suffix theo mode
- [ ] Universe hợp lệ (VN-SMALL/MID/LARGE-CAP)
- [ ] Fundamentals chỉ sau ngày công bố; missing = `.notna()`, không zero
- [ ] Ratio: denominator dương; `safe_divide_panel` nếu cross_sectional
- [ ] Không loops/lambdas/imports/global aggregations
- [ ] Không future observation / backfill / negative shift
- [ ] Bounds đúng mode: time_series `[0,+1]`, cross_sectional market-neutral
- [ ] Metadata docstring = luận điểm kinh tế

---

## 9. Roadmap Build (theo thứ tự ưu tiên)

> **Ghi chú quan trọng:** Code strategy do **AI agent viết trực tiếp** theo file guide này — KHÔNG có tool sinh code (không dựng lại `generate_strategies.py` kiểu vòng 1). Tool duy nhất cần dựng/cập nhật là validator.

| # | Việc | Output | Trạng thái |
|:-:|------|--------|-----------|
| 1 | Archive vòng 1 → `output/stage_1/` | cấu trúc thư mục | ✅ DONE |
| 2 | Viết lại syntax docs (data/feature/op/params) | `syntax/*.md` | ✅ DONE |
| 3 | Viết lại strategy_framework.md | master spec Round 2 | ✅ DONE |
| 4 | **File guide này** | blueprint build framework | ✅ DONE |
| 5 | Cập nhật `tools/validate_framework.py` V2 | validator mode contract | ⏳ NEXT |
| 6 | Agent viết trực tiếp strategy Level 1-5 | `output/stage_2/` + `index.csv` | ⏳ |
| 7 | Submit + verify, điều chỉnh params | sample pass | ⏳ |

> Quy trình vận hành (không qua generator): viết code → `validate_framework.py` V2 → `submit_and_check.py` → `check_results.py`.

---

## 10. Nguyên tắc khi gen

1. **Dễ trước, khó sau** — Level 1 pass trước, rồi tăng dần.
2. **Thesis rõ ràng** — mỗi strategy 1 luận điểm; không copy-paste cùng điều kiện cho nhiều thesis.
3. **Tránh turnover cao** — fees bị phạt nặng; tiered sizing giảm rebalance.
4. **Point-in-time tuyệt đối** — fundamentals chỉ dùng sau ngày công bố.
5. **Không dựa vào may rủi** — ổn định across in-sample/out-of-sample mới pass.
6. **Nền tảng tự chọn mode** nhưng ta **gen rõ cả 2 mode** trong pipeline.
