# AI Agent Onboarding Guide — Alpha Bot

> **Đọc file này đầu tiên khi bắt đầu phiên làm việc mới.**
> File map toàn bộ knowledge base — đọc đúng thứ tự để build context nhanh nhất.

---

## Round 2 (ACTIVE) — Fundamental Alpha Arena

> **Round 2 là ưu tiên hiện tại:** daily equity research (thay vì intraday futures vòng 1).
> Vòng 1 đã archive tại `output/stage_1/`.

### Reading Order — Round 2

| # | File | Purpose | Đọc khi nào |
|:-:|------|---------|-------------|
| 1 | `agent/stage_2_guideline.md` | **Rules chính thức Round 2** (universes, modes, point-in-time, scoring) | **Đầu phiên** |
| 2 | `agent/framework_build_guide.md` | **Blueprint build framework + gen strategy dễ→khó (Level 1-5, cả 2 mode)** | **Trước khi gen code** |
| 3 | `template_example/strategy_framework.md` | **Master spec Round 2** — mode contract, templates, compliance checklist | **Trước khi code** |
| 4 | `idea/planning_alpha/_framework/MASTER_alpha_planning.md` | **Master planning** — 4-layer construction (data → feat → mask → op → position), data groups, mask layers | **Khi bắt đầu plan alpha** |
| 5 | `syntax/data_syntax.md` | 496 fields (PV/IS/BS/CF) + mode contract | **Khi chọn data** |
| 6 | `syntax/time_series/feature_syntax.md`, `syntax/cross_sectional/feature_syntax.md` | 36 panel features + time_series family | **Khi cần indicator** |
| 7 | `syntax/time_series/operations_syntax.md`, `syntax/cross_sectional/operations_syntax.md` | 7 cross-sectional ops + time_series ops | **Khi cần operator** |
| 8 | `syntax/time_series/parameters.md`, `syntax/cross_sectional/parameters.md` | Parameter chuẩn daily (ratio 1:3) | **Khi cần param** |
| 9 | `template_example/VN-*/` | 14 examples Round 2 (BANK/INSURANCE/SECURITIES/TOP30) | **Khi tham khảo mẫu** |
| 10 | `agent/migration_plan_v2.md` | Kế hoạch migration V1→V2 (Phase A done, B done, C pending) | **Khi cần bối cảnh** |
| 11 | `idea/planning_alpha/stage_2/` | **Idea Round 2** — mỗi alpha ghi 1 file markdown trước khi gen | **Khi bắt đầu gen alpha** |
| 12 | `agent/system_health_check.md` | **Health check Stage 2** — offline + API read-only + live opt-in | **Khi kiểm tra trạng thái hệ thống** |

---

## Reading Order — Vòng 1 (ARCHIVED)

| # | File | Purpose | Đọc khi nào |
|:-:|------|---------|-------------|
| 1 | `README.md` | Tổng quan project, 5-step workflow, project structure | **Đầu phiên** |
| 3 | `template_example/(Old)vnfuture/strategy_framework.md` | Master spec vòng 1 (intraday futures) | **Chỉ khi làm việc với vòng 1** |
| 4 | `data/vietnam_market_characteristics_v1.md` | Đặc thù thị trường VN futures vòng 1 → thiết kế strategy | **Trước khi code (vòng 1)** |
| 5 | `idea/hypothesis/hypothesis_framework.md` | Acceptance criteria: 10-metric weighted scorecard | **Khi review hypothesis** |
| 6 | `syntax/INDEX.md` | Cửa vào cho toàn bộ syntax docs | **Khi bắt đầu code** |
| 7 | `idea/planning_alpha/stage_1/enhancement_return_roll_tiered_session.md` | 3 enhancements (return_roll, tiered sizing, session gating) | **Khi cần hiểu code vòng 1** |
| 8 | `idea/planning_alpha/stage_1/alpha_generation_rolling_mean_quantile.md` | ~890 alpha variants | **Khi cần thêm ý tưởng** |
| 9 | `idea/planning_alpha/stage_1/backtest_plan.md` | Kế hoạch backtest vòng 1 | **Khi bắt đầu backtest** |
| 10 | `idea/planning_alpha/stage_1/scaling_proposal_500_10000_strategies.md` | Kế hoạch mở rộng lên 10000 strategies | **Khi planning scale** |

