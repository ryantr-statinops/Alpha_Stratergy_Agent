# Alpha Ideas Master Plan — Complete API Mapping & Strategy Design

> **Session:** 2026-07-03 — Fresh start, 6 new thesis groups
> **Platform:** XNOQuant — `CustomStrategy(SimpleAlgorithm)`
> **Core Reference:** `feature/feature_syntax.md` (140+ functions), `operations/operations_syntax.md` (30+ operators), `data/vietnam_market_characteristics.md`, `template_example/strategy_framework.md`
> **Target:** Vietnam Quant Challenge 2026 — Sharpe ≥ 2.5, CAGR > 20%, Max DD > -20%

---

## 1. Project State

| Item | Status |
|------|--------|
| `output/` | Cleared — 0 strategies |
| `tools/` | Cleared — no generator/validator yet |
| `idea/planning_alpha/` | 6 new thesis design docs added |
| Ready for implementation | Yes |

---

## 2. Ideas → API Mapping Summary

| # | Idea | Platform Support | Core API | Proxy Strategy |
|---|------|:----------------:|----------|----------------|
| 1 | **Rolling Mean** | ✅ Full | `rolling_mean`, `sma`, `ema`, `kama`, `mama`, `wma`, `dema`, `tema`, `t3`, `trima` | Direct |
| 2 | **Quantile** | ✅ Full | `rolling_quantile`, `rolling_rank`, `rolling_percentile_rank`, `rolling_zscore` | Direct |
| 3 | **Volatility Clustering** | ⚠️ Proxy | `rolling_std`, `var`, `atr`, `natr`, `trange` | rolling_std regime detection |
| 4 | **Time-Series Decomposition** | ⚠️ Proxy | `ht_trendline`, `dcperiod`, `trendmode`, `sine`, `linearreg_slope`, `tsf` | Hilbert decomp: trend = ht_trendline, cycle = close - trend |
| 5 | **OBI & VPIN** | ⚠️ Proxy | `bop`, `cmf`, `ad`, `adosc`, `mfi`, `fut_matched_*`, `fut_open_interest` | BOP/CMF cho OBI; volume + OI imbalance |
| 6 | **HMM** | ❌ Proxy | `adx`, `trendmode`, `atr`, `kama`, `mama` | ADX + vol regime classification (3-state) |
| 7 | **Hurst Exponent** | ❌ None | — | Không implement được |
| 8 | **Entropy / Info Theory** | ❌ Proxy | `rolling_mad`, `rolling_percentile_rank`, `rolling_std` | rolling_mad/std ratio for disorder |
| 9 | **Cointegration** | ⚠️ Proxy | `correl`, `beta`, `rolling_correlation`, `rolling_covariance`, `linearreg_intercept` | Spread = close - beta*VN30; trade z-score |
| 10 | **Correlation** | ✅ Full | `correl`, `rolling_correlation`, `beta`, `rolling_covariance` | Direct |

---

## 3. The 6 New Thesis Groups

| Thesis | Core Ideas | Data Fields | Timeframes |
|--------|-----------|-------------|:----------:|
| **T01: Rolling Mean + Quantile** | Rolling Mean, Quantile | `pv_close`, `pv_volume`, `fut_*` | 5, 15, 30, 60 |
| **T02: Volatility Regime** | Volatility Clustering, HMM proxy | `pv_close`, `pv_high`, `pv_low` | 5, 15, 30, 60 |
| **T03: Time-Series Decomposition** | Time-Series Decomp, Entropy proxy | `pv_close` | 15, 30, 60 |
| **T04: Microstructure Flow** | OBI, VPIN proxy | `pv_close`, `pv_volume`, `fut_matched_*`, `fut_open_interest` | 5, 15, 30 |
| **T05: Cross-Market Correlation** | Correlation, Cointegration proxy | `pv_close`, `pv_vn30_*`, `pv_dji_*` | 15, 30, 60 |
| **T06: Multi-Factor Composite** | Tất cả ideas | All fields | 15, 30, 60 |

---

## 4. VN Market → Strategy Mapping

| VN Characteristic | Thesis Applied | Mechanism |
|-------------------|---------------|-----------|
| Retail 80-90%, FOMO/panic | T01 Quantile, T04 Microstructure | Q90/Q10 extremes detect overreaction; BOP/CMF detect buying/selling pressure |
| Margin call 1:6-1:8 cascade | T04 Microstructure, T02 Volatility | OI drop + volume spike xác nhận cascade; rolling_std phát hiện vol regime |
| Basis volatility futures-cash | T05 Cross-Market | Spread z-score trade basis reversion |
| Session microstructure (lunch, ATC) | Tất cả | Session gating: close lunch (04:30-06:00 UTC), close trước ATC (07:20) |
| Trend kéo dài 2-3 phiên | T01 Rolling Mean, T02 Volatility | KAMA/MAMA tự thích ứng; ADX regime filter |
| No circuit breaker | T02 Volatility | Trend momentum mạnh; rolling_std cảnh báo vol spike |
| Retail dominated news-driven | T03 Decomposition | trendmode phân biệt trend vs cycle; sine/leadsine detect turning points |
| Global spillover (DJI) | T05 Cross-Market | correl(VN30F1M, DJI) + consensus trading |

---

## 5. Sharpe 7-Component Template (Universal)

