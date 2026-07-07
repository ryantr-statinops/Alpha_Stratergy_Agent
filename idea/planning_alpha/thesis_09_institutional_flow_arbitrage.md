# Thesis 09: Institutional Flow Arbitrage

> **Core Ideas:** Track institutional money flow via Open Interest (OI) and matched volume/value changes; trade with the flow when OI confirms price, fade when OI diverges
> **VN Market Fit:** VN30F futures dominated by institutional participants — OI + matched volume reveal whether price moves are real or fake
> **Data Fields:** `pv_close`, `pv_high`, `pv_low`, `pv_volume` (futures) + `pv_vn30_close` (VN30 Index) + `fut_open_interest_vn30f1m_1d`, `fut_matched_value_vn30f1m_1d`, `fut_matched_volume_vn30f1m_1d`, `fut_total_value_vn30f1m_1d`
> **Timeframes:** 60m (daily fields update 1x/ngày, TF thấp hơn cho signal constant intraday)
> **Total Variants:** 3 core strategies (1 per template, default params)

---

## Key Design Constraints

1. **No individual stock data**: `self.data` chỉ có futures OHLCV, VN30 index, DJI, và `fut_*_1d` daily fields
2. **Daily fields are constant intraday**: `fut_*_1d` chỉ update 1 lần/ngày → không thể dùng `rolling_zscore` (z-score của constant = 0/NaN — xem thesis 08)
3. **Safe operations on daily fields**: Chỉ dùng `pct_change()` cho daily fields (tạo daily delta)
4. **OHLCV-based operations safe always**: `rolling_zscore`, `sma`, `adx` trên OHLCV hoạt động real-time

## Available Data Fields

| Field | Type | Updates | Usage |
|-------|------|---------|-------|
| `pv_close/high/low/volume` | OHLCV | Real-time | z-score, ADX, SMA, volume filters |
| `pv_vn30_close` | Index | Real-time | z-score, ROC, direction alignment |
| `fut_open_interest_vn30f1m_1d` | Daily | 1x/ngày | `pct_change()` → OI direction |
| `fut_matched_value_vn30f1m_1d` | Daily | 1x/ngày | `pct_change()` → flow direction |
| `fut_matched_volume_vn30f1m_1d` | Daily | 1x/ngày | `pct_change()` → volume flow direction |
| `fut_total_value_vn30f1m_1d` | Daily | 1x/ngày | (used for context) |

## Templates

### T09-A: OI Confirmation

Compare OI change direction vs futures return direction to distinguish genuine trends from weak moves.

**Logic:**
- `oi_change = pct_change(fut_open_interest, 1)` — daily OI change
- `fut_ret = pct_change(close, 1)` — futures return
- **Genuine long**: `fut_ret > 0` AND `oi_change > 0` (new money entering)
- **Genuine short**: `fut_ret < 0` AND `oi_change > 0` (new shorts building)
- **Fade long** (weak down): `fut_ret < 0` AND `oi_change < 0` (liquidation → rebound)
- **Fade short** (weak up): `fut_ret > 0` AND `oi_change < 0` (short covering → reversal)
- **Exit**: ADX < exit threshold

**Why this works:** OI increasing with price = new participants = strong trend. OI decreasing = existing participants closing = weak/no conviction.

### T09-B: Flow Divergence

Matched value flow + VN30 alignment + volume confirmation to detect institutional participation.

**Logic:**
- `matched_change = pct_change(fut_matched_value, 1)` — daily matched value change
- `vn30_ret = pct_change(vn30_close, 1)` — index direction
- `fut_ret = pct_change(close, 1)` — futures direction
- **Strong long**: fut bull AND matched value up AND VN30 aligns AND volume above SMA
- **Strong short**: fut bear AND matched value up AND VN30 aligns AND volume above SMA
- **Fade long** (weak down): fut bear AND matched value down
- **Fade short** (weak up): fut bull AND matched value down
- **Exit**: ADX < exit

**Why matched value**: Rising matched value = institutional participation increasing. When it drops, retail noise dominates → fade.

### T09-C: Composite Flow

Combine OHLCV-based z-scores (safe, real-time) with binary flow alignment signals.

**Logic:**
- `price_z = rolling_zscore(close, w)` → futures valuation
- `vn30_z = rolling_zscore(vn30_close, w)` → index context
- `vol_z = rolling_zscore(volume, w)` → participation intensity
- `composite = price_z + vn30_z + vol_z` → combined signal
- **Flow aligned**: OI direction == matched volume direction (both ↑ or both ↓)
- **Long**: composite > entry AND flow aligned AND ADX > entry
- **Short**: composite < -entry AND flow aligned AND ADX > entry
- **Exit**: |composite| < 0.5 OR ADX < exit

**Why composite**: All 3 z-scores are OHLCV-based (safe, real-time), only binary signals come from daily fields. Avoids z-score-on-constant problem entirely.

## Parameter Tuning

| Template | adx_entry | adx_exit | adx_window | window | entry |
|----------|-----------|----------|------------|--------|-------|
| T09-A | 18 | 12 | 7 | — | — |
| T09-B | 18 | 12 | 7 | — | 14 (vol) |
| T09-C | 18 | 12 | 7 | 20 | 2.0 |

Daily fields constant intraday → all entries effective at first bar after daily data refresh.

## Regime Map

| Template | Regimes | Vol | Rationale |
|----------|---------|-----|-----------|
| T09-A | weak, ranging | normal, low | OI confirmation works best when market is deciding direction |
| T09-B | trending | normal, high | Flow divergence needs volume + trend to be meaningful |
| T09-C | weak, ranging | normal, low | Composite z-score reversion works in range-bound markets |

## Key Lessons from Thesis 08

- `fut_*_1d` fields are **broadcast as constant values** on intraday timeframes
- `rolling_zscore` on a constant array → entire output is 0 or NaN (std = 0)
- `pct_change` on a constant array → 0 (correct for daily = no change within same day)
- Solution: use `pct_change()` for daily fields, reserve `rolling_zscore()` for OHLCV

## Files

| File | Location | Purpose |
|------|----------|---------|
| Template code | `tools/generate_strategies.py` | 3 code templates (T09-A/B/C) |
| Backtest runner | `backtest/runners/thesis_09.py` | 3 numpy/pandas implementations |
| Output files | `output/thesis_09_institutional_flow_arbitrage/` | 3 XNOQuant strategy files |
| Tuning guide | `output/thesis_09_institutional_flow_arbitrage/README.md` | Vietnamese usage guide |
| Regime map | `backtest/regime.py` | STRATEGY_REGIME_MAP entries |
| Orchestrator | `backtest/run.py` | FUNC_MAP + import |

*End of Thesis 09 Design*