---

## Quick Reference

### Stack (Round 2 — ACTIVE)
- Platform: **XNOQuant** (`https://alpha.xnoquant.io/build`)
- Class: `CustomStrategy(SimpleAlgorithm)`
- Method: `__algorithm__(self)`
- API: `self.data.*`, `self.feat.*`, `self.op.*`
- **2 mode:** `time_series` (không suffix, `set_positions`, long-only `[0,+1]`) |
  `cross_sectional` (`_panel` suffix, `set_portfolio_positions`, market-neutral)
- **Universes:** VN-SMALL-CAP / VN-MID-CAP / VN-LARGE-CAP (daily)
- No pandas/numpy, no loops/lambdas, no global aggregations, point-in-time fundamentals
- Chọn feature theo cap: `data/vietnam_market_characteristics.md` (SMALL→growth/earnings, MID→quality/ROE, LARGE→cashflow/value)

### Position Order (time_series)
```python
self.set_positions(exit_setup, position=0)    # Exit first
self.set_positions(weak_long, position=0.5)   # Half size second
self.set_positions(strong_long, position=1)   # Full size last (override)
```

### Stack (Vòng 1 — ARCHIVED)
- Platform: **XNOQuant** (`https://alpha.xnoquant.io/build`)
- Class: `CustomStrategy(SimpleAlgorithm)`
- Method: `__algorithm__(self)` (not `__logic__`)
- API: `self.data.*`, `self.feat.*`, `self.op.*`, `self.set_positions()`
- No pandas, numpy, SeriesT, `open` variable

### Position Order (Vòng 1)
```python
self.set_positions(exit_setup, position=0)    # Exit first
self.set_positions(long_setup, position=1)     # Long second
self.set_positions(short_setup, position=-1)   # Short third
```

### Thesis Groups (Vòng 1 — ARCHIVED, 35 groups)
Xem danh sách đầy đủ tại `output/` — các thư mục `thesis_NN_name/`.
Các nhóm chính:
| # | Thesis | Timeframes | Key Data |
|:-:|--------|:----------:|----------|
| 01 | Momentum | 5, 15, 30, 60 | `pv_close`, `pv_volume`, `pv_vn30_close` |
| 02 | Trend | 5, 15, 30, 60 | `pv_close`, `pv_high`, `pv_low` |
| 03 | Mean Reversion | 5, 15, 30, 60 | `pv_close` |
| 04 | Breakout | 5, 15, 30, 60 | `pv_close`, `pv_volume`, `pv_high`, `pv_low` |
| 05 | Cross-Market | 15, 30, 60 | `pv_close`, `pv_vn30_*`, `pv_dji_*` |
| 06 | Volume & Flow | 15, 30, 60 | `pv_close`, `fut_*` |
| 07 | Intraday Session | 5, 15 | `pv_open`, `pv_close`, `pv_high`, `pv_low` |
| 08 | Multi-Factor | 15, 30, 60 | All of the above |
| ... | thesis_09 → thesis_38 | (xem trong output/) | — |
Ngoài ra còn: `single_feat_alpha/` (47 files) và `multi_feat_alpha/` (9 files).

### Multi-Timeframe Window Sizing (Vòng 1 — 15min futures, ARCHIVED)
| Timeframe | Fast | Mid | Slow | RSI | ADX | Vol | ReturnRoll | ReturnThresh | SessionCandles |
|:---------:|:----:|:---:|:----:|:---:|:---:|:---:|:----------:|:-------------:|:--------------:|
| 5min | 8 | 14 | 20 | 7 | 7 | 14 | 3 | 0.0001 | 72 |
| 15min | 13 | 26 | 34 | 10 | 10 | 20 | 5 | 0.0002 | 24 |
| 30min | 20 | 40 | 50 | 14 | 14 | 26 | 8 | 0.0003 | 12 |
| 60min | 30 | 60 | 100 | 21 | 21 | 34 | 14 | 0.0005 | 6 |

