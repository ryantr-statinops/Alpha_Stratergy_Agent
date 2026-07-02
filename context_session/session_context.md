# Context Session — Alpha Bot

**Session Date:** 2026-07-02 (Updated)  
**Purpose:** Full context snapshot for AI Agent continuity — 805 multi-thesis strategies, Phase 1 Sharpe improvements  
**Next Agent:** Read this first, then proceed

---

## 1. Project Overview

Dự án nghiên cứu và phát triển chiến lược đầu tư định lượng cho nền tảng **XNOQuant**, tập trung vào thị trường phái sinh VnFuture (VN30F1M).

**Target:** 500+ chiến lược Published cho Vietnam Quant Challenge 2026  
**Status:** 805 strategies generated across 8 thesis groups × 4 timeframes  
**User tightened targets:** Sharpe ≥ 2.5 (min 2.0), CAGR > 20%, Max DD > -20%, PF > 1.3, Calmar > 1.1  
**Estimated current Sharpe:** 1.2-1.5 (after Phase 1 universal ADX filter)

**Core Tech Stack:**
- Python on XNOQuant platform
- Framework: `SimpleAlgorithm` → `CustomStrategy`
- API: `self.data`, `self.feat`, `self.op`, `self.set_positions()`

---

## 2. Directory Structure

```
ALPHA_BOT/
├── .agent/
│   └── GUIDE.md                        # AI onboarding + Problem→Solution lookup
├── context_session/
│   └── session_context.md              # File này
├── data/
│   ├── VnFuture.md                     # OHLCV + fut_* + pv_vn30_* + pv_dji_* fields
│   └── vietnam_market_characteristics.md  # VN market analysis, Sharpe rules, mapping table
├── feature/
│   └── feature_syntax.md               # 140+ indicators
├── operations/
│   └── operations_syntax.md            # 30+ operators
├── template_example/
│   ├── strategy_framework.md           # **Master spec** — multi-timeframe, thesis guide, VN30/DJI
│   └── (9 file .py mẫu)
├── idea/
│   ├── planning_alpha/
│   │   ├── alpha_generation_rolling_mean_quantile.md  # ~890 alpha
│   │   ├── enhancement_return_roll_tiered_session.md  # 3 enhancements implemented (A/B/C)
│   │   ├── backtest_plan.md              # 4-week backtest plan
│   │   ├── scaling_proposal_500_10000_strategies.md
│   │   └── strategy_001_mean_quantile_rsi.md
│   ├── hypothesis/
│   │   ├── hypothesis_framework.md     # 10-metric scorecard
│   │   └── hyp_thesis_01_momentum.md → 08_multifactor.md  # 30 hypotheses
│   └── stage_overview/
├── output/
│   ├── index.csv                       # Master manifest (805 strategies)
│   ├── thesis_01_momentum/             5min/ 15min/ 30min/ 60min/
│   ├── thesis_02_trend/                5min/ 15min/ 30min/ 60min/
│   ├── thesis_03_mean_reversion/       5min/ 15min/ 30min/ 60min/
│   ├── thesis_04_breakout/             5min/ 15min/ 30min/ 60min/
│   ├── thesis_05_cross_market/         15min/ 30min/ 60min/
│   ├── thesis_06_volume_flow/          15min/ 30min/ 60min/
│   ├── thesis_07_intraday_session/     5min/ 15min/
│   └── thesis_08_multifactor/          15min/ 30min/ 60min/
└── tools/
    ├── generate_strategies.py          # Multi-thesis generator: 38 templates, 3 enhancements, universal ADX
    └── validate_framework.py           # 24-rule comprehensive validator
```

---

## 3. Data Sources

### Core OHLCV (`self.data.pv_*`)
| Field | Usage |
|-------|-------|
| `pv_close` | Giá đóng cửa (chính) |
| `pv_high` | Giá cao nhất |
| `pv_low` | Giá thấp nhất |
| `pv_open` | Giá mở cửa (dùng `open_price`) |
| `pv_volume` | Khối lượng |
| `pv_vn30_open` | VN30 open |
| `pv_vn30_high` | VN30 high |
| `pv_vn30_low` | VN30 low |
| `pv_vn30_close` | VN30 close |
| `pv_vn30_volume` | VN30 volume |
| `pv_dji_open` | DJI open |
| `pv_dji_high` | DJI high |
| `pv_dji_low` | DJI low |
| `pv_dji_close` | DJI close |
| `pv_dji_volume` | DJI volume |

### VnFuture Futures (`self.data.fut_*_vn30f1m_1d`)
| Field | Ý nghĩa |
|-------|---------|
| `fut_matched_volume_vn30f1m_1d` | Khối lượng khớp lệnh |
| `fut_matched_value_vn30f1m_1d` | Giá trị khớp lệnh |
| `fut_agreed_volume_vn30f1m_1d` | Khối lượng thỏa thuận |
| `fut_agreed_value_vn30f1m_1d` | Giá trị thỏa thuận |
| `fut_total_volume_vn30f1m_1d` | Tổng khối lượng |
| `fut_total_value_vn30f1m_1d` | Tổng giá trị |
| `fut_open_interest_vn30f1m_1d` | Hợp đồng mở |

