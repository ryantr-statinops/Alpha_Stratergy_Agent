# Context Session — Alpha Bot

**Session Date:** 2026-07-02 (Updated)  
**Purpose:** Full context snapshot for AI Agent continuity — 805 multi-thesis strategies generated  
**Next Agent:** Read this first, then proceed

---

## 1. Project Overview

Dự án nghiên cứu và phát triển chiến lược đầu tư định lượng cho nền tảng **XNOQuant**, tập trung vào thị trường phái sinh VnFuture (VN30F1M).

**Target:** 500+ chiến lược Published cho Vietnam Quant Challenge 2026  
**Status:** 805 strategies generated across 8 thesis groups × 4 timeframes  
**Scoring:** Sharpe ≥ 1.2, CAGR ≥ 25%, Sortino ≥ 1.5, Calmar ≥ 0.9, weighted 10-metric scorecard

**Core Tech Stack:**
- Python on XNOQuant platform
- Framework: `SimpleAlgorithm` → `CustomStrategy`
- API: `self.data`, `self.feat`, `self.op`, `self.set_positions()`

---

## 2. Directory Structure

```
ALPHA_BOT/
├── .gitignore
├── README.md                           # Master guide — đọc đầu tiên
├── context_session/
│   └── session_context.md              # File này
├── data/
│   └── VnFuture.md                     # OHLCV + fut_* + pv_vn30_* + pv_dji_* fields
├── feature/
│   └── feature_syntax.md               # 140+ indicators
├── operations/
│   └── operations_syntax.md            # 30+ operators
├── template_example/
│   ├── strategy_framework.md           # **Master spec** — multi-timeframe, thesis guide, VN30/DJI
│   ├── (9 file .py mẫu)
├── idea/
│   ├── planning_alpha/
│   │   ├── alpha_generation_rolling_mean_quantile.md  # ~890 alpha
│   │   ├── strategy_001_mean_quantile_rsi.md
│   │   └── scaling_proposal_500_10000_strategies.md
│   ├── hypothesis/
│   │   ├── hypothesis_framework.md     # Updated: 10-metric scorecard (Sortino, VaR, CVaR, Ulcer, Cost, Correlation)
│   │   └── hyp_strategy_001.md
│   └── stage_overview/
│       └── session_overview.md
├── output/
│   ├── index.csv                       # Master manifest (805 strategies, enhanced columns)
│   ├── thesis_01_momentum/             # 132 strategies
│   │   ├── 5min/  15min/  30min/  60min/
│   ├── thesis_02_trend/                # 144 strategies
│   │   ├── 5min/  15min/  30min/  60min/
│   ├── thesis_03_mean_reversion/       # 136 strategies
│   │   ├── 5min/  15min/  30min/  60min/
│   ├── thesis_04_breakout/             # 108 strategies
│   │   ├── 5min/  15min/  30min/  60min/
│   ├── thesis_05_cross_market/         # 81 strategies
│   │   ├── 15min/  30min/  60min/
│   ├── thesis_06_volume_flow/          # 96 strategies
│   │   ├── 15min/  30min/  60min/
│   ├── thesis_07_intraday_session/     # 48 strategies
│   │   ├── 5min/  15min/
│   └── thesis_08_multifactor/          # 60 strategies
│       ├── 15min/  30min/  60min/
└── tools/
    └── generate_strategies.py          # Multi-thesis generator: 35+ templates, parameter-grid variants
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

**Important:** All function names are **lowercase** (e.g., `self.feat.ema()`, not `self.feat.EMA()`).

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

### Multi-Timeframe Window Sizing

| Timeframe | Fast | Mid | Slow | RSI | ADX | Vol |
|:---------:|:----:|:---:|:----:|:---:|:---:|:---:|
| 5 min | 8 | 14 | 20 | 7 | 7 | 14 |
| 15 min | 13 | 26 | 34 | 10 | 10 | 20 |
| 30 min | 20 | 40 | 50 | 14 | 14 | 26 |
| 60 min | 30 | 60 | 100 | 21 | 21 | 34 |

---

## 7. Acceptance Criteria (`idea/hypothesis/hypothesis_framework.md`)

### Metric Targets (Cập nhật 2026-07-02 — 10 metrics, weighted scoring)

| Metric | Weight | Target |
|--------|:------:|--------|
| Sharpe Ratio | High | ≥ 1.2 |
| CAGR | High | ≥ 25% |
| Sortino Ratio | Medium | ≥ 1.5 |
| Calmar Ratio | Medium | ≥ 0.9 |
| Max Drawdown | High | ≥ -40% |
| Profit Factor | Medium | ≥ 1.7 |
| Value at Risk (VaR 95%) | Medium | ≥ -5% |
| Conditional VaR (CVaR 95%) | Low | ≥ -6% |
| Ulcer Index | Low | ≤ 12 |
| Cost (slippage + fee) | Low | ≤ 1% |
| Correlation (vs benchmark) | Low | ≤ 0.8 |

**Weight scoring:** HIGH=2pts, MEDIUM=1pt, LOW=0.5pt. Max=13pts. PASS ≥ 8.0 with Sharpe+CAGR+MaxDD MUST-PASS.

---

## 8. Strategy Inventory (805 Strategies)

**8 Thesis Groups × 4 Timeframes:**

| # | Thesis Group | 5min | 15min | 30min | 60min | Total | Key Indicators |
|:-:|--------------|:----:|:-----:|:-----:|:-----:|:-----:|----------------|
| 01 | Momentum | 33 | 33 | 33 | 33 | 132 | ROC, CMO, VN30 confirm |
| 02 | Trend | 36 | 36 | 36 | 36 | 144 | MA cross, MACD, ADX, Aroon |
| 03 | Mean Reversion | 34 | 34 | 34 | 34 | 136 | Quantile, RSI, BBands, CCI, VolClimax |
| 04 | Breakout | 27 | 27 | 27 | 27 | 108 | Quantile BO, Donchian, Range, VN30 |
| 05 | Cross-Market | — | 27 | 27 | 27 | 81 | Relative strength, DJI, Consensus, Gap |
| 06 | Volume & Flow | — | 32 | 32 | 32 | 96 | OI, Matched Vol/Val, OBV, MFI |
| 07 | Intraday Session | 24 | 24 | — | — | 48 | Open drive, Lunch rev, Close sqz, Gap fill |
| 08 | Multi-Factor | — | 20 | 20 | 20 | 60 | Z-score, Mom multi, Trend+Vol+VN30 |
| | **Total** | **154** | **233** | **209** | **209** | **805** | |

**Generator:** `tools/generate_strategies.py` — 35+ templates, parameter-grid variant generators, timeframe-aware window scaling. Template types: momentum_pure, momentum_vol, momentum_vn30, momentum_cascade, momentum_cmo, trend_ma_cross, trend_macd, trend_quantile, trend_ema_adx, trend_aroon, meanrev_quantile, meanrev_rsi, meanrev_bbands, meanrev_volclimax, meanrev_cci, breakout_quantile, breakout_donchian, breakout_range, breakout_vn30, cross_relative, cross_dji, cross_consensus, cross_gap, volume_oi, volume_matched_surge, volume_value, volume_obv, volume_mfi, intraday_open_drive, intraday_revert, intraday_close, intraday_gapfill, multifactor_zscore, multifactor_momentum, multifactor_trendvol.

---

## 9. Workflow Status

```
Step 1: Alpha Generation    ✅ (890 alpha in planning_alpha/)
Step 2: Planning & Hypoth   ✅ (Strategy #001 planned + 6 hypotheses)
Step 3: User Review          ✅ (Approved)
Step 4: Chain-of-Thought     ✅ (Strategy #001 coded)
Step 5: Output               ✅ (805 strategies — 8 thesis groups × 4 timeframes)
```

**Next possible tasks:**
- Backtest validation on XNOQuant platform (verify Sharpe, CAGR, Sortino)
- Create hypothesis documents for each thesis group
- Optimize strategy parameters via walk-forward validation
- Generate remaining strategies to reach 1,000+ (add more templates/variants)
- Split each "BOTH" strategy into separate LONG/SHORT variants
- Correlation analysis: identify low-correlation strategy portfolio
- Create thesis-specific documentation in `idea/hypothesis/`

---

## 10. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| `__algorithm__()` not `__logic__()` | All templates use `__algorithm__` |
| Class `CustomStrategy(SimpleAlgorithm)` | Consistent naming across all files |
| No pandas/numpy imports | Framework handles internally |
| Lowercase feat functions (`ema`, `rsi`) | Matches `feature_syntax.md` API |
| Exit → Long → Short order | Framework requirement (strategy_framework.md) |
| `output/thesis_NN_name/timeframe/` structure | Scales to 10,000+ strategies, filterable by thesis + timeframe |
| `output/index.csv` with thesis_group, timeframe, thesis_id | Enhanced metadata for filtering & analysis |
| Variant generators (parameter grids) | One template → 5-10 strategy variants via window/threshold sweeps |
| Timeframe-aware window scaling | 5/15/30/60 min use different default windows for appropriate signal sensitivity |
| VN30 + DJI data available | Cross-market relative strength, consensus, gap strategies |
| 10-metric weighted scorecard | Competition scoring: Sharpe > CAGR > Sortino > Calmar > Max DD > VaR > CVaR > Ulcer > Cost > Correlation |
| Fake data not used | Only `self.data.*` fields allowed |

---

*End of Context Session — Handoff ready for next AI Agent*