### Parameter Daily (Round 2 — ACTIVE, xem `syntax/time_series/parameters.md`)
| Feature | Fast | Slow | Ratio | Ghi chú |
|---------|:----:|:----:|:-----:|---------|
| ema | 8-12 | 24-36 | 1:3 | ~1.5 tuần / ~1.5 tháng |
| sma (volume) | 10 | 20 | — | active / stable |
| rsi | 7 | 9 | — | active / balanced |
| atr | 14 | — | — | chuẩn |
| macd | 8 | 21 / signal 5 | — | theo sample |
| fundamental | `pct_change(x, periods=1)` + `fillna(0)` | — | — | step-change khi report mới |

### Acceptance Criteria (Vòng 1 — ARCHIVED, 10-metric weighted)
> Round 2 dùng pass criteria **theo universe** tại `tools/common.py` (`PASS_THRESHOLDS_BY_UNIVERSE`) + `tools/check_results.py`.
| Metric | Weight | Target | Must-pass |
|--------|:------:|--------|:---------:|
| Sharpe Ratio | High | ≥ 2.0 (user) / ≥ 1.2 (competition) | ✅ |
| CAGR | High | ≥ 20% | ✅ |
| Max Drawdown | High | ≥ -20% | ✅ |
| Sortino Ratio | Medium | ≥ 1.5 | |
| Calmar Ratio | Medium | ≥ 1.1 | |
| Profit Factor | Medium | ≥ 1.3 | |
| VaR (95%) | Medium | ≥ -5% | |
| CVaR (95%) | Low | ≥ -6% | |
| Ulcer Index | Low | ≤ 12 | |
| Cost | Low | ≤ 1% | |
| Correlation | Low | ≤ 0.8 | |

PASS: ≥ 8.0/13pts with Sharpe, CAGR, Max DD must-pass.

### Công thức Sharpe ≥ 2.0 (Vòng 1 — ARCHIVED, futures intraday)
```
Sharpe ≥ 2.0 =
  (ADX > 22)                        # Filter noise
  + (return_roll > 0)               # Confirm momentum
  + (volume > SMA)                  # Volume confirmation
  + (ROC > 0.3%)                    # Avoid whipsaw
  + Asymmetric exit (return_roll < 0) # Cut loss fast
  + Session gating (close lunch, pre-ATC) # Avoid manipulation
  + Consecutive loss protection (3 max) # Preserve capital
```

---

## Round 2 — Pipeline Gen & Submit

Quy trình vận hành Round 2 (không có tool sinh code — agent viết trực tiếp):

```bash
# 0. IDEA → GHI FILE → DUYỆT → GEN (bắt buộc, xem Workflow Alpha Round 2 bên dưới)
#    Mỗi alpha phải có file markdown trong idea/planning_alpha/stage_2/ trước khi gen code.

# 1. VIẾT STRATEGY theo blueprint → tạo file output/stage_2/ + ghi index.csv
#    (theo agent/framework_build_guide.md, Level 1-5, 1 trong 2 mode)

# 2. VALIDATE compliance (mode contract, point-in-time, bounds) — strict bắt cả warning
python tools/validate_framework.py --strict

# 3. SUBMIT lên XNOQuant (cần .env: XNO_EDITOR_ID + XNO_TOKEN; universe chọn THỦ CÔNG trên UI)
#    Universe trong CSV luôn suy từ path output/stage_2/<cap>/... (KHÔNG ghi đè bằng flag).
#    --universe chỉ là FILTER chọn 1 cap (single editor => không submit nhiều cap cùng lúc).
#    --dry-run xem trước editor/universe/files — không gọi API.
python tools/submit_and_check.py --batch --dry-run --universe VN-SMALL-CAP   # xem trước (an toàn)
python tools/submit_and_check.py --batch --test --universe VN-SMALL-CAP      # live 1 file đầu (chọn đúng universe trên UI trước)
python tools/submit_and_check.py --batch --universe VN-SMALL-CAP             # submit cả cap

# 4. REVIEW kết quả (backtest/results_stage_2.csv, PASS theo universe)
python tools/check_results.py --detail --universe VN-SMALL-CAP

# 5. COMMIT + PUSH
```

### Workflow Alpha Round 2 (IDEA → FILE → DUYỆT → GEN)

