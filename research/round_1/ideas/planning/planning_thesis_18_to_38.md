# Alpha Ideas Master Plan — Thesis 18 → 38 (21 New Alpha Groups)

> **Session:** 2026-07-12
> **Platform:** XNOQuant — `CustomStrategy(SimpleAlgorithm)`
> **Core Reference:** `syntax/data_syntax.md`, `syntax/feature_syntax.md`, `syntax/operations_syntax.md`, `template_example/strategy_framework.md`
> **Mode:** Brainstorm → Design → Generate → Backtest → Iterate

---

## 1. Current Project State

| Item | Status |
|------|:------:|
| Thesis 01–06 | ✅ Implemented (old phase) |
| Thesis 07–10 | ✅ Implemented |
| Thesis 11 (VWAP Basis) | ✅ Implemented |
| Thesis 12 (Kalman Filter) | ✅ Implemented |
| Thesis 13 (CMF + Squeeze) | ✅ Implemented |
| Thesis 14 (BB Squeeze Reversal) | ✅ Implemented (A + C) |
| Thesis 15 (MAVP Adaptive) | ✅ Implemented (A + B + C) |
| Thesis 16 (Price-Vol Velocity) | ✅ Implemented |
| Thesis 17 (Vol-Adj Momentum) | ✅ Implemented (A + B + C) |
| **Thesis 18–38 (New)** | **⬜ Planning Phase** |

---

## 2. Origin — 20 Viable Alpha Ideas

Generated from brainstorming session + `syntax/feature_syntax.md` analysis.
All ideas verified for: **cú pháp khả thi**, **chưa trùng thesis hiện có**, **phù hợp 15m/30m**.

### Nhóm A — Price Position (scale 0-1)
| # | Idea | Feature | Entry Logic |
|---|------|---------|-------------|
| 1 | **Range Rank** | `rolling_rank(close, 100)` | rank > 0.95 = overbought short; rank < 0.05 = oversold long |
| 2 | **Distance to BB** | `(close - bb_lower) / (bb_upper - bb_lower)` | > 0.95 = upper band touch (short); < 0.05 = lower band touch (long) |
| 3 | **MinMax Scaling** | `(close - min(200)) / (max(200) - min(200))` | > 0.95 = multi-session high; < 0.05 = multi-session low |

### Nhóm B — Momentum Dynamics
| # | Idea | Feature | Entry Logic |
|---|------|---------|-------------|
| 4 | **Momentum Decay** | `linearreg_slope(rolling_mean(close, 20), 5)` | slope giảm dần = trend exhaustion → đảo chiều |
| 5 | **Return Mean** | `rolling_mean(returns(close), 20)` | > 0.001 = positive drift (long); < -0.001 = negative drift (short) |
| 6 | **MACD Hist Divergence** | `linearreg_slope(macd_hist, 5)` | hist_slope giảm khi giá tăng = bearish divergence |

### Nhóm C — Volume/Flow
| # | Idea | Feature | Entry Logic |
|---|------|---------|-------------|
| 7 | **Volume-Price Divergence** | `obv` + `rolling_max/min(close)` | price新高但OBV新低 = distribution → short |
| 8 | **Price-Volume Correlation** | `rolling_correlation(close, volume, 20)` | corr < -0.5 = divergence regime (reversal bias) |
| 9 | **CMF Quantile Threshold** | `rolling_quantile(cmf, 100)` | cmf_rank > 0.9 = accumulation → long; < 0.1 = distribution → short |

### Nhóm D — Volatility/Regime
| # | Idea | Feature | Entry Logic |
|---|------|---------|-------------|
| 10 | **Log-Return Vol Filter** | `rolling_std(log_returns(close), 20)` | vol < percentile(20) = flat market → skip trade |
| 11 | **BB Width Squeeze** | `rolling_quantile(bb_width, 100, 0.1)` | bb_width < quantile(10) = squeeze → prepare breakout |
| 12 | **Vol-of-Vol (ATR Var)** | `rolling_std(atr(14), 20)` | vol_of_vol thấp = stable regime; cao = chaotic |
| 13 | **ADX Acceleration** | `linearreg_slope(adx(14), 5)` | adx_slope tăng = trend starting; slope giảm = trend fading |