---

## 4. Feature Functions (`self.feat.*`)

**Key categories (full list in `feature/feature_syntax.md`):**

| Category | Functions |
|----------|-----------|
| Trend | `ema`, `sma`, `macd`, `adx`, `bbands`, `sar`, `kama`, `t3`, `tema`, `wma`, `trima`, `dema` |
| Momentum | `rsi`, `roc`, `cmo`, `stoch`, `willr`, `ultosc`, `trix`, `ppo`, `apo`, `aroon`, `bop`, `cci` |
| Volume | `obv`, `mfi`, `adosc`, `ad`, `cmf` |
| Rolling | `rolling_mean`, `rolling_quantile`, `rolling_std`, `rolling_zscore`, `rolling_median`, `rolling_max`, `rolling_min`, `rolling_sum`, `rolling_correlation`, `rolling_covariance`, `rolling_mad`, `rolling_argmax`, `rolling_argmin`, `rolling_rank`, `rolling_percentile_rank` |
| Price Transform | `avgprice`, `medprice`, `typprice`, `wclprice`, `hlc3`, `ohlc4`, `vwap`, `rolling_vwap` |
| Math | `add`, `sub`, `mult`, `div`, `sum`, `max`, `min`, `maxindex`, `minindex`, `minmax` |
| Candlestick | `doji`, `hammer`, `engulfing_pattern`, `morning_star`, `evening_star`, `harami_pattern`, `hikkake_pattern`, `three_white_soldiers`, `three_black_crows`, `marubozu`, `shooting_star`, `spinning_top` (+ ~40 more) |

**Important:** All function names are **lowercase**.

---

## 5. Operation Functions (`self.op.*`)

| Category | Functions |
|----------|-----------|
| Cross | `crossed_above`, `crossed_below`, `crossed`, `crossed_above_value`, `crossed_below_value` |
| Shift | `shift`, `diff`, `pct_change`, `previous`, `current` |
| State | `rising`, `falling`, `bars_since`, `hold_for`, `value_when` |
| Boolean | `and_`, `or_`, `not_`, `between`, `where`, `sign` |
| NA | `fillna`, `ffill`, `zero_ifna`, `isna`, `notna`, `isfinite` |
| Math | `abs`, `clip`, `replace` |

---

## 6. Framework Rules (`template_example/strategy_framework.md`)

### Template Structure
```python
class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        # STEP 1: self.data
        # STEP 2: self.feat
        # STEP 3: self.op + logic
        # STEP 4: self.set_positions()

        self.set_positions(exit_setup, position=0)    # Exit first
        self.set_positions(long_setup, position=1)     # Long second
        self.set_positions(short_setup, position=-1)   # Short third
```

### Hard Rules
- ❌ Không `import pandas`, `import numpy`
- ❌ Không biến `open` (dùng `open_price`)
- ❌ Không `SeriesT` type hints
- ❌ Không gọi API ngoài `self.set_positions()`
- ✅ Tên hàm feature luôn lowercase
- ✅ Thứ tự: Exit → Long → Short

### Position Values
| Value | Meaning |
|-------|---------|
| 0 | Flat / Exit |
| 1.0 | Full Long |
| 0.5 | Partial Long |
| -0.5 | Partial Short |
| -1.0 | Full Short |

---

## 7. Phase 1 — Universal ADX Filter (Implemented 2026-07-02)

### What changed
- **`inject_filters()`** post-processor now injects ADX into ALL templates that don't already have it:
  - Adds `high = self.data.pv_high`, `low = self.data.pv_low` if missing
  - Computes `adx = self.feat.adx(high, low, close, timeperiod=adx_window)`
  - Entry: `& (adx > 22)` on long_setup/short_setup (non-tiered templates only)
  - Exit: `| (adx < 15)` on exit_setup (non-tiered templates only)
- **6 tiered templates** (trend_macd, trend_quantile, trend_ema_adx, multifactor_zscore, multifactor_momentum, multifactor_trendvol) — unchanged, already had ADX with tiered thresholds
- **~32 non-ADX templates** now have universal ADX filter

### Current Sharpe Pipeline
```
Entry:    ADX > 22  +  return_roll > 0  +  (template-specific signal)
Exit:     ADX < 15  OR  abs(return_roll) < threshold  OR  (template-specific exit)
Sizing:   Non-tiered: 1.0 / 0 / -1.0
          Tiered (6 templates): 0.5 / 1.0 with ADX > 18 / > 22
Session:  position_close_after_n_candles + intraday_session ranges
```

---

## 8. Acceptance Criteria

