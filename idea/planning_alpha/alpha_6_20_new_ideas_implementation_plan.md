# Alpha Ideas Master Plan - 20 New Ideas (Low-Overlap Priority)

> **Session:** 2026-07-16
> **Goal:** Lich trien khai chi tiet cho 20 idea moi, uu tien moi hoan toan va it overlap nhat voi `output/` hien tai.
> **Primary Context:** `data/vietnam_market_characteristics.md`, `data/VnFuture.md`, `syntax/feature_syntax.md`, `syntax/operations_syntax.md`

---

## 1. Design Rules

### 1.1 Market Rules to Respect
- VN30F1M is retail-dominated, so trend bursts and forced liquidations matter.
- Morning session (02:00-04:30 UTC) is the cleanest trending window.
- Lunch (04:30-06:00 UTC) is noisy and should be closed or avoided.
- ATC (07:30-07:45 UTC) is manipulation-prone, so positions should be flat.
- ADX < 20 usually means do not trade.

### 1.2 Code Constraints
- Use `CustomStrategy(SimpleAlgorithm)` and `__algorithm__(self)`.
- Prefer causal operators from `syntax/operations_syntax.md`.
- Avoid `open` as a variable name; use `open_price`.
- Use tuple unpacking for multi-return features like `mama`, `stoch`, `macd`.

### 1.3 Common Confirmation Stack
Default stack for most ideas:
- Core signal: 1 primary idea only.
- Confirmation: `adx > 22` or `adx > 20`.
- Momentum: `return_roll > 0` for long, `< 0` for short when applicable.
- Volume: `pv_volume > SMA(volume, 20)` or futures flow confirmation.
- Exit: core reversal + `adx < 18` + session close.

---

## 2. The 20 Ideas

### Group A - Direction / Trend Strength

#### 1. `PLUS_DI_MINUS_DI_SPREAD_ADX`
- **Core**: `plus_di - minus_di`
- **Long**: spread > 0 and ADX strong
- **Short**: spread < 0 and ADX strong
- **Exit**: spread crosses 0 or ADX weakens
- **Data**: `pv_high`, `pv_low`, `pv_close`
- **TF**: 15m, 30m
- **Overlap risk**: low

#### 2. `DX_CCI_BREAKOUT`
- **Core**: DX trend strength + CCI direction
- **Long**: `dx > 22` and `cci > 0`
- **Short**: `dx > 22` and `cci < 0`
- **Exit**: CCI cross 0 or `adx < 18`
- **Data**: OHLC
- **TF**: 15m, 30m
- **Overlap risk**: low

#### 3. `ADXR_ROC_MOMENTUM`
- **Core**: ADXR for smoother trend strength
- **Long**: `adxr > threshold` and `roc > 0`
- **Short**: `adxr > threshold` and `roc < 0`
- **Exit**: ROC reverses or ADXR weakens
- **Data**: OHLC
- **TF**: 15m, 30m, 60m
- **Overlap risk**: low

#### 4. `KAMA_SLOPE_ADX`
- **Core**: slope of KAMA / trend direction
- **Long**: `kama slope > 0` and ADX strong
- **Short**: `kama slope < 0` and ADX strong
- **Exit**: slope flips or `adx < 18`
- **Data**: OHLC
- **TF**: 15m, 30m
- **Overlap risk**: low

#### 5. `ADOSC_ADX_FLOW`
- **Core**: Chaikin AD oscillator with trend filter
- **Long**: `adosc > 0` and ADX strong
- **Short**: `adosc < 0` and ADX strong
- **Exit**: ADOSC crosses 0 or ADX weakens
- **Data**: OHLC + volume
- **TF**: 15m, 30m
- **Overlap risk**: low-medium

---

### Group B - Adaptive Trend / MA Variants

#### 6. `DEMA_CCI`
- **Core**: DEMA trend line
- **Long**: `close > dema` and `cci > 0`
- **Short**: `close < dema` and `cci < 0`
- **Exit**: close crosses DEMA or CCI crosses 0
- **Data**: OHLC
- **TF**: 15m, 30m
- **Overlap risk**: low