### Nhóm E — Enhanced Mean Reversion
| # | Idea | Feature | Entry Logic |
|---|------|---------|-------------|
| 14 | **RSI Quantile MR** | `rolling_quantile(rsi(14), 100)` | rsi_rank < 0.1 = oversold (long); > 0.9 = overbought (short) |
| 15 | **Cointegration Spread** | `rolling_zscore(pv_close - pv_vn30_close, 60)` | z < -2 = cheap future → long; z > 2 = expensive → short |
| 16 | **VWAP Deviation** | `close / rolling_vwap(20) - 1` | > 0.02 = overextended long → short; < -0.02 = undersold → long |
| 17 | **Rolling Sharpe Gate** | `rolling_mean(ret, 20) / rolling_std(ret, 20)` | sharpe > 0.5 = strategy in positive regime → allow trade |

### Nhóm F — Pattern & Composite
| # | Idea | Feature | Entry Logic |
|---|------|---------|-------------|
| 18 | **Candle Body Ratio** | `body = abs(close - open)`; `range = high - low` | body/range > 0.7 = strong candle (momentum); < 0.3 = weak |
| 19 | **Regression Channel** | `linearreg(close, 50) ± 2*rolling_std(close, 50)` | outside channel = extreme → reversal |
| 20 | **Standardized Return Quantile** | `rolling_zscore(returns(close), 20) → rolling_quantile` | combined: return_z_rank extremes |

### Nhóm G — Macro Regime (daily data)
| # | Idea | Feature | Entry Logic |
|---|------|---------|-------------|
| 21 | **Interbank Filter** | `vn_interbank_interest_rate_1w_daily` | rate thấp = loose liquidity → risk-on bias |
| 22 | **USD/VND Risk Filter** | `vn_usd_vnd_sbv_central_daily` | VND ổn định → normal; VND biến động > 1% → risk-off |

---

## 3. Thesis 18→38 — Mapping

| Thesis | Core Idea | Templates | Ideas Used | Timeframes |
|:------:|-----------|:---------:|:----------:|:----------:|
| **18** | Range Rank Breakout | A: Rank only / B: Rank + Vol | #1 | 15, 30 |
| **19** | BB Relative Position | A: BB Distance / B: BB + ADX / C: BB + Vol | #2 | 15, 30, 60 |
| **20** | MinMax Position Scaling | A: MinMax entry / B: MinMax + Trend | #3 | 15, 30, 60 |
| **21** | Momentum Decay Reversal | A: Slope decay / B: Decay + Divergence | #4 | 15, 30 |
| **22** | Return Mean Drift | A: RetMean cross / B: RetMean + ADX | #5 | 15, 30 |
| **23** | MACD Histogram Divergence | A: Hist slope / B: Hist + Price cross | #6 | 15, 30, 60 |
| **24** | Volume-Price Divergence | A: OBV divergence / B: VPD + ATR | #7 | 15, 30 |
| **25** | Price-Volume Correlation | A: Corr filter / B: Corr + Regime | #8 | 15, 30, 60 |
| **26** | CMF Quantile Threshold | A: CMF rank / B: CMF + RSI | #9 | 15, 30 |
| **27** | Log-Return Vol Filter | A: Vol gate / B: Vol-adaptive sizing | #10 | 15, 30 |
| **28** | BB Width Squeeze | A: Squeeze detect / B: Squeeze + breakout | #11 | 15, 30, 60 |
| **29** | Vol-of-Vol (ATR Var) | A: Low vol regime / B: Vol breakout | #12 | 15, 30 |
| **30** | ADX Acceleration | A: ADX slope / B: ADX + DI confirm | #13 | 15, 30, 60 |
| **31** | RSI Quantile Mean Reversion | A: RSI rank / B: RSI + Vol confirm | #14 | 15, 30 |
| **32** | Cointegration Spread MR | A: Spread z-score / B: Spread + ADX | #15 | 15, 30, 60 |
| **33** | Regression Channel | A: Channel breakout / B: Channel + BB | #19 | 15, 30, 60 |
| **34** | VWAP Deviation | A: VWAP% entry / B: VWAP + Volume | #16 | 15, 30 |
| **35** | Rolling Sharpe Gate | A: Sharpe filter / B: Sharpe + Mom | #17 | 15, 30, 60 |
| **36** | Candle Body Ratio | A: Strong candle / B: Candle + Filter | #18 | 15, 30 |
| **37** | Standardized Return Quantile | A: RetZ rank / B: RetZ + Volume | #20 | 15, 30 |
| **38** | Macro Regime Context | A: Interbank / B: USDVND / C: Composite | #21, #22 | 15, 30 |

