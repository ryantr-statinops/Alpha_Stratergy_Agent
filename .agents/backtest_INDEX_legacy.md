# backtest/ — Local Backtest Engine

> **⚠️ ROUND 2 (ACTIVE) KHÔNG dùng local backtest.** Round 2 chạy backtest trực tiếp trên nền tảng
> XNOQuant qua `tools/submit_and_check.py` (simulate → fetch metrics). Toàn bộ engine này phục vụ
> **vòng 1 (VN30F futures intraday)** — đã archive, giữ làm reference.

## Overview

Local backtest engine for VN30F futures strategies. Reads template configs from `tools/generate_strategies.py`, fetches VN30F data via `vnstock`, runs vectorized strategy simulations, and exports performance metrics.

## Architecture

```
run.py  (orchestrator)
  ├── data/fetch_data.py          — fetch + cache VN30F 5m/daily data
  ├── regime.py                   — market regime detection + strategy filter
  ├── backtest.py                 — core strategy runner
  │   ├── exit_conditions.py      — ADX / momentum / volatility exit layers
  │   └── evaluate.py             — performance metrics (Sharpe, CAGR, MaxDD, ...)
  └── runners/
      ├── base.py                 — position computing helpers
      ├── thesis_01.py → 11.py    — strategy implementations
      └── thesis_12.py             — ❌ DEAD (Kalman Filter, not imported by run.py)
```

## Module Map

### Alive Modules

| File | Role | Imported By |
|------|------|-------------|
| `run.py` | Orchestrator — fetches data, iterates templates, runs backtest | CLI entry point |
| `backtest.py` | Core strategy runner — calls position func, exit layers, freeze protection | `run.py` |
| `evaluate.py` | Performance metrics (Sharpe, CAGR, MaxDD, Sortino, Calmar, PF, VaR, CVaR, Ulcer) | `backtest.py` |
| `exit_conditions.py` | 3-layer exit: ADX trend, momentum reversal, volatility explosion | `backtest.py` |
| `regime.py` | Market regime detection (ADX/NATR/ROC/ATR) + strategy filter | `run.py` |
| `data/fetch_data.py` | VN30F data pipeline: fetch, cache, resample | `run.py` |
| `features/__init__.py` | Feature module exports | All thesis runners |
| `features/ma.py` | Moving averages, rolling stats, linear regression | All thesis runners |
| `features/momentum.py` | ADX, RSI, ROC, MACD, Aroon, STOCH, CCI, DX, MFI | All thesis runners |
| `features/volatility.py` | ATR, NATR, Bollinger Bands, volatility | All thesis runners |
| `features/volume.py` | OBV, volume indicators | All thesis runners |
| `features/cycle.py` | HT_DCPERIOD, HT_DCPHASE, HT_SINE, HT_TRENDMODE | All thesis runners |
| `features/kalman.py` | Kalman filter helpers | `thesis_12.py` (dead) |
| `features/candles.py` | Candle pattern recognition | All thesis runners |
| `features/operators.py` | Cross detection, fillna, pct_change, rolling stats | All thesis runners |
| `runners/base.py` | Position computing helpers (vectorized, tiered) | All thesis runners |
| `runners/thesis_01.py` → `thesis_11.py` | Strategy implementations (T01 → T11) | `run.py` |

### Dead Modules (not imported by `run.py`)

| File | Reason | Action |
|------|--------|--------|
| `runners/thesis_12.py` | Kalman Filter strategies — not imported in `run.py` FUNC_MAP | Keep (reference) |
| `_quick_test.py` | Standalone proof-of-concept test | Keep (reference) |
| `_save_partial_5m.py` | One-time util to save partial 5m data | Keep (reference) |
| `data/_quick_fetch.py` | Dev test — quick fetch 2 contracts | Keep (reference) |
| `data/_check_cache.py` | Dev test — cache inspection | Keep (reference) |
| `data/_test_5m_chunked.py` | Dev test — chunked 5m fetch | Keep (reference) |
| `data/_test_contract_chunks.py` | Dev test — contract chunking | Keep (reference) |
| `data/_test_fetch.py` | Dev test — fetch validation | Keep (reference) |
| `data/_test_vnstock.py` | Dev test — vnstock API | Keep (reference) |
| `data/_test_vnstock2.py` | Dev test — vnstock API | Keep (reference) |
| `data/_test_vnstock3.py` | Dev test — vnstock API | Keep (reference) |
| `data/_test_vnstock4.py` | Dev test — vnstock API | Keep (reference) |

## Data Flow

```
run.py
  │
  ├── data/fetch_data.py
  │     └── fetch_5m() / fetch_daily() → resample() → data_cache
  │
  ├── regime.py
  │     └── detect_regime() → strategy_allowed() → filter
  │
  ├── runners/thesis_NN.py
  │     └── position_func(df, **params) → np.ndarray (positions)
  │
  ├── backtest.py
  │     ├── exit_conditions.py → compute_exit() + apply_freeze_protection()
  │     └── evaluate.py → metrics dict
  │
  └── results.csv
```

## Quick Reference

### Run Backtest
```bash
python backtest/run.py
```

### Add New Strategy
1. Create `backtest/runners/thesis_NN.py` with position functions
2. Import in `backtest/run.py` + add to `FUNC_MAP`
3. Add template config in `tools/generate_strategies.py` `TEMPLATES`

### Dependency Chain
```
run.py → fetch_data → detect_regime → strategy_allowed → thesis_NN.position_func → backtest.run_strategy → evaluate
```

### Dead Code Summary
12 files marked as dead — kept for reference, not imported by any live code path.
