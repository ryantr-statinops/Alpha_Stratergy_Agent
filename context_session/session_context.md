# Context Session — Alpha Bot (Phase: Planning Thesis 18→38)

**Session Date:** 2026-07-12
**Purpose:** Brainstorm & plan 21 new alpha groups (Thesis 18→38) từ 20 viable ideas
**Next Agent:** Đọc file này trước, sau đó đọc `idea/planning_alpha/alpha_ideas_master_plan.md` để tiếp tục

---

## 1. Hiện trạng dự án

| Hạng mục | Trạng thái |
|----------|:----------:|
| Thesis 01–17 | ✅ Implemented, generated, pushed |
| `tools/generate_strategies.py` | ✅ 1615 strategy variants |
| `output/` | ✅ 1615 files across 17 thesis folders |
| `context_session/` | ✅ Updated |
| `syntax/data_syntax.md` | ✅ Updated với macro fields mới |
| `template_example/strategy_framework.md` | ✅ Updated với position_setup notices |

### Thesis currently deployed (01–17)

| Thesis | Templates | Status |
|:------:|:---------:|:------:|
| 01 Momentum | A→G (7) | ✅ |
| 02 Trend | A→F (6) | ✅ |
| 03 Mean Reversion | A→E (5) | ✅ |
| 04 Breakout | A→G (7) | ✅ |
| 05 Cross-Market | A→G (7) | ✅ |
| 06 Volume & Flow | A→E (5) | ✅ |
| 07 Intraday Session | A→C (3) | ✅ |
| 08 Multi-Factor | A→E (5) | ✅ |
| 09—10 Regime | A→C (6) | ✅ |
| 11 VWAP Basis | A→D (4) | ✅ |
| 12 Kalman Filter | A→D (4) | ✅ |
| 13 CMF + Squeeze | A (1) | ✅ |
| 14 BB Squeeze Reversal | A, C (2) | ✅ |
| 15 MAVP Adaptive | A, B, C (3) | ✅ |
| 16 Price-Vol Velocity | A (1) | ✅ |
| 17 Vol-Adj Momentum | A, B, C (3) | ✅ |

---

## 2. Current Work — Thesis 18→38 Planning

### Nguồn gốc
Brainstorm 50 ideas → filter qua `syntax/feature_syntax.md` → còn **20 alpha khả thi**.
Đã đối chiếu với 17 thesis hiện có: **không trùng lặp**.

### 20 Alpha Ideas (Grouped)

| Nhóm | Ideas | Số lượng |
|:-----|:------|:--------:|
| A — Price Position | Range Rank, BB Distance, MinMax Scaling | 3 |
| B — Momentum Dynamics | Momentum Decay, Return Mean, MACD Hist Div | 3 |
| C — Volume/Flow | VPD, P-V Correlation, CMF Quantile | 3 |
| D — Volatility/Regime | LogRet Vol, BB Squeeze, Vol-of-Vol, ADX Accel | 4 |
| E — Enhanced MR | RSI Quantile, Cointegration, VWAP Dev, Sharpe Gate | 4 |
| F — Pattern & Composite | Candle Ratio, Regression Channel, StdRet Quantile | 3 |
| G — Macro | Interbank, USD/VND | 2 |

### Mapping → 21 Theses (18→38)

| Thesis | Core Idea | Templates | TF |
|:------:|-----------|:---------:|:--:|
| 18 | Range Rank Breakout | A, B | 15, 30 |
| 19 | BB Relative Position | A, B, C | 15, 30, 60 |
| 20 | MinMax Scaling | A, B | 15, 30, 60 |
| 21 | Momentum Decay | A, B | 15, 30 |
| 22 | Return Mean Drift | A, B | 15, 30 |
| 23 | MACD Hist Divergence | A, B | 15, 30, 60 |
| 24 | Volume-Price Divergence | A, B | 15, 30 |
| 25 | Price-Volume Correlation | A, B | 15, 30, 60 |
| 26 | CMF Quantile Threshold | A, B | 15, 30 |
| 27 | Log-Return Vol Filter | A, B | 15, 30 |
| 28 | BB Width Squeeze | A, B | 15, 30, 60 |
| 29 | Vol-of-Vol (ATR Var) | A, B | 15, 30 |
| 30 | ADX Acceleration | A, B | 15, 30, 60 |
| 31 | RSI Quantile MR | A, B | 15, 30 |
| 32 | Cointegration Spread | A, B | 15, 30, 60 |
| 33 | Regression Channel | A, B | 15, 30, 60 |
| 34 | VWAP Deviation | A, B | 15, 30 |
| 35 | Rolling Sharpe Gate | A, B | 15, 30, 60 |
| 36 | Candle Body Ratio | A, B | 15, 30 |
| 37 | StdRet Quantile | A, B | 15, 30 |
| 38 | Macro Regime Context | A, B, C | 15, 30 |

**Total dự kiến:** ~49 templates

---

## 3. Quy tắc code (reminder)

1. **Pipeline**: `Exit → Long → Short`, có `assert not (long_signal & short_signal).any()`
2. **Exit**: `atr_stop | trailing` (universal, đã chứng minh qua T14-C)
3. **Position**: fixed scalar (-1/0/1)
4. **Data**: `pv_close`, `pv_high`, `pv_low`, `pv_volume`, `pv_open` (Core)
5. **Cross**: `pv_vn30_close` cho thesis 32, `pv_dji_close` cho thesis 38
6. **Macro**: interbank & USD/VND daily cho thesis 38

---

## 4. Việc cần làm tiếp theo

1. ✅ **Brainstorm hoàn tất** — 20 alpha ideas verified
2. ✅ **Master plan written** — `idea/planning_alpha/alpha_ideas_master_plan.md`
3. ⬜ **User review** — review master plan, adjust if needed
4. ⬜ **Write hypothesis files** — `idea/hypothesis/hyp_thesis_18_*.md` → `hyp_thesis_38_*.md`
5. ⬜ **Add code to generate_strategies.py** — T18→38 codes
6. ⬜ **Regenerate output/**
7. ⬜ **Upload to XNOQuant — Simulate + scorecard**

---

## 5. File quan trọng

| File | Vai trò |
|------|---------|
| `idea/planning_alpha/alpha_ideas_master_plan.md` | Master plan chi tiết Thesis 18→38 |
| `tools/generate_strategies.py` | Template generator (single source of truth) |
| `syntax/feature_syntax.md` | Feature API catalog |
| `syntax/data_syntax.md` | Data field catalog (đã update macro fields) |
| `template_example/strategy_framework.md` | Framework rules (đã update position notices) |

---

*End of Context Session — Đã hoàn tất brainstorming. Chờ user review master plan.*
