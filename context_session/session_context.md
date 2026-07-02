# Context Session — Alpha Bot (New Strategy Cycle)

**Session Date:** 2026-07-03
**Purpose:** Fresh start — 6 new thesis groups designed, planning alpha docs completed
**Next Agent:** Read this first, then proceed to code generation

---

## 1. Project Status

| Item | Status |
|------|--------|
| `output/` | ✅ Cleared — 0 strategies |
| `tools/generate_strategies.py` | ✅ Cleared — ready to rewrite |
| `tools/validate_framework.py` | ✅ Cleared — ready to rewrite |
| `idea/planning_alpha/` | ✅ 7 new docs created (1 master + 6 thesis) |
| `context_session/` | ✅ Updated |

**Target:** Vietnam Quant Challenge 2026 — XNOQuant platform
**User tightened targets:** Sharpe ≥ 2.5 (min 2.0), CAGR > 20%, Max DD > -20%, PF > 1.3, Calmar > 1.1

---

## 2. Planning Documents Created

| File | Content |
|------|---------|
| `alpha_ideas_master_plan.md` | Tổng hợp 10 ý tưởng, mapping API, 6 thesis groups, Sharpe 7-component template, window sizing table |
| `thesis_01_rolling_mean_quantile.md` | 7 templates: Price vs Mean, Crossover, Mean+Confirm, Quantile Breakout, Mean+Quantile Channel, Z-Score Reversion, KAMA/MAMA |
| `thesis_02_volatility_regime.md` | 6 templates: Vol Breakout, Low Vol MeanRev, HMM Proxy (3-state), ATR Trailing, NATR Regime Switch, KAMA Adaptive |
| `thesis_03_time_series_decomposition.md` | 5 templates: Hilbert Trend+Sine, DCPeriod Adaptive, LinReg Slope, Sine Crossover, Dispersion Entropy Proxy |
| `thesis_04_microstructure_flow.md` | 7 templates: BOP+CMF, MFI Reversal, OI Cascade, Whale Footprint, AD Osc Divergence, OBV, Volume Imbalance |
| `thesis_05_cross_market_correlation.md` | 7 templates: Spread Z-score, VN30 Confirm, Basis Extreme, DJI Consensus, Rolling Correl, RS Ratio, Correlation Breakdown |
| `thesis_06_multifactor_composite.md` | 5 templates: 3-Factor Z, 4-Factor Z, Multi-Layer, Candlestick+Z, Regime-Weighted |

---

## 3. The 6 Thesis Groups

| # | Thesis | Core Ideas | Total Templates | Est. Variants | Timeframes |
|:-:|--------|-----------|:---------------:|:-------------:|:----------:|
| 01 | Rolling Mean + Quantile | Rolling Mean, Quantile | 7 | ~364 | 5, 15, 30, 60 |
| 02 | Volatility Regime | Vol Clustering, HMM proxy | 6 | ~84 | 5, 15, 30, 60 |
| 03 | Time-Series Decomposition | Hilbert Decomp, Entropy proxy | 5 | ~38 | 15, 30, 60 |
| 04 | Microstructure Flow | OBI, VPIN, Cascade | 7 | ~71 | 5, 15, 30 |
| 05 | Cross-Market Correlation | Correlation, Cointegration proxy | 7 | ~51 | 15, 30, 60 |
| 06 | Multi-Factor Composite | Z-score composite, Tiered sizing | 5 | ~69 | 15, 30, 60 |
| | **Total** | **10 ideas mapped** | **37 templates** | **~677 variants** | |

---

## 4. Workflow Status

```
Step 1: Alpha Generation    ✅ 6 thesis docs + master plan in idea/planning_alpha/
Step 2: Planning & Hypoth   ✅ 6 hypothesis docs in idea/hypothesis/
Step 3: User Review         ✅ Approved
Step 4: Chain-of-Thought    ✅ tools/generate_strategies.py
Step 5: Output              ✅ 1311 variants in output/
```

---

## 5. Results Summary

| Thesis | Variants | Templates | Timeframes |
|:------:|:--------:|:---------:|:----------:|
| 01 Rolling Mean + Quantile | 652 | T01-A through T01-G (7) | 5, 15, 30, 60 |
| 02 Volatility Regime | 272 | T02-A through T02-F (6) | 5, 15, 30, 60 |
| 03 Time-Series Decomposition | 66 | T03-A through T03-E (5) | 15, 30, 60 |
| 04 Microstructure Flow | 105 | T04-A through T04-G (7) | 5, 15, 30 |
| 05 Cross-Market Correlation | 90 | T05-A through T05-G (7) | 15, 30, 60 |
| 06 Multi-Factor Composite | 126 | T06-A through T06-E (5) | 15, 30, 60 |
| **Total** | **1311** | **37 templates / 239 param variants** | All TFs |

## 6. Tools Created

| Tool | Purpose | Status |
|------|---------|:------:|
| `tools/generate_strategies.py` | Generates all strategy variants from template definitions | ✅ |
| `tools/validate_framework.py` | Compliance: Exit→Long→Short, forbidden patterns, index consistency | ✅ |

Validation: **1311/1311 pass** — 0 errors, 0 warnings.

## 7. Next Steps

1. Upload `output/` folder to XNOQuant platform
2. Run batch simulation across all 1311 variants
3. Evaluate using scorecard: Sharpe ≥ 2.5, CAGR > 20%, Max DD > -20%, Calmar > 1.1
4. Select top variants per thesis group for optimization
5. Iterate on best-performing template(s) for final selection

---

## 6. Key Reference Data

### Multi-Timeframe Window Sizing
| TF | Fast | Mid | Slow | RSI | ADX | Vol | ReturnRoll | ReturnThresh | SessionCandles |
|:--:|:----:|:---:|:----:|:---:|:---:|:---:|:----------:|:-------------:|:--------------:|
| 5m | 8 | 14 | 20 | 7 | 7 | 14 | 3 | 0.0001 | 72 |
| 15m | 13 | 26 | 34 | 10 | 10 | 20 | 5 | 0.0002 | 24 |
| 30m | 20 | 40 | 50 | 14 | 14 | 26 | 8 | 0.0003 | 12 |
| 60m | 30 | 60 | 100 | 21 | 21 | 34 | 14 | 0.0005 | 6 |

### ADX Thresholds
| TF | ADX Entry | ADX Exit |
|:--:|:---------:|:--------:|
| 5m | 22 | 15 |
| 15m | 22 | 15 |
| 30m | 18 | 12 |
| 60m | 16 | 10 |

### Session Ranges (UTC)
- Lunch close: `04:30-06:00` — ALL theses
- Pre-ATC close: `07:20-07:45` — ALL theses
- Position open (thesis 07): `02:00-04:30, 06:00-07:45`

---

*End of Context Session — Ready for code generation phase.*
