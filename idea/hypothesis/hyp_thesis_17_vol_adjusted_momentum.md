# Hypothesis — Thesis 17: Volatility-Adjusted Momentum

## Thông tin chung

| Field | Value |
|-------|-------|
| Thesis Group | 17 — Volatility-Adjusted Momentum |
| Core Idea | Normalize ROC (momentum) by ATR (volatility) to filter out noise. Only genuine momentum that exceeds current volatility level triggers entries. Adaptive thresholds for low/high vol regimes. |
| Data Fields | `pv_close`, `pv_high`, `pv_low`, `pv_volume` |
| Timeframes | 15, 30, 60 min |
| Templates | T17-A (Core Breakout), T17-B (+SMA Filter), T17-C (Regime Adaptive) |
| Est. Variants | ~9 (3 TFs x 3 params) |
| Status | TODO |

---

## HYP-VAM-01: Vol-Adj Momentum Core (T17-A)

**Logic:**
```python
adj_mom = roc(close, 14) / atr(high, low, close, 14)
adj_mom_z = rolling_zscore(adj_mom, 20)
long: adj_mom_z > 1.5 & close > bb_mid & volume > vol_sma & return_roll > 0
short: adj_mom_z < -1.5 & close < bb_mid & volume > vol_sma & return_roll < 0
exit: adx < 18 | atr_stop | trailing
```

## HYP-VAM-02: Vol-Adj Momentum + SMA Filter (T17-B)

Thêm SMA13/SMA34 trend filter. Entry chỉ khi SMA nhanh cùng hướng.

**Exit thêm:** `adj_mom_z < 0` — thoát sớm khi momentum về neutral.

## HYP-VAM-03: Vol-Adj Momentum Regime (T17-C)

- `vol_regime = atr / sma(atr, 20)`
- Low vol (ratio < 0.8): z_entry = 2.0, trailing mult = 1.5
- High vol (ratio >= 0.8): z_entry = 1.2, trailing mult = 2.5

## Scorecard Targets

| Metric | Target |
|--------|:------:|
| Sharpe Ratio | ≥ 1.2 |
| CAGR | ≥ 20% |
| Max Drawdown | > -25% |
| Profit Factor | ≥ 1.5 |

## Next Steps

- [ ] Upload lên XNOQuant
- [ ] Simulate + scorecard