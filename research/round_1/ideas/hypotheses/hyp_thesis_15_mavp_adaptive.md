# Hypothesis — Thesis 15: MAVP Adaptive Momentum

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 15 — MAVP Adaptive Momentum |
| Core Idea | Replace fixed SMA with `mavp(close, periods=dcperiod)` — adaptive moving average that tracks market cycle. Entry when price crosses adaptive MA with volume + ADX confirmation. Exit via event-only ADX fade + ATR stop + trailing. |
| Data Fields | `pv_close`, `pv_high`, `pv_low`, `pv_volume` |
| Timeframes | 15, 30, 60 min |
| Templates | T15-mavp (Core), T15-mavp_B (Adaptive BBands), T15-mavp_C (TrendMode Gatekeeper) |
| Est. Variants | ~9 (3 TFs x 3 params) |
| Status | TODO |

---

## HYP-MAV-01: MAVP Adaptive Trend (T15-mavp)

**Logic:**
```python
dc_period = self.op.fillna(self.feat.dcperiod(close), 20)
dc_clipped = self.feat.rolling_max(dc_period, 5)  # smooth dcperiod
mavp_ma = self.feat.mavp(close, periods=dc_clipped, minperiod=8, maxperiod=30, matype=0)
entry: close > mavp_ma & adx > 22 & volume > vol_sma & return_roll > 0
exit: crossed_below_value(adx, 18) | atr_stop_short | trailing_short
```

## HYP-MAVP-02: Adaptive Bollinger Bands (T15-mavp_B)

Dùng `mavp` làm mid band cho BBands. Upper/lower band tự động co giãn theo cycle.

## HYP-MAVP-03: TrendMode Gate (T15-mavp_C)

Thêm `trendmode == 1` vào entry. Exit thêm `trendmode == 0`.

## Hard Rules

| Rule | Check | Status |
|------|-------|--------|
| HM-1: Anomaly | ADX filter | ✅ |
| HM-2: Liquidity | VN30F1M | ✅ |
| RK-1: Risk ≤ 2% | Position bounds | ✅ |
| RK-3: Consecutive Loss | Event-based exit | ✅ |

## Scorecard Targets

| Metric | Target |
|--------|:------:|
| Sharpe Ratio | ≥ 1.2 |
| CAGR | ≥ 20% |
| Max Drawdown | > -25% |
| Profit Factor | ≥ 1.5 |

## Edge Cases

| Case | Mitigation |
|------|------------|
| dcperiod NaN đầu | `fillna(20)` fallback |
| dcperiod dao động | `rolling_max` smooth + clip [8, 30] |
| Cycle không rõ | ADX > 22 bắt buộc |