```python
return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
return_roll = self.feat.rolling_mean(return_1, window=return_window)
adx = self.feat.adx(high, low, close, timeperiod=adx_window)
vol_sma = self.feat.sma(volume, timeperiod=vol_window)

# Entry
long_setup = (core_signal_long)
           & (return_roll > 0)                    # 2. Momentum confirm
           & (adx > adx_entry_threshold)           # 1. ADX noise filter
           & (volume > vol_sma)                   # 3. Volume confirm
           & (abs(return_1) > min_roc_threshold)  # 4. Whipsaw guard

# Exit
exit_setup = (core_exit_long)
           | self.op.crossed_below(abs(return_roll), return_threshold)  # 5. Asymmetric
           | self.op.crossed_below(adx, adx_exit_threshold)            # 5. Trend faded
           | trailing_long_exit | trailing_short_exit                   # Chandelier stop

# 6. Session gating — built via class attrs
position_close_after_n_candles = SESSION_CANDLES[tf]
position_close_ranges = LUNCH_CLOSE_RANGES + ["07:20-07:45"]  # UTC

# 7. Consecutive loss protection
recent_exit = self.feat.rolling_max(exit_setup, window=cooldown_period)
long_setup = long_setup & (recent_exit < 1)
short_setup = short_setup & (recent_exit < 1)
```

---

## 6. Multi-Timeframe Window Sizing

| TF | Fast | Mid | Slow | RSI | ADX | Vol | ReturnRoll | ReturnThresh | SessionCandles | ChandelierW | ChandelierM | Cooldown |
|:--:|:----:|:---:|:----:|:---:|:---:|:---:|:----------:|:-------------:|:--------------:|:-----------:|:-----------:|:--------:|
| 5m | 8 | 14 | 20 | 7 | 7 | 14 | 3 | 0.0001 | 72 | 6 | 2.0 | 3 |
| 15m | 13 | 26 | 34 | 10 | 10 | 20 | 5 | 0.0002 | 24 | 5 | 2.0 | 2 |
| 30m | 20 | 40 | 50 | 14 | 14 | 26 | 8 | 0.0003 | 12 | 4 | 2.5 | 2 |
| 60m | 30 | 60 | 100 | 21 | 21 | 34 | 14 | 0.0005 | 6 | 3 | 3.0 | 1 |

### ADX Thresholds by TF

| TF | ADX Entry | ADX Exit |
|:--:|:---------:|:--------:|
| 5m | 22 | 15 |
| 15m | 22 | 15 |
| 30m | 18 | 12 |
| 60m | 16 | 10 |

### Session Ranges (UTC)

| Range | Purpose |
|-------|---------|
| `04:30-06:00` | Lunch close (VN 11:30-13:00) — ALL theses |
| `07:20-07:45` | Pre-ATC close — ALL theses |
| `02:00-04:30, 06:00-07:45` | Position open — THESIS 07 only |

---

## 7. Acceptance Criteria (10-metric weighted)

| Metric | Weight | Target | Must-pass |
|--------|:------:|--------|:---------:|
| Sharpe Ratio | High | ≥ 2.5 (user) / ≥ 2.0 (min) | ✅ |
| CAGR | High | > 20% | ✅ |
| Max Drawdown | High | > -20% | ✅ |
| Sortino Ratio | Medium | ≥ 1.5 | |
| Calmar Ratio | Medium | ≥ 1.1 | |
| Profit Factor | Medium | ≥ 1.3 | |
| VaR (95%) | Medium | ≥ -5% | |
| CVaR (95%) | Low | ≥ -6% | |
| Ulcer Index | Low | ≤ 12 | |
| Cost | Low | ≤ 1% | |
| Correlation | Low | ≤ 0.8 | |

**PASS:** ≥ 8.0/13pts với Sharpe, CAGR, Max DD must-pass.

---

## 8. Document Tree

```
idea/planning_alpha/
├── alpha_ideas_master_plan.md              ← THIS FILE
├── thesis_01_rolling_mean_quantile.md      # Rolling Mean + Quantile
├── thesis_02_volatility_regime.md          # Volatility Clustering + HMM proxy
├── thesis_03_time_series_decomposition.md  # Time-Series Decomp + Entropy proxy
├── thesis_04_microstructure_flow.md        # OBI + VPIN proxy
├── thesis_05_cross_market_correlation.md   # Correlation + Cointegration proxy
├── thesis_06_multifactor_composite.md      # Multi-Factor Composite
├── alpha_5_new_ideas_cascade_basis_lunch_whale_exhaustion.md  # Legacy
├── alpha_generation_rolling_mean_quantile.md                   # Legacy ~890 ref
├── strategy_001_mean_quantile_rsi.md                           # Legacy sample
├── enhancement_return_roll_tiered_session.md                   # Legacy
├── scaling_proposal_500_10000_strategies.md                    # Legacy
└── backtest_plan.md                                            # Legacy
```

---

## 9. Implementation Roadmap

```
Phase 1: Design (current)
├── Master plan + 6 thesis docs  →  ✅ Done
└── User review                  →  ⬜ Pending

Phase 2: Code Generation
├── Write tools/generate_strategies.py  →  ⬜ Pending
├── Write tools/validate_framework.py   →  ⬜ Pending
└── Generate strategies → output/       →  ⬜ Pending

Phase 3: Backtest
├── Upload to XNOQuant          →  ⬜ Pending
├── Simulate all strategies     →  ⬜ Pending
└── Scorecard by thesis group   →  ⬜ Pending

Phase 4: Optimize
├── Analyze Sharpe < target     →  ⬜ Pending
├── Tune parameters             →  ⬜ Pending
└── Iterate                     →  ⬜ Pending
```

---

*End of Master Plan — Ready for thesis-by-thesis deep dive.*