**Total: 21 Thesis × ~2.3 templates = ~49 templates**

---

## 4. Template Design Principles

### 4.1 Universal Exit Structure
```python
exit_long = atr_stop_long | trailing_long
exit_short = atr_stop_short | trailing_short
```
Áp dụng cho ALL templates (đã chứng minh hiệu quả qua T14-C).

### 4.2 Pipeline Order (bắt buộc)
```python
assert not (long_signal & short_signal).any()
self.set_positions(exit_setup, position=0)
self.set_positions(long_signal, position=1)
self.set_positions(short_signal, position=-1)
```

### 4.3 Core Feature — Chỉ 1 feature làm entry signal
Mỗi template có **đúng 1 core feature** quyết định entry. Các feature khác chỉ làm confirmation gate.

### 4.4 Fixed Params Convention

| Group | Default Windows | Notes |
|-------|-----------------|-------|
| Position | 100–200 | rolling_rank, minmax |
| Momentum | 14–20 | roc, returns, linearreg |
| Volume | 20 | vol_sma |
| Volatility | 14 | atr, adx |
| BBands | 20, 2 | bb_window, nbdev |
| Exit | — | atr_mult=2.0, trailing_span=10 |

---

## 5. Timeframes per Thesis

| TF | Which Theses | Rationale |
|:--:|:-------------|:----------|
| **15m** | ALL (18–38) | Primary — quick signal generation |
| **30m** | ALL (18–38) | Secondary — confirm or alternative |
| **60m** | 19, 20, 23, 25, 28, 30, 32, 33, 35 | Slower ideal for position/volatility/correlation theses |

---

## 6. Data Dependencies

| Data Field | Used By Theses |
|------------|:--------------|
| `pv_close`, `pv_high`, `pv_low` | ALL |
| `pv_volume` | 19, 20, 24, 25, 26, 31, 34, 36, 37 |
| `pv_open` | 36 (candle body) |
| `pv_vn30_close` | 32 (cointegration spread) |
| `pv_dji_close` | 38 (optional macro context) |
| `vn_interbank_interest_rate_1w_daily` | 38 |
| `vn_usd_vnd_sbv_central_daily` | 38 |

---

## 7. Implementation Roadmap

```
Phase 1: Plan (current)
├── Master plan                →  ✅ Done
├── Hypothesis files (18→38)   →  ⬜ Pending
└── User review                →  ⬜ Pending

Phase 2: Code Generation
├── Add T18→38 codes to generate_strategies.py  →  ⬜ Pending
├── Update TEMPLATE_META                        →  ⬜ Pending
└── Regenerate output/                          →  ⬜ Pending

Phase 3: Backtest & Validate
├── Upload to XNOQuant            →  ⬜ Pending
├── Simulate ~49 templates        →  ⬜ Pending
└── Scorecard ranking             →  ⬜ Pending

Phase 4: Iterate
├── Keep top 30% per thesis       →  ⬜ Pending
├── Tune parameters               →  ⬜ Pending
└── Drop bottom 30%               →  ⬜ Pending
```

---

## 8. Success Criteria

| Metric | Target | Must-pass |
|--------|--------|:---------:|
| Sharpe Ratio | ≥ 1.3 | ✅ |
| CAGR | ≥ 15% | ✅ |
| Max Drawdown | > -35% | ✅ |
| Profit Factor | ≥ 1.2 | |
| Calmar Ratio | ≥ 1.1 | |
| Correlation to existing theses | ≤ 0.7 | |

---

*End of Master Plan — Ready for hypothesis design.*