### Metric Targets (User tightened)
| Metric | User Target | Competition Target |
|--------|:-----------:|:-----------------:|
| Sharpe Ratio | ≥ 2.5 (min 2.0) | ≥ 1.2 |
| CAGR | > 20% | ≥ 25% |
| Max Drawdown | > -20% | ≥ -40% |
| Profit Factor | > 1.3 | ≥ 1.7 |
| Calmar Ratio | > 1.1 | ≥ 0.9 |
| Sortino Ratio | — | ≥ 1.5 |

### Competition Scorecard (10 metrics, 13pts max, PASS ≥ 8.0)
```
Sharpe(2pt) + CAGR(2pt) + Sortino(1pt) + Calmar(1pt) +
MaxDD(2pt) + VaR(1pt) + CVaR(0.5pt) + Ulcer(0.5pt) +
Cost(0.5pt) + Correlation(0.5pt)
→ Must-pass: Sharpe, CAGR, MaxDD
```

---

## 9. Strategy Inventory (805 Strategies)

| # | Thesis Group | 5min | 15min | 30min | 60min | Total | Status |
|:-:|--------------|:----:|:-----:|:-----:|:-----:|:-----:|--------|
| 01 | Momentum | 33 | 33 | 33 | 33 | 132 | ✅ return_roll + ADX |
| 02 | Trend | 36 | 36 | 36 | 36 | 144 | ✅ 3 tiered + 2 non-tiered w/ ADX |
| 03 | Mean Reversion | 34 | 34 | 34 | 34 | 136 | ✅ return_roll + ADX |
| 04 | Breakout | 27 | 27 | 27 | 27 | 108 | ✅ return_roll + ADX |
| 05 | Cross-Market | — | 27 | 27 | 27 | 81 | ✅ return_roll + ADX |
| 06 | Volume & Flow | — | 32 | 32 | 32 | 96 | ✅ return_roll + ADX |
| 07 | Intraday Session | 24 | 24 | — | — | 48 | ✅ return_roll + ADX + session ranges |
| 08 | Multi-Factor | — | 20 | 20 | 20 | 60 | ✅ 3 tiered w/ ADX |
| | **Total** | **154** | **233** | **209** | **209** | **805** | **100% validated** |

---

## 10. Generator Architecture

- **38 templates** in `TEMPLATES` dict + parameter variant generators
- **`inject_filters()` post-processor** handles ALL enhancements:
  1. Class attributes (return_window, return_threshold, position_close, adx_window, session ranges)
  2. Data variable injection (high/low if needed for ADX)
  3. return_roll computation
  4. ADX computation + entry/exit filter (for non-ADX templates)
  5. Entry modification: `& (return_roll > 0)`, `& (adx > 22)`
  6. Exit modification: `| (abs(return_roll) < threshold)`, `| (adx < 15)`
- **Output**: `output/thesis_NN_name/TF/*.py` + `output/index.csv`
- **Validator**: `tools/validate_framework.py` — 24 rules, 25,685 checks

---

## 11. Knowledge Base

| File | Contents |
|------|----------|
| `data/VnFuture.md` | All data fields reference |
| `data/vietnam_market_characteristics.md` | VN market analysis, mapping table, Sharpe rules, risk management |
| `feature/feature_syntax.md` | 140+ indicators |
| `operations/operations_syntax.md` | 30+ operators |
| `template_example/strategy_framework.md` | Master spec, class structure, compliance checklist |
| `.agent/GUIDE.md` | AI onboarding, Problem→Solution, reading order |

---

## 12. What's Blocked / Not Done

- **Chưa backtest nào** — upload manual từng file lên XNOQuant, không có API/CLI
- **Không offline data** — platform có built-in data, không build được local simulator
- **Phase 2 chưa triển khai** — stricter entry thresholds (ROC > 0.5%, quantile 0.90/0.10)
- **Phase 3 chưa triển khai** — asymmetric exit optimization, consecutive loss protection
- **Session context cần update manual** — người dùng sẽ yêu cầu update khi cần

---

## 13. Workflow Status

```
Step 1: Alpha Generation    ✅ (890 alpha ideas in planning_alpha/)
Step 2: Planning & Hypoth   ✅ (8 hypothesis docs x 30 hypotheses)
Step 3: User Review         ✅ (Approved for current gen)
Step 4: Chain-of-Thought    ✅ (Phase 1 universal ADX filter)
Step 5: Output              ✅ (805 strategies — valid 100%)
```

**Next possible tasks:**
- Begin backtest on XNOQuant (paste 32 representative strategies)
- Update hypothesis docs with backtest results
- Phase 2: stricter thresholds (ROC > 0.5%, quantile 0.90/0.10)
- Phase 3: asymmetric exit + consecutive loss protection
- Correlation analysis for portfolio construction
- Generate more templates / split LONG/SHORT variants

---

*End of Context Session — Handoff ready for next AI Agent*