1. **IDEA:** nghĩ ra alpha + lý do chọn cap (`VN-SMALL-CAP` / `VN-MID-CAP` / `VN-LARGE-CAP`).
2. **GHI FILE** (bắt buộc, trước khi gen): tạo file `.md` tại `idea/planning_alpha/stage_2/`
   — format: `concept → thesis → universe → mode → level → fields → logic → risk`.
3. **DUYỆT:** user review file idea; chỉ gen code sau khi approve.
4. **GEN:** viết code → `output/stage_2/<cap>/<mode>/` + ghi `output/index.csv` (cột `filepath` = `<cap>/<mode>/<file>.py`).
5. **VALIDATE + SUBMIT + REVIEW** (bước 2-4 pipeline trên).

### Rule — Batch Gen & Universe Assignment (bắt buộc)

Mỗi lần gen `n` alpha, phải khai báo rõ alpha nào được thiết kế cho cap nào (trong 3 cap), trước khi viết code:

1. **Khai báo trước khi gen:** nêu rõ `n`, danh sách alpha + `universe` mục tiêu (`VN-SMALL-CAP` / `VN-MID-CAP` / `VN-LARGE-CAP`) + `mode` (`time_series` / `cross_sectional`).
2. **Khai báo trong response:** bảng alpha → universe → mode → level + 1 dòng lý do chọn cap được trình bày **trực tiếp trong câu trả lời cho user** (không ghi thành file markdown riêng — nguồn chính thức là `output/index.csv` cột `universe`).
3. **Thiết kế riêng theo cap:** tham số + thesis phải hợp cap đó (vd small-cap biến động mạnh hơn → chấp nhận MaxDD lớn hơn; large-cap ổn định → yêu cầu Sharpe cao hơn). Không dùng chung 1 alpha cho mọi cap.
4. **Ghi universe vào `index.csv`** cho từng file (cột `universe`) — để `check_results.py` đánh PASS đúng ngưỡng của cap.
5. **Submit theo cap:** gọi `submit_and_check.py --batch --universe <CAP>` riêng cho từng cap (flag là FILTER; universe thực ghi CSV suy từ path cap).

Ví dụ khai báo batch:
| # | Alpha | Universe | Mode | Level |
|:-:|-------|----------|------|:-----:|
| 1 | VnSmallEpsMomentum | VN-SMALL-CAP | time_series | 1 |
| 2 | VnMidRoEQuality | VN-MID-CAP | time_series | 2 |
| 3 | VnLargeCsValueRank | VN-LARGE-CAP | cross_sectional | 4 |

---

## Alpha Creation Workflow (Vòng 1 — ARCHIVED)

Quy trình 7 bước sau khi nghĩ ra alpha idea mới (vòng 1 — futures intraday):

```bash
# 1. NGHĨ Ý TƯỞNG → ghi vào idea/planning_alpha/stage_1/alpha_data_type_ideas.md

# 2. CHECK TRÙNG (tránh viết lại strategy đã có)
python backtest/check_duplicate.py --check
python backtest/check_duplicate.py --idea DT_IDEA_15min.py

# 3. VIẾT STRATEGY → tạo file trong output/data_type_alpha/

# 4. SUBMIT & VERIFY
python tools/submit_and_check.py

# 5. NẾU FAIL → fix hoặc replace, quay lại bước 3

# 6. UPDATE INDEX
python backtest/check_duplicate.py --index

# 7. COMMIT + PUSH
```

---

## Problem → Solution Lookup

Khi gặp vấn đề, tra theo triệu chứng:

| Triệu chứng | File cần đọc | Fix |
|-------------|-------------|-----|
| **Không biết bắt đầu gen strategy Round 2** | `agent/framework_build_guide.md` | Blueprint Level 1-5 + 2 mode |
| **Round 2 rules không rõ** | `agent/stage_2_guideline.md` | Universes, modes, point-in-time, scoring |
| **Không biết field nào dùng được** | `syntax/data_syntax.md` | 496 fields + mode contract |
| **Trộn series/panel bị lỗi** | `template_example/strategy_framework.md` §Mode Contract | Chọn 1 mode, đúng suffix |
| **Fundamentals bị look-ahead** | `template_example/strategy_framework.md` §5 | Chỉ dùng sau ngày công bố, `.notna()` |
| **Sharpe < 1.5 (vòng 1)** | `data/vietnam_market_characteristics_v1.md` §5 (Sharpe Rules) | Thiếu ADX filter, return_roll, volume confirm |
| **Max DD > -40% (vòng 1)** | `data/vietnam_market_characteristics_v1.md` §7 (Risk Management) | Thiếu session gating, exit quá chậm |
| **Strategy không publish được** | `template_example/strategy_framework.md` §Checklist | Docstring thiếu thesis, position bounds sai |
| **Look-ahead bias** | `template_example/strategy_framework.md` §Data Access | Dùng `pv_close` thay vì `pv_open` |
| **Generator ra code sai** | `tools/generate_strategies.py` search `inject_filters` | Fix generator, regenerate |
| **Không biết tham số nào cho TF nào** | `syntax/time_series/parameters.md` (Round 2) / `agent/GUIDE.md` §Window Sizing (vòng 1) | Bảng tham số đầy đủ |
| **Cần thêm template mới** | `tools/generate_strategies.py` search `TEMPLATES` | Thêm vào TEMPLATES dict |
| **Cần validate output** | `python tools/validate_framework.py --strict` | Run validator (strict bắt warning) |
| **Cần hiểu VN market behavior** | `data/vietnam_market_characteristics.md` | Full analysis + mapping table |
| **Cần cải thiện Sharpe** | `idea/planning_alpha/stage_1/enhancement_return_roll_tiered_session.md` | 3 enhancements đã implement (A/B/C) |
| **Cần thêm alpha ideas** | `idea/planning_alpha/stage_1/alpha_generation_rolling_mean_quantile.md` | ~890 variants tham khảo |
| **Cần planning scale** | `idea/planning_alpha/stage_1/scaling_proposal_500_10000_strategies.md` | Roadmap mở rộng |
| **Cần bắt đầu backtest** | `idea/planning_alpha/stage_1/backtest_plan.md` | Decision rules, tracking |
| **Cần check duplicate trước khi viết alpha mới** | `backtest/check_duplicate.py --check` | Run duplicate checker |
| **Cần tìm strategy theo feature** | `backtest/check_duplicate.py --feature adx` | Search by indicator |

---

## Generator Usage (Vòng 1 — ARCHIVED)

```bash
# Generate all strategies
python tools/generate_strategies.py

# Validate all output files
python tools/validate_framework.py

# Update strategy count stats
python tools/update_guide_stats.py
```

### Generator Architecture (Vòng 1 — ARCHIVED)
- **108 templates** in `TEMPLATES` dict with parameter variants
- **6 ADX templates** get tiered sizing (strong/weak split)
- **`inject_filters()`** post-processor adds return_roll, class attrs, session gating to ALL templates
- **Output**: `output/thesis_NN_name/TF/*.py` + `output/index.csv`

### Enhancements Implemented
| Enhancement | Scope | Status |
|-------------|-------|--------|
| A — return_roll filter | All 1774 strategies | ✅ |
| B — Tiered sizing | 6 ADX templates | ✅ |
| C — Session gating | All 1774 strategies | ✅ |

---

## Output Structure
```
output/
├── index.csv                        # Manifest Round 2 (filepath,thesis_group,template,mode,universe,description,params)
│                                    #   filepath = <cap>/<mode>/<file>.py; universe suy từ cap
├── STATS.md                         # Round 2 stats (do tools/update_guide_stats.py sinh)
├── stage_1/                         # ARCHIVE vòng 1 (VNFuture intraday futures)
│   ├── index.csv                    # Strategies manifest vòng 1 (xem STATS.md)
│   ├── thesis_NN_name/  TF/*.py     # Generated hypotheses (35 groups)
│   ├── single_feat_alpha/   *.py    # 47 single-feat strategies (manual)
│   │   └── tier2/           *.py    # 14 Tier 2 single-feat strategies
│   ├── multi_feat_alpha/    *.py    # 9 multi-feat strategies (manual)
│   └── data_type_alpha/     *.py    # 48 data-type alpha strategies (manual)
└── stage_2/                         # ACTIVE vòng 2 (Round 2 — daily equity) — agent viết trực tiếp
    ├── vn_small_cap/                # 1 thư mục con / cap
    │   ├── time_series/             #   + mode time_series (VD VnSmallEpsGrowthMomentum.py)
    │   └── cross_sectional/         #   + mode cross_sectional (VD VnSmallCsEpsRank.py)
    ├── vn_mid_cap/                  #   (VD VnMidTrendQuality.py / VnMidCsRoERank.py)
    └── vn_large_cap/                #   (VD VnLargeRevenueStability.py / VnLargeCsValueMomentum.py)
```
Xem `output/STATS.md` (do `tools/update_guide_stats.py` sinh ra) để biết số liệu Round 2.

