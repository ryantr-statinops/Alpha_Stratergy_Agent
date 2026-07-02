# AI Agent Onboarding Guide — Alpha Bot

> **Đọc file này đầu tiên khi bắt đầu phiên làm việc mới.**
> File map toàn bộ knowledge base — đọc đúng thứ tự để build context nhanh nhất.

---

## Reading Order

| # | File | Purpose | Đọc khi nào |
|:-:|------|---------|-------------|
| 1 | `context_session/session_context.md` | Trạng thái dự án hiện tại: 805 strategies, tiến độ, blocking issues | **Đầu phiên** |
| 2 | `README.md` | Tổng quan project, 5-step workflow, project structure | **Đầu phiên** |
| 3 | `template_example/strategy_framework.md` | **Master spec** — class structure, multi-timeframe windows, VN30/DJI patterns, compliance checklist | **Trước khi code** |
| 4 | `data/vietnam_market_characteristics.md` | Đặc thù thị trường VN → thiết kế strategy, Sharpe optimization rules, regime detection | **Trước khi code** |
| 5 | `idea/hypothesis/hypothesis_framework.md` | Acceptance criteria: 10-metric weighted scorecard (Sharpe, CAGR, Sortino, Calmar, Max DD, VaR, CVaR, Ulcer, Cost, Correlation) | **Khi review hypothesis** |
| 6 | `data/VnFuture.md` | All data fields: OHLCV + futures + VN30 + DJI | **Khi cần tra field** |
| 7 | `feature/feature_syntax.md` | 140+ indicators reference | **Khi cần tra function** |
| 8 | `operations/operations_syntax.md` | 30+ operators reference | **Khi cần tra operator** |
| 9 | `idea/planning_alpha/enhancement_return_roll_tiered_session.md` | 3 enhancements implemented (return_roll, tiered sizing, session gating) | **Khi cần hiểu code hiện tại** |
| 10 | `idea/planning_alpha/alpha_generation_rolling_mean_quantile.md` | ~890 alpha variants (idea source) | **Khi cần thêm ý tưởng** |
| 11 | `idea/planning_alpha/backtest_plan.md` | Kế hoạch backtest 4 tuần, decision rules, tracking template | **Khi bắt đầu backtest** |
| 12 | `idea/planning_alpha/scaling_proposal_500_10000_strategies.md` | Kế hoạch mở rộng từ 500 lên 10000 strategies | **Khi planning scale** |
| 13 | `idea/planning_alpha/strategy_001_mean_quantile_rsi.md` | Strategy design mẫu đầu tiên — mean reversion + quantile + RSI | **Khi tham khảo mẫu** |

**Optimal order:** 1→2→3→4→5 first, then 6→7→8 on-demand when coding. Read 9→13 when needed.

---

## Quick Reference

### Stack
- Platform: **XNOQuant** (`https://alpha.xnoquant.io/build`)
- Class: `CustomStrategy(SimpleAlgorithm)`
- Method: `__algorithm__(self)` (not `__logic__`)
- API: `self.data.*`, `self.feat.*`, `self.op.*`, `self.set_positions()`
- No pandas, numpy, SeriesT, `open` variable

### Position Order
```python
self.set_positions(exit_setup, position=0)    # Exit first
self.set_positions(long_setup, position=1)     # Long second
self.set_positions(short_setup, position=-1)   # Short third
```

### 8 Thesis Groups
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

### Multi-Timeframe Window Sizing
| Timeframe | Fast | Mid | Slow | RSI | ADX | Vol | ReturnRoll | ReturnThresh | SessionCandles |
|:---------:|:----:|:---:|:----:|:---:|:---:|:---:|:----------:|:-------------:|:--------------:|
| 5min | 8 | 14 | 20 | 7 | 7 | 14 | 3 | 0.0001 | 72 |
| 15min | 13 | 26 | 34 | 10 | 10 | 20 | 5 | 0.0002 | 24 |
| 30min | 20 | 40 | 50 | 14 | 14 | 26 | 8 | 0.0003 | 12 |
| 60min | 30 | 60 | 100 | 21 | 21 | 34 | 14 | 0.0005 | 6 |

### Acceptance Criteria (10-metric weighted)
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

### Công thức Sharpe ≥ 2.0
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

## Problem → Solution Lookup

Khi gặp vấn đề, tra theo triệu chứng:

