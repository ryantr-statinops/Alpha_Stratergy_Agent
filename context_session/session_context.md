# Context Session — Alpha Bot

**Session Date:** 2026-07-01  
**Purpose:** Full context snapshot for AI Agent continuity  
**Next Agent:** Read this first, then proceed

---

## 1. Project Overview

Dự án nghiên cứu và phát triển chiến lược đầu tư định lượng cho nền tảng **XNOQuant**, tập trung vào thị trường phái sinh VnFuture (VN30F1M).

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
│   └── VnFuture.md                     # Dữ liệu fut_* fields
├── feature/
│   └── feature_syntax.md               # 140+ indicators
├── operations/
│   └── operations_syntax.md            # 30+ operators
├── template_example/
│   ├── strategy_framework.md           # **Master spec** — đọc trước khi code
│   ├── (9 file .py mẫu)
├── idea/
│   ├── planning_alpha/
│   │   ├── alpha_generation_rolling_mean_quantile.md  # ~890 alpha
│   │   ├── strategy_001_mean_quantile_rsi.md          # Plan cho Strategy #001
│   │   └── scaling_proposal_500_10000_strategies.md   # Scaling architecture
│   ├── hypothesis/
│   │   ├── hypothesis_framework.md     # Testing framework + acceptance criteria
│   │   └── hyp_strategy_001.md         # Hypothesis test cases
│   └── stage_overview/
│       └── session_overview.md         # Session log
├── output/
│   ├── index.csv                       # Master manifest (50 strategies)
│   ├── A_rolling_mean_level/           # 8 files
│   ├── B_rolling_mean_crossover/       # 6 files
│   ├── C_mean_confirmation/            # 9 files
│   ├── D_rolling_quantile_level/       # 6 files
│   ├── E_quantile_channel/             # 5 files
│   ├── F_quantile_confirmation/        # 5 files
│   ├── H_vnfuture_specific/            # 5 files
│   └── I_combined_mean_quantile/       # 6 files
└── tools/
    └── generate_strategies.py          # Batch generator script
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
| `pv_vn30_close` | VN30 close |

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

---

## 7. Acceptance Criteria (`idea/hypothesis/hypothesis_framework.md`)

### Metric Targets (Bắt buộc)

| Metric | Target |
|--------|--------|
| Sharpe Ratio | ≥ 1.2 |
| CAGR | ≥ 25% |
| Max Drawdown | ≥ -40% |
| Profit Factor | ≥ 1.7 |
| Calmar Ratio (CAGR/DD) | ≥ 0.9 |

### Multi-Stage Validation
- **Stage Train:** 70% dữ liệu (cho phép tune, không overfit)
- **Stage Test:** 30% dữ liệu giấu kín (pass target mới được deploy)

### Verdict
| Điều kiện | Kết quả |
|-----------|---------|
| Train ≥ 4/5 | → Sang Test |
| Test ≥ 4/5 | → PASS, deploy |
| Test < 4/5 | → REJECT, redesign |

---

## 8. Strategy Inventory (50 Strategies)