#### 7. `TEMA_RSI`
- **Core**: TEMA trend line
- **Long**: `close > tema` and `rsi > 50`
- **Short**: `close < tema` and `rsi < 50`
- **Exit**: close crosses TEMA or RSI crosses 50
- **Data**: OHLC
- **TF**: 15m, 30m
- **Overlap risk**: low

#### 8. `T3_ROC`
- **Core**: smoothed T3 trend filter
- **Long**: `close > t3` and `roc > 0`
- **Short**: `close < t3` and `roc < 0`
- **Exit**: close crosses T3 or ROC flips
- **Data**: OHLC
- **TF**: 15m, 30m
- **Overlap risk**: low

#### 9. `APO_VOLUME_Z`
- **Core**: APO trend oscillator
- **Long**: `apo > 0` and volume z-score positive
- **Short**: `apo < 0` and volume z-score positive
- **Exit**: APO crosses 0 or volume z-score fades
- **Data**: OHLC + volume
- **TF**: 15m
- **Overlap risk**: low

#### 10. `PPO_OBV_CONFIRM`
- **Core**: PPO trend oscillator
- **Long**: `ppo > 0` and OBV above OBV MA
- **Short**: `ppo < 0` and OBV below OBV MA
- **Exit**: PPO crosses 0 or OBV loses slope
- **Data**: OHLC + volume
- **TF**: 15m, 30m
- **Overlap risk**: low

---

### Group C - Volume / Futures Flow

#### 11. `TRIX_MATCHED_VOLUME_ACCELERATION`
- **Core**: TRIX trend plus futures matched volume acceleration
- **Long**: `trix > 0` and matched volume accelerates
- **Short**: `trix < 0` and matched volume accelerates
- **Exit**: TRIX crosses 0 or volume acceleration stalls
- **Data**: `pv_close`, `fut_matched_volume_vn30f1m_1d`
- **TF**: 15m, 30m
- **Overlap risk**: low

#### 12. `MFI_VOLUME_ACCELERATION`
- **Core**: MFI with volume momentum
- **Long**: `mfi > 50` and volume accelerating
- **Short**: `mfi < 50` and volume accelerating
- **Exit**: MFI crosses 50 or volume momentum fades
- **Data**: OHLC + volume
- **TF**: 15m, 30m
- **Overlap risk**: low

#### 13. `OPEN_INTEREST_CHANGE_ROC`
- **Core**: open interest change + price ROC
- **Long**: OI rises while ROC positive
- **Short**: OI rises while ROC negative
- **Exit**: OI change normalizes or ROC flips
- **Data**: `fut_open_interest_vn30f1m_1d`, `pv_close`
- **TF**: 30m, 60m
- **Overlap risk**: low

#### 14. `OPEN_INTEREST_DIVERGENCE_RETURN_ROLL`
- **Core**: OI divergence vs return roll
- **Long**: price weak but OI does not confirm selling
- **Short**: price strong but OI does not confirm buying
- **Exit**: return_roll normalizes or OI reverts
- **Data**: OI + OHLC
- **TF**: 30m, 60m
- **Overlap risk**: low

#### 15. `MATCHED_VALUE_ACCELERATION_ADX`
- **Core**: matched value acceleration + trend strength
- **Long**: matched value rising fast and ADX strong
- **Short**: matched value falling / weak and ADX strong
- **Exit**: matched value acceleration fades or ADX < 18
- **Data**: `fut_matched_value_vn30f1m_1d`, OHLC
- **TF**: 15m, 30m
- **Overlap risk**: low

---

### Group D - Regime / Macro / Cross-Market

#### 16. `HT_TRENDMODE_ROC`
- **Core**: trend mode filter with ROC timing
- **Long**: trendmode = 1 and ROC positive
- **Short**: trendmode = 1 and ROC negative
- **Exit**: trendmode flips to cycle or ROC flips
- **Data**: OHLC
- **TF**: 15m, 30m, 60m
- **Overlap risk**: low

