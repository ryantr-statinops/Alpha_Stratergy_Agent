# AI Agent Onboarding Guide — Alpha Bot

> **Đọc file này đầu tiên khi bắt đầu phiên làm việc mới.**

---

## Reading Order

| # | File | Purpose |
|:-:|------|---------|
| 1 | `context_session/session_context.md` | Full project context: 805 strategies, 8 thesis groups, all data fields, rules |
| 2 | `README.md` | Project overview, 5-step workflow |
| 3 | `template_example/strategy_framework.md` | **Master spec** — class structure, multi-timeframe windows, VN30/DJI patterns, compliance checklist |
| 4 | `idea/hypothesis/hypothesis_framework.md` | Acceptance criteria: 10-metric weighted scorecard (Sharpe, CAGR, Sortino, Calmar, Max DD, VaR, CVaR, Ulcer, Cost, Correlation) |
| 5 | `data/VnFuture.md` | All data fields: OHLCV + futures + VN30 + DJI |
| 6 | `feature/feature_syntax.md` | 140+ indicators reference |
| 7 | `operations/operations_syntax.md` | 30+ operators reference |
| 8 | `idea/planning_alpha/alpha_generation_rolling_mean_quantile.md` | ~890 alpha variants (idea source) |

**Optimal order:** Read 1→2→3→4 first, then 5→6→7 on-demand when coding. Read 8 if more alpha ideas needed.

---

## Quick Reference

### Stack
- Platform: XNOQuant
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
| Timeframe | Fast | Mid | Slow | RSI | ADX | Vol |
|:---------:|:----:|:---:|:----:|:---:|:---:|:---:|
| 5min | 8 | 14 | 20 | 7 | 7 | 14 |
| 15min | 13 | 26 | 34 | 10 | 10 | 20 |
| 30min | 20 | 40 | 50 | 14 | 14 | 26 |
| 60min | 30 | 60 | 100 | 21 | 21 | 34 |

### Acceptance Criteria (10-metric weighted)
| Metric | Weight | Target |
|--------|:------:|--------|
| Sharpe Ratio | High | ≥ 1.2 |
| CAGR | High | ≥ 25% |
| Sortino Ratio | Medium | ≥ 1.5 |
| Calmar Ratio | Medium | ≥ 0.9 |
| Max Drawdown | High | ≥ -40% |
| Profit Factor | Medium | ≥ 1.7 |
| VaR (95%) | Medium | ≥ -5% |
| CVaR (95%) | Low | ≥ -6% |
| Ulcer Index | Low | ≤ 12 |
| Cost | Low | ≤ 1% |
| Correlation | Low | ≤ 0.8 |

PASS: ≥ 8.0/13pts **with** Sharpe, CAGR, Max DD must-pass.

### Output Structure
```
output/
├── index.csv                        # 805 strategies manifest
├── thesis_01_momentum/     .../5min/ .../15min/ .../30min/ .../60min/
├── thesis_02_trend/        ...
├── thesis_03_mean_reversion/
├── thesis_04_breakout/
├── thesis_05_cross_market/          # 15, 30, 60 only
├── thesis_06_volume_flow/           # 15, 30, 60 only
├── thesis_07_intraday_session/      # 5, 15 only
└── thesis_08_multifactor/           # 15, 30, 60 only
```

### Generator
`python tools/generate_strategies.py` — 35+ templates, parameter-grid variants, timeframe-aware.