| Alpha ID | Family | File | Logic |
|----------|--------|------|-------|
| A-005 | A_rolling_mean_level | `A-005_MeanLevel8.py` | close > mean(8) → LONG |
| A-006 | A_rolling_mean_level | `A-006_MeanLevel8.py` | close < mean(8) → SHORT |
| A-009 | A_rolling_mean_level | `A-009_MeanLevel14.py` | close > mean(14) → LONG |
| A-010 | A_rolling_mean_level | `A-010_MeanLevel14.py` | close < mean(14) → SHORT |
| A-013 | A_rolling_mean_level | `A-013_MeanLevel30.py` | close > mean(30) → LONG |
| A-014 | A_rolling_mean_level | `A-014_MeanLevel30.py` | close < mean(30) → SHORT |
| A-017 | A_rolling_mean_level | `A-017_MeanLevel100.py` | close > mean(100) → LONG |
| A-018 | A_rolling_mean_level | `A-018_MeanLevel100.py` | close < mean(100) → SHORT |
| B2-001 | B_rolling_mean_crossover | `B2-001_MACross5_20.py` | MA5 > MA20 → LONG |
| B2-002 | B_rolling_mean_crossover | `B2-002_MACross5_20.py` | MA5 < MA20 → SHORT |
| B2-009 | B_rolling_mean_crossover | `B2-009_MACross10_30.py` | MA10 > MA30 → LONG |
| B2-010 | B_rolling_mean_crossover | `B2-010_MACross10_30.py` | MA10 < MA30 → SHORT |
| B2-015 | B_rolling_mean_crossover | `B2-015_MACross20_100.py` | MA20 > MA100 → LONG |
| B2-016 | B_rolling_mean_crossover | `B2-016_MACross20_100.py` | MA20 < MA100 → SHORT |
| C-005 | C_mean_confirmation | `C-005_Mean50ROC.py` | close > mean(50) & ROC > 0 |
| C-006 | C_mean_confirmation | `C-006_Mean50ROC.py` | close < mean(50) & ROC < 0 |
| C-007 | C_mean_confirmation | `C-007_Mean14ADX.py` | close > mean(14) & ADX > 20 |
| C-008 | C_mean_confirmation | `C-008_Mean14ADX.py` | close < mean(14) & ADX > 20 |
| C-013 | C_mean_confirmation | `C-013_Mean14MACD.py` | close > mean(14) & MACD > Signal |
| C-014 | C_mean_confirmation | `C-014_Mean14MACD.py` | close < mean(14) & MACD < Signal |
| C-019 | C_mean_confirmation | `C-019_Mean20Volume.py` | close > mean(20) & Vol > SMA |
| C-020 | C_mean_confirmation | `C-020_Mean20Volume.py` | close < mean(20) & Vol > SMA |
| C-025 | C_mean_confirmation | `C-025_Mean14CMO.py` | close > mean(14) & CMO > 0 |
| D-001 | D_rolling_quantile_level | `D-001_QuantileChannel10_80.py` | close > Q80(10) → LONG |
| D-002 | D_rolling_quantile_level | `D-002_QuantileChannel10_80.py` | close < Q20(10) → SHORT |
| D-019 | D_rolling_quantile_level | `D-019_QuantileChannel30_90.py` | close > Q90(30) → LONG |
| D-020 | D_rolling_quantile_level | `D-020_QuantileChannel30_90.py` | close < Q10(30) → SHORT |
| D-031 | D_rolling_quantile_level | `D-031_QuantileChannel100_75.py` | close > Q75(100) → LONG |
| D-032 | D_rolling_quantile_level | `D-032_QuantileChannel100_75.py` | close < Q25(100) → SHORT |
| E1-001 | E_quantile_channel | `E1-001_QChannel10_80_20.py` | Close > Q80(10) → L, < Q20(10) → S |
| E1-003 | E_quantile_channel | `E1-003_QChannel20_80_20.py` | same, window=20 |
| E1-006 | E_quantile_channel | `E1-006_QChannel14_90_10.py` | Close > Q90(14) → L, < Q10(14) → S |
| E2-001 | E_quantile_channel | `E2-001_QRev10_80_20.py` | Reversion: short at Q80, long at Q20 |
| E2-003 | E_quantile_channel | `E2-003_QRev20_80_20.py` | Reversion, window=20 |
| F-001 | F_quantile_confirmation | `F-001_Q14RSI.py` | Close > Q80(14) & RSI > 50 |
| F-002 | F_quantile_confirmation | `F-002_Q14RSI.py` | Close < Q20(14) & RSI < 50 |
| F-005 | F_quantile_confirmation | `F-005_Q20ADX.py` | Close > Q80(20) & ADX > 20 |
| F-006 | F_quantile_confirmation | `F-006_Q20ADX.py` | Close < Q20(20) & ADX > 20 |
| F-013 | F_quantile_confirmation | `F-013_Q20Volume.py` | Close > Q80(20) & Vol > SMA |
| H-001 | H_vnfuture_specific | `H-001_MatchedVolMean14.py` | matched_vol > mean(14) |
| H-003 | H_vnfuture_specific | `H-003_OpenInterestQ80.py` | OI > Q80(20) & price > mean(20) |
| H-005 | H_vnfuture_specific | `H-005_OpenInterestMean14.py` | OI > mean(14) & price > mean(14) |
| H-009 | H_vnfuture_specific | `H-009_TotalVolMean20.py` | total_vol > mean(20) & price > mean(20) |
| H-021 | H_vnfuture_specific | `H-021_MatchedValQ80.py` | matched_val > Q80(14) & price > mean(14) |
| I-000 | I_combined_mean_quantile | `I-000_VNFutureMeanQuantileRSI.py` | close > Q80 > mean(14) & RSI > 50 |
| I-001 | I_combined_mean_quantile | `I-001_Mean14Q10RSI.py` | close > Q80(10) > mean(14) & RSI > 50 |
| I-002 | I_combined_mean_quantile | `I-002_Mean14Q10RSI.py` | close < Q20(10) < mean(14) & RSI < 50 |
| I-003 | I_combined_mean_quantile | `I-003_Mean20Q14Volume.py` | close > Q80(14) > mean(20) & Vol > SMA |
| I-005 | I_combined_mean_quantile | `I-005_Mean50Q20ADX.py` | close > Q80(20) > mean(50) & ADX > 20 |
| I-006 | I_combined_mean_quantile | `I-006_Mean50Q20ADX.py` | close < Q20(20) < mean(50) & ADX > 20 |

---

## 9. Workflow Status

```
Step 1: Alpha Generation    ✅ (890 alpha in planning_alpha/)
Step 2: Planning & Hypoth   ✅ (Strategy #001 planned + 6 hypotheses)
Step 3: User Review          ✅ (Approved)
Step 4: Chain-of-Thought     ✅ (Strategy #001 coded)
Step 5: Output               ✅ (50 strategies generated in output/)
```

**Next possible tasks:**
- Generate more strategies (up to 10,000 using `tools/generate_strategies.py`)
- Update `output/index.csv` with more metadata columns
- Create detailed hypothesis docs for other strategies
- Refactor generator to support all 890 alpha variants

---

## 10. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| `__algorithm__()` not `__logic__()` | All templates use `__algorithm__` |
| Class `CustomStrategy(SimpleAlgorithm)` | Consistent naming across all files |
| No pandas/numpy imports | Framework handles internally |
| Lowercase feat functions (`ema`, `rsi`) | Matches `feature_syntax.md` API |
| Exit → Long → Short order | Framework requirement (strategy_framework.md) |
| `output/` subdirectories by family | Scale to 10,000+ strategies |
| `output/index.csv` manifest | Tra cứu nhanh, filter được |
| Fake data not used | Only `self.data.*` fields allowed |

---

*End of Context Session — Handoff ready for next AI Agent*