---

## Commit Rule

Sau **mỗi lần thực thi** (sửa code, tạo file, update doc, validate pass), phải:

1. **Commit ngay** — mỗi task một commit, không gộp task không liên quan
2. **Push ngay** — `git push`
3. **Commit message** phải mô tả rõ thay đổi và lý do

Nguyên tắc: commit nhỏ, commit thường xuyên → dễ rollback, dễ review, dễ quản lý.

---

## Important Files

| File | When to reference | 
|------|-------------------|
| `agent/stage_2_guideline.md` | Every Round-2 session start — official rules |
| `agent/framework_build_guide.md` | Before generating Round-2 strategies |
| `idea/planning_alpha/_framework/MASTER_alpha_planning.md` | Master planning — 4-layer construction (data → feat → mask → op → position) |
| `data/vietnam_market_characteristics.md` | Round 2 — đặc thù 3 cap → chọn feature nhanh |
| `agent/migration_plan_v2.md` | Understanding V1→V2 migration status |
| `tools/common.py` | Round 2 — `PASS_THRESHOLDS_BY_UNIVERSE`, `is_pass()` |
| `tools/submit_and_check.py` | Round 2 — submit `output/stage_2/` → `backtest/results_stage_2.csv` |
| `tools/check_results.py` | Round 2 — review results theo universe |
| `tools/validate_framework.py` | Round 2 — validate compliance sau khi gen |
| `tools/generate_strategies.py` | **VÒNG 1** (generator — KHÔNG dùng cho Round 2; Round 2 agent viết trực tiếp `output/stage_2/`) |
| `tools/validate_framework.py` | After every generation |
| `idea/planning_alpha/stage_1/enhancement_return_roll_tiered_session.md` | Understanding implemented enhancements (A/B/C) |
| `idea/planning_alpha/stage_1/alpha_generation_rolling_mean_quantile.md` | ~890 alpha variants for new ideas |
| `idea/planning_alpha/stage_1/backtest_plan.md` | Starting backtest workflow |
| `idea/planning_alpha/stage_1/scaling_proposal_500_10000_strategies.md` | Scale-up roadmap |
| `idea/planning_alpha/stage_1/strategy_001_mean_quantile_rsi.md` | First strategy design reference |
| `idea/hypothesis/hyp_thesis_01_momentum.md` → `08_multifactor.md` | Hypothesis docs (30 hypotheses) |
| `output/STATS.md` | Auto-generated strategy count stats (run `tools/update_guide_stats.py`) |
| `backtest/check_duplicate.py` | Check duplicates before writing new alpha |
| `backtest/INDEX.md` | Backtest module documentation + dead code list |
| `tools/INDEX.md` | Tool reference — chọn đúng tool cho từng task |

---

## Key Decisions (Historical)

1. **return_roll filter first**: universal momentum smoothing added to all templates via `inject_filters()` post-processor — highest impact.
2. **Tiered sizing for ADX templates only**: 6 ADX templates get strong/weak split; non-ADX templates remain single-tier.
3. **Post-processing architecture**: `inject_filters()` in `render()` handles all 3 enhancements symmetrically.
4. **Session ranges for thesis 07 only**: `position_open_ranges` = ["02:00-04:30", "06:00-07:45"], `position_close_ranges` = ["04:20-04:30", "07:30-07:45"] — UTC times.
5. **User tightened targets**: Sharpe ≥ 2.5 (minimum 2.0), CAGR > 20%, Max DD > -20%, PF > 1.3, Calmar > 1.1.
