# Output — Strategy Catalog

> **805 strategies** — 8 thesis groups × 4 timeframes × template variants  
> All enhanced with return_roll filter + universal ADX filter + session gating  
> 100% validated (25,685 checks, 24 rules)

---

## Overview

| Metric | Value |
|--------|-------|
| Total strategies | 805 |
| Thesis groups | 8 |
| Timeframes | 5min / 15min / 30min / 60min |
| Templates | 38 (in generator) |
| Entry filters | ADX > entry_threshold (TF-dependent: 22/20/18/16), return_roll > 0, volume confirm |
| Exit filters | ADX < exit_threshold (TF-dependent: 15/14/12/10), abs(return_roll) < threshold, signal reversal |
| Direction | All BOTH long + short |
| Validation | 24 rules, 100% pass |

---

## Inventory

| Thesis | Folder | 5min | 15min | 30min | 60min | Total | Type |
|--------|--------|:----:|:-----:|:-----:|:-----:|:-----:|------|
| **01 — Momentum** | `thesis_01_momentum/` | 33 | 33 | 33 | 33 | **132** | ROC, CMO, VN30 confirm, volume |
| **02 — Trend** | `thesis_02_trend/` | 36 | 36 | 36 | 36 | **144** | MA cross, MACD, quantile, EMA+ADX, Aroon |
| **03 — Mean Reversion** | `thesis_03_mean_reversion/` | 34 | 34 | 34 | 34 | **136** | Quantile, RSI, BBands, VolClimax, CCI |
| **04 — Breakout** | `thesis_04_breakout/` | 27 | 27 | 27 | 27 | **108** | Quantile BO, Donchian, Range, VN30 |
| **05 — Cross-Market** | `thesis_05_cross_market/` | — | 27 | 27 | 27 | **81** | Relative, DJI, Consensus, Gap |
| **06 — Volume & Flow** | `thesis_06_volume_flow/` | — | 32 | 32 | 32 | **96** | OI, Matched Vol/Val, OBV, MFI |
| **07 — Intraday Session** | `thesis_07_intraday_session/` | 24 | 24 | — | — | **48** | Open Drive, Lunch Rev, Close Sq, Gap Fill |
| **08 — Multi-Factor** | `thesis_08_multifactor/` | — | 20 | 20 | 20 | **60** | Z-score, Momentum MF, Trend+Vol |
| | | **154** | **233** | **209** | **209** | **805** | |

---

## Strategy Structure

Every strategy file follows this pattern:

```python
"""
name:    MomFast_5min
summary: Momentum: ROC(8) — 5min
thesis:  momentum | 5min
idea:    Pure momentum: ROC direction
"""
class CustomStrategy(SimpleAlgorithm):

    roc_window = 8                     # Template-specific params
    return_window = 3                  # ← Enhancement A: return_roll
    return_threshold = 0.0001          # ← Enhancement A
    position_close_after_n_candles = 72 # ← Enhancement C: session gating
    adx_window = 7                     # ← Phase 1: universal ADX

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high       # ← Added for ADX
        low = self.data.pv_low         # ← Added for ADX
        return_1 = self.op.fillna(...) # ← Enhancement A
        return_roll = self.feat.rolling_mean(...) # ← Enhancement A
        adx = self.feat.adx(...)       # ← Phase 1: universal ADX

        long_setup = (signal) & (return_roll > 0) & (adx > 22)
        short_setup = (signal) & (return_roll < 0) & (adx > 22)
        exit_setup = (signal) | (abs(return_roll) < threshold) | (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
```

### Timeframe-Dependent Parameters

| Param | 5min | 15min | 30min | 60min |
|-------|:----:|:-----:|:-----:|:-----:|
| ROC (fast) | 5 | 8 | 13 | 20 |
| ROC (mid) | 10 | 14 | 20 | 30 |
| ROC (slow) | 14 | 20 | 30 | 40 |
| return_window | 2 | 3 | 5 | 8 |
| return_threshold | 0.01% | 0.03% | 0.06% | 0.10% |
| ADX window | 5 | 7 | 9 | 12 |
| ADX entry threshold | > 22 | > 20 | > 18 | > 16 |
| ADX exit threshold | < 15 | < 14 | < 12 | < 10 |
| Max hold (candles) | 72 | 24 | 12 | 6 |

### 6 Tiered Templates (thesis 02 + 08)

Use strong/weak split instead of single setup:
- `strong_long`: ADX > 22-25 + return_roll + volume → position = 1.0
- `weak_long`: ADX > 18-20 + return_roll → position = 0.5
- `strong_short`: position = -1.0
- `weak_short`: position = -0.5

---

## Index File

`index.csv` — master manifest with fields:

| Field | Description |
|-------|-------------|
| `alpha_id` | Unique ID: `{thesis_id}-{counter:04d}` |
| `thesis_group` | Folder name (e.g. `thesis_01_momentum`) |
| `timeframe` | 5min / 15min / 30min / 60min |
| `direction` | Always BOTH (long + short) |
| `thesis_id` | 1-8 |
| `file` | Relative path from `output/` |
| `name` | Strategy name |
| `summary` | Human-readable description |

---

## Enhancements Applied

| Enhancement | Scope | Implementation |
|-------------|-------|----------------|
| **A — return_roll filter** | All 805 | `return_roll > 0` entry, `abs(return_roll) < threshold` exit |
| **B — Tiered sizing** | 6 ADX templates | strong 1.0 / weak 0.5 split by ADX level |
| **C — Session gating** | All 805 | `position_close_after_n_candles`, Thesis 07: open/close ranges |
| **Phase 1 — Universal ADX** | All non-ADX templates | `adx > 22` entry, `adx < 15` exit |

---

## How to Use

1. **Backtest**: Copy file content → paste into XNOQuant editor → Simulate
2. **Filter by thesis**: Browse `thesis_NN_*/` subdirectories
3. **Filter by timeframe**: Pick `5min/`, `15min/`, `30min/`, `60min/`
4. **Find by ID**: Search `index.csv` for `alpha_id`

### Recommended First Backtests (32 strategies)

See `idea/planning_alpha/backtest_plan.md` for the full screening plan.