#### 17. `CROSS_MARKET_BETA_CCI`
- **Core**: beta to DJI or VN30 + CCI confirmation
- **Long**: beta supportive + CCI positive
- **Short**: beta supportive + CCI negative
- **Exit**: CCI crosses 0 or beta weakens
- **Data**: `pv_close`, `pv_dji_close` or `pv_vn30_close`
- **TF**: 30m, 60m
- **Overlap risk**: medium

#### 18. `CROSS_MARKET_CORRELATION_ROC`
- **Core**: rolling correlation regime + ROC
- **Long**: low correlation regime and ROC positive
- **Short**: low correlation regime and ROC negative
- **Exit**: correlation rises above threshold or ROC flips
- **Data**: `pv_close`, `pv_vn30_close` / `pv_dji_close`
- **TF**: 30m, 60m
- **Overlap risk**: medium

#### 19. `MACRO_REGIME_INTERBANK_MOMENTUM`
- **Core**: daily macro regime + intraday momentum
- **Long**: loose liquidity regime + positive momentum
- **Short**: tight liquidity regime + negative momentum
- **Exit**: momentum reverses or macro regime changes
- **Data**: macro daily + OHLC
- **TF**: 30m, 60m
- **Overlap risk**: low-medium

#### 20. `USDVND_RISK_OFF_FILTER`
- **Core**: USD/VND shock filter + trend direction
- **Long**: stable FX regime + trend positive
- **Short**: unstable FX regime + trend negative
- **Exit**: FX regime normalizes or trend weakens
- **Data**: macro daily + OHLC
- **TF**: 30m, 60m
- **Overlap risk**: low-medium

---

## 3. Priority Order

### Wave 1 - Best Fit / Lowest Overlap
1. `PLUS_DI_MINUS_DI_SPREAD_ADX`
2. `DX_CCI_BREAKOUT`
3. `KAMA_SLOPE_ADX`
4. `ADXR_ROC_MOMENTUM`
5. `TRIX_MATCHED_VOLUME_ACCELERATION`

### Wave 2 - Strong Secondary Candidates
6. `DEMA_CCI`
7. `TEMA_RSI`
8. `T3_ROC`
9. `MATCHED_VALUE_ACCELERATION_ADX`
10. `HT_TRENDMODE_ROC`

### Wave 3 - Higher Overlap / More Macro Dependency
11. `ADOSC_ADX_FLOW`
12. `PPO_OBV_CONFIRM`
13. `MFI_VOLUME_ACCELERATION`
14. `OPEN_INTEREST_CHANGE_ROC`
15. `OPEN_INTEREST_DIVERGENCE_RETURN_ROLL`

### Wave 4 - Cross-Market / Macro Filters
16. `CROSS_MARKET_BETA_CCI`
17. `CROSS_MARKET_CORRELATION_ROC`
18. `MACRO_REGIME_INTERBANK_MOMENTUM`
19. `USDVND_RISK_OFF_FILTER`
20. `APO_VOLUME_Z`

---

## 4. Implementation Template

### 4.1 File Naming
- `MF_<CORE>_<FILTER>_15min.py`
- Keep one file per idea.
- Use concise but descriptive names.

### 4.2 Code Skeleton
```python
class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        ...
        exit_setup = ...
        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)
        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
```

### 4.3 Evaluation Order
1. Syntax verify.
2. Single-run submit.
3. Check summary metrics.
4. Keep only PASS ideas.
5. Replace weakest ideas in the same wave.

### 4.4 Pass Criteria
- Sharpe >= 1.3
- CAGR >= 15%
- MaxDD > -35%
- Profit Factor >= 1.2
- Calmar >= 1.1

---

## 5. Notes

- Ideas 1-5 are the cleanest first pass because they rely on trend + direction and avoid heavy macro dependency.
- Ideas 11, 13, 14, 15 can exploit VN30 futures-specific data and may outperform generic indicators.
- Ideas 17-20 are more regime-sensitive; they should be tested after the intraday/core set.
- Use `summary-table` for evaluation if multi-year backtest coverage matters more than aggregate-only output.

---

*End of plan.*
