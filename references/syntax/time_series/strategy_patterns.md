# Time-Series Strategy Patterns

This document contains construction patterns for one execution mode. It is not performance evidence. Exact fields, parameters, masks, and trial budgets must be preregistered and validated. Shared data comes from [`../data_syntax.md`](../data_syntax.md).

## 2. Time-Series Quality and Trend

Use a persistent fundamental state to define quality and price trend to define timing.

```python
class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual
        total_assets = self.data.fun_bs_total_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)

        known = self.op.notna(net_profit) & self.op.notna(total_assets)
        valid = known & (total_assets > 0)
        roa = net_profit / total_assets
        quality = valid & (net_profit > 0) & (roa > 0.01)

        weak_long = quality & (close > ema_slow)
        strong_long = weak_long & (ema_fast > ema_slow)
        exit_setup = (close < ema_slow) | (valid & (roa < 0))

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
```

Rules:

- Quality is persistent; trend controls timing.
- Exit uses slow regime failure or genuine quality failure.
- Do not exit on a noisy one-day confirmation unless the thesis is event-driven.
- Entry and exit should normally be mutually exclusive.

## 3. Time-Series Report-Event Overlay

A fundamental change is an event, not a continuously refreshed state.

```python
profit = self.data.fun_is_net_profit_loss_after_tax_quarterly
assets = self.data.fun_bs_total_assets_quarterly
close = self.data.pv_close

known = self.op.notna(profit) & self.op.notna(assets) & (assets > 0)
profit_change = self.op.pct_change(profit, periods=1)
report_known = known & self.op.notna(profit_change)
report_event = report_known & (profit > 0) & (profit_change > 0)
```

Use the event as an overlay or trigger. Keep a separate persistent state if the position is intended to survive between reports. For negative/sign-changing profit, prefer an asset-scaled delta when supported by the operator contract.

## 7. Noise Filtering

Filter noise so a single noisy bar does not open or close a position. Compose from existing
`self.op` + `self.feat` only; no `noise_*` operator is assumed.

```python
close = self.data.pv_close
fast = self.feat.ema(close, timeperiod=12)
slow = self.feat.ema(close, timeperiod=36)

# Mask unavailable / non-finite bars, and smooth price causally (not fundamentals).
known = self.op.notna(close) & self.op.isfinite(close)
smooth = self.op.ffill(close)

# Require persistence so a one-bar flicker does not trade.
cross_up = self.op.crossed_above(fast, slow)
up_trend = self.op.rising(close, 3)
confirmed = cross_up & up_trend
entry = known & self.op.hold_for(confirmed, 2)

# Dead-band / hysteresis via native arithmetic to ignore noise around the slow EMA.
band = slow * 1.02
strong_up = known & self.op.between(close, band, float("inf"))
```

Rules:

- A filter is an eligibility/state guard, not an alpha signal on its own.
- Prefer confirmation (`hold_for`, `consecutive_true`, `rising`, `falling`) over adding gates.
- Use a dead-band with native `*`/comparison; never `fillna` a fundamental to hide missing
  as zero.
- Keep every filter causal: forward-only fills and positive lookbacks.

## 8. Breakout Pattern

A breakout feature must have verified current-bar semantics.

```python
close = self.data.pv_close
high = self.data.pv_high
cfo = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual

breakout_level = self.feat.donchian_upper(high, timeperiod=20)
known = self.op.notna(cfo)
quality = known & (cfo > 0)
entry = quality & (close > breakout_level)
```

Do not use the pattern until it is known whether the current bar is included in the breakout level. Use a slow trend/quality exit rather than adding unrelated conditions to rescue backtest performance.

## 9. Ablation Pattern

Every composite starts from a baseline:

```text
B0: price/trend baseline
B1: B0 + one fundamental quality component
B2: B1 + one liquidity eligibility layer
B3: B2 + one sizing or event overlay
```

Change one dimension per step. Record each variant, including failures. Do not optimize field, horizon, threshold, sizing, and exit simultaneously.

## 10. Anti-Patterns

### Raw monetary rank

```python
# INVALID research design: mostly ranks company size
signal = self.data.fun_is_net_profit_loss_after_tax_annual_panel
```

### Missing-to-zero eligibility

```python
# INVALID
profit = self.op.fillna(profit, value=0)
```

### Kitchen-sink entry

```python
# FRAGILE: too many unrelated hard gates
entry = quality & value & momentum & low_vol & low_leverage & volume & breakout
```

### Repeated factor amplification

```python
# FRAGILE unless preregistered and robust as a family
signal = value * trend * trend * trend * trend
```

### Test-driven repair

```text
Test fails -> add another condition -> rerun same test -> call it OOS
```

Once test results influence a change, that test is development data. See `validation_protocol.md`.

### One-bar whipsaw trigger

```python
# FRAGILE: a single noisy bar opens a position
entry = crossed_above(fast, slow)  # just a flicker, no persistence
```

Confirm before trading: `hold_for` / `consecutive_true` / `rising` / `falling`, or a dead-band.

## 11. Pattern Promotion Checklist

- [ ] Thesis selects the mode before testing.
- [ ] Field names and shapes are valid.
- [ ] Fundamental semantics follow `fundamental_data_contract.md`.
- [ ] Panel defaults/evidence follow `panel_feature_contract.md`.
- [ ] Baseline exists.
- [ ] Each ablation changes one component.
- [ ] Entry has no more than four primary economic conditions.
- [ ] Strong entry adds no more than two confirmations.
- [ ] Confirm the signal before entry (noise filter) and record the chosen filter as a variant.
- [ ] Exit has no more than three OR branches.
- [ ] Cross-sectional coverage and concentration are audited.
- [ ] All variants are tracked as one family.
- [ ] Final selection follows `validation_protocol.md`.