| Triệu chứng | File cần đọc | Fix |
|-------------|-------------|-----|
| **Sharpe < 1.5** | `data/vietnam_market_characteristics.md` §5 (Sharpe Rules) | Thiếu ADX filter, return_roll, volume confirm |
| **Max DD > -40%** | `data/vietnam_market_characteristics.md` §7 (Risk Management) | Thiếu session gating, exit quá chậm |
| **Strategy không publish được** | `template_example/strategy_framework.md` §Checklist | Docstring thiếu thesis, position bounds sai |
| **Look-ahead bias** | `template_example/strategy_framework.md` §Data Access | Dùng `pv_close` thay vì `pv_open` |
| **Generator ra code sai** | `tools/generate_strategies.py` search `inject_filters` | Fix generator, regenerate |
| **Không biết tham số nào cho TF nào** | `.agent/GUIDE.md` §Multi-Timeframe Window Sizing | Bảng tham số đầy đủ |
| **Cần thêm template mới** | `tools/generate_strategies.py` search `TEMPLATES` | Thêm vào TEMPLATES dict |
| **Cần validate output** | `python tools/validate_framework.py` | Run validator |
| **Cần hiểu VN market behavior** | `data/vietnam_market_characteristics.md` | Full analysis + mapping table |
| **Cần cải thiện Sharpe** | `idea/planning_alpha/enhancement_return_roll_tiered_session.md` | 3 enhancements đã implement (A/B/C) |
| **Cần thêm alpha ideas** | `idea/planning_alpha/alpha_generation_rolling_mean_quantile.md` | ~890 variants tham khảo |
| **Cần planning scale** | `idea/planning_alpha/scaling_proposal_500_10000_strategies.md` | Roadmap mở rộng |
| **Cần bắt đầu backtest** | `idea/planning_alpha/backtest_plan.md` | Decision rules, tracking |

---

## Generator Usage

```bash
# Generate all 805 strategies
python tools/generate_strategies.py

# Validate all output files
python tools/validate_framework.py
```

### Generator Architecture
- **38 templates** in `TEMPLATES` dict with parameter variants
- **6 ADX templates** get tiered sizing (strong/weak split)
- **`inject_filters()`** post-processor adds return_roll, class attrs, session gating to ALL templates
- **Output**: `output/thesis_NN_name/TF/*.py` + `output/index.csv`

### Enhancements Implemented
| Enhancement | Scope | Status |
|-------------|-------|--------|
| A — return_roll filter | All 805 strategies | ✅ |
| B — Tiered sizing | 6 ADX templates | ✅ |
| C — Session gating | All 805 strategies | ✅ |

---

## Output Structure
```
output/
├── index.csv                        # 805 strategies manifest
├── thesis_01_momentum/     5min/ 15min/ 30min/ 60min/
├── thesis_02_trend/         5min/ 15min/ 30min/ 60min/
├── thesis_03_mean_reversion/ 5min/ 15min/ 30min/ 60min/
├── thesis_04_breakout/      5min/ 15min/ 30min/ 60min/
├── thesis_05_cross_market/        15min/ 30min/ 60min/
├── thesis_06_volume_flow/         15min/ 30min/ 60min/
├── thesis_07_intraday_session/    5min/ 15min/
└── thesis_08_multifactor/         15min/ 30min/ 60min/
```

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
| `context_session/session_context.md` | Every session start |
| `tools/generate_strategies.py` | ALL code changes go here (NEVER patch output files) |
| `tools/validate_framework.py` | After every generation |
| `idea/planning_alpha/enhancement_return_roll_tiered_session.md` | Understanding implemented enhancements (A/B/C) |
| `idea/planning_alpha/alpha_generation_rolling_mean_quantile.md` | ~890 alpha variants for new ideas |
| `idea/planning_alpha/backtest_plan.md` | Starting backtest workflow |
| `idea/planning_alpha/scaling_proposal_500_10000_strategies.md` | Scale-up roadmap |
| `idea/planning_alpha/strategy_001_mean_quantile_rsi.md` | First strategy design reference |
| `idea/hypothesis/hyp_thesis_01_momentum.md` → `08_multifactor.md` | Hypothesis docs (30 hypotheses) |

---

## Key Decisions (Historical)

1. **return_roll filter first**: universal momentum smoothing added to all templates via `inject_filters()` post-processor — highest impact.
2. **Tiered sizing for ADX templates only**: 6 ADX templates get strong/weak split; non-ADX templates remain single-tier.
3. **Post-processing architecture**: `inject_filters()` in `render()` handles all 3 enhancements symmetrically.
4. **Session ranges for thesis 07 only**: `position_open_ranges` = ["02:00-04:30", "06:00-07:45"], `position_close_ranges` = ["04:20-04:30", "07:30-07:45"] — UTC times.
5. **User tightened targets**: Sharpe ≥ 2.5 (minimum 2.0), CAGR > 20%, Max DD > -20%, PF > 1.3, Calmar > 1.1.
