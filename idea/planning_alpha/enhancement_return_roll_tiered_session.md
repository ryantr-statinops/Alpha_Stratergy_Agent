# Planning — 3 Core Enhancements: Return Roll, Tiered Sizing, Session Gating

**Target:** All 805 strategies across 8 thesis groups  
**Current State:** Missing momentum smoothing, tiered sizing, and time-based constraints  
**Status:** Planning

---

## 1. Enhancement A: Return Roll (Momentum Smoothing Filter)

### Motivation

5/9 example files use `return_roll` to smooth short-term momentum and filter noisy signals:

```python
return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
return_roll = self.feat.rolling_mean(return_1, window=N)
```

Without this, entry signals fire on single-bar noise (e.g., price ticks above a threshold then reverses).

### Implementation

Add `return_roll` as a **universal filter** applied to all templates:

- **Entry:** `long_setup &= (return_roll > 0)` and `short_setup &= (return_roll < 0)`  
  (i.e., require recent momentum to agree with direction)
- **Exit:** Optional weak-momentum exit: `exit_setup |= (abs(return_roll) < threshold)`

### Parameter Grid

| Timeframe | return_roll window (N) | Flat threshold |
|:---------:|:----------------------:|:--------------:|
| 5 min | 3 | 1e-4 |
| 15 min | 5 | 2e-4 |
| 30 min | 8 | 3e-4 |
| 60 min | 14 | 5e-4 |

Trade-off: Smaller N = faster response, more noise. Larger N = smoother, slower.

### Templates Affected

All ~35 templates, adding `return_window` class attribute + 4 lines of feature engineering.

---

## 2. Enhancement B: Tiered Position Sizing

### Motivation

Example files (`VNFutureTieredTrendSizing`, `VNFutureTimedCloseMomentum`) use weak/strong tiers:

```python
strong_long = (entry_conditions) & (adx > 22) & (volume > base) & (return_1 > 0)
weak_long   = (entry_conditions) & (adx > 18) & (return_1 > 0)

self.set_positions(weak_long,   position=0.5)
self.set_positions(strong_long, position=1)
```

Current strategies only have single ±1.0 sizing — no differentiation between weak/strong signals.

### Implementation

Split each entry into 2 tiers:
- **Strong entry:** Requires ALL conditions + ADX > 22 + volume confirmation + return_roll > 0  
  → position = 1.0 (long) / -1.0 (short)
- **Weak entry:** Core conditions + ADX > 18 + return_roll > 0 (no volume)  
  → position = 0.5 (long) / -0.5 (short)

Exit remains the same: flat first, then weak fills, then strong overwrites.

### Position Values

| Tier | Long | Short |
|------|:----:|:-----:|
| Strong | 1.0 | -1.0 |
| Weak | 0.5 | -0.5 |

### Templates Affected

All templates that have volume/ADX data available. Templates without ADX/volume (e.g., `momentum_pure`) use single tier.

---

## 3. Enhancement C: Session & Time Constraints

### Motivation

Example files use:
- `position_close_after_n_candles = 24` — max hold time
- `position_close_ranges = ["04:20-04:30", "07:30-07:45"]` — forced flat windows
- `position_open_ranges = ["02:00-04:30", "06:00-07:45"]` — allowed trading windows

Current strategies have **no time/session constraints** — risk holding through low-liquidity periods.

### Implementation

Add to ALL templates:
```python
position_close_after_n_candles = MAX_CANDLES  # timeframe-dependent
```

Optionally for thesis 07 (Intraday Session):
```python
position_open_ranges = ["02:00-04:30", "06:00-07:45"]  # UTC (VN morning + afternoon)
position_close_ranges = ["04:20-04:30", "07:30-07:45"]  # UTC (lunch + end)
```

### Max Hold Candles by Timeframe

| Timeframe | Max candles | Real time |
|:---------:|:-----------:|:---------:|
| 5 min | 24 | 2 hours |
| 15 min | 16 | 4 hours |
| 30 min | 8 | 4 hours |
| 60 min | 6 | 6 hours |

---

## 4. Dependency Matrix

| Thesis Group | return_roll | Tiered Sizing | Session Constraints |
|-------------|:-----------:|:-------------:|:-------------------:|
| 01 Momentum | ✓ | Only w/ ADX/vol | ✓ candles |
| 02 Trend | ✓ | ✓ (has ADX+vol) | ✓ candles |
| 03 Mean Reversion | ✓ | ✓ (has vol/R) | ✓ candles |
| 04 Breakout | ✓ | ✓ (has vol) | ✓ candles |
| 05 Cross-Market | ✓ | Partial (no vol) | ✓ candles |
| 06 Volume & Flow | ✓ | Partial | ✓ candles |
| 07 Intraday Session | ✓ | ✓ | ✓ ranges + candles |
| 08 Multi-Factor | ✓ | ✓ | ✓ candles |

---

## 5. Current Baseline Metrics (Expected)

| Metric | Baseline (no filter) | With return_roll | With tiered + session |
|--------|:-------------------:|:----------------:|:--------------------:|
| Sharpe Ratio | ~0.6-0.8 | ~0.8-1.0 | ~1.0-1.2 |
| Win Rate | ~50% | ~52-55% | ~55-58% |
| Max Drawdown | ~-35% | ~-25% | ~-20% |
| Trades/month | 40-60 | 25-40 | 20-35 |

*Note: Estimates based on template examples. Actual metrics require backtest.*

---

## 6. Priority Order

1. **return_roll filter** — simplest, highest impact, affects all strategies
2. **Tiered sizing** — medium complexity, affects ~25/35 templates
3. **Session constraints** — low complexity, affects all (candles) + thesis 07 (ranges)

---

## 7. Next Steps

- [ ] User Review (Bước 3)
- [ ] Update generator: add return_roll to all templates
- [ ] Update generator: add tiered sizing templates
- [ ] Update generator: add position_close_after_n_candles
- [ ] Update generator: add session ranges for thesis 07
- [ ] Regenerate 805+ strategies
- [ ] Hypothesis testing loop (Bước 2b)
