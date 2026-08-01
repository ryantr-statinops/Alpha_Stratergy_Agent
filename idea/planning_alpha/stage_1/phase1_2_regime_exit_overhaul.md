# Phase 1 + 2: Regime Detection Overlay & Exit Pattern Fix

## Problem Summary

Backtest phân tích cho thấy toàn bộ 1459 strategy bị overfit vào regime **trending 2021**:
- 2020 (COVID): Sharpe 0.19, CAGR +0.88%, PF 1.13 — gần như không hoạt động
- 2021 (Uptrend): Sharpe 2.13, CAGR +25.43%, PF 2.68 — quá đẹp
- 2022 (Correction): Sharpe -0.03, CAGR -0.27%, PF 1.01 — lỗi không exit được

Nguyên nhân chính:
1. **Không có regime detection** — tất cả strategy chạy mọi lúc, không filter theo điều kiện thị trường
2. **Exit yếu** — đa số chỉ dùng `adx < threshold`, trong range market ADX xuống thấp nhưng không phải tín hiệu thoát

---

## Phase 1: Regime Detection Overlay

### 1.1 `backtest/regime.py` — Module phát hiện regime

```python
def detect_regime(df: pd.DataFrame, tf: str = "1D") -> dict:
    """
    Returns regime state dict with keys:
    - adx_regime: "trending" | "weak" | "ranging"
    - vol_regime: "high" | "normal" | "low"
    - return_regime: "uptrend" | "downtrend" | "sideways"
    - vola_direction: "expanding" | "compressing" | "stable"
    - regime_score: float 0.0–1.0 confidence
    """
    1. Compute ADX(14) → trailing 20-bar mean
       - adx_mean > 25 → "trending"
       - adx_mean 20-25 → "weak"
       - adx_mean < 20 → "ranging"

    2. Compute NATR(14) → ratio to 20-bar SMA
       - natr_ratio > 1.3 → "high"
       - natr_ratio < 0.7 → "low"
       - else → "normal"

    3. Compute ROC(close, 20) trailing mean
       - roc_mean > 0.02 → "uptrend"
       - roc_mean < -0.02 → "downtrend"
       - else → "sideways"

    4. Compute ATR slope (linearreg_slope of ATR, 10 bars)
       - slope > 0.001 → "expanding"
       - slope < -0.001 → "compressing"
       - else → "stable"

    5. regime_score = weighted combination of confidence from each sub-signal
    return dict
```

### 1.2 `backtest/strategy_signatures.py` — Regime signature cho mỗi strategy

Training process: chạy backtest từng strategy, ghi lại performance theo regime.

```python
BUILDER_REGIME_MAP = {
    # Thesis 01: Rolling Mean → works in trending + weak
    "T01-A": {"regime": ["trending", "weak"], "vol": ["normal", "low"]},
    "T01-B": {"regime": ["trending"], "vol": ["normal"]},
    "T01-C": {"regime": ["trending", "weak"], "vol": ["normal", "low"]},
    ...
    # Thesis 02-A: Vol Breakout → works in high vol
    "T02-A": {"regime": ["trending", "weak"], "vol": ["high", "normal"]},
    "T02-B": {"regime": ["ranging"], "vol": ["low"]},  # Low vol mean rev
    ...
    # Thesis 08: Key Level Absorption → works in ranging + weak
    "T08-A": {"regime": ["ranging", "weak"], "vol": ["low", "normal"]},
    "T08-B": {"regime": ["weak", "trending"], "vol": ["high"]},
    ...
}
```

**Hoặc dynamic**: Chạy 1 lần backtest đầy đủ → tính Sharpe/CAGR cho mỗi strategy theo từng regime window → tự động assign signature.

### 1.3 Sửa `backtest/run.py` — Thêm regime filter vào loop

```python
regime = detect_regime(df_daily, "1D")  # detect từ daily data

# Trong strategy loop:
signature = REGIME_SIGNATURES.get(base, None)
if signature:
    if regime["adx_regime"] not in signature["regime"]:
        continue  # skip strategy không phù hợp regime
    if regime["vol_regime"] not in signature["vol"]:
        continue
```

---

## Phase 2: Fix Exit Patterns

### 2.1 `backtest/exit_conditions.py` — Module exit chuẩn hóa

```python
def should_exit(df: pd.DataFrame, params: dict, position: np.ndarray) -> np.ndarray:
    """
    Returns boolean array: True = exit.
    3-layer exit: trend + momentum + volatility.
    """
    close = df["close"]
    high = df["high"]
    low = df["low"]
    volume = df["volume"]

    # Layer 1: Trend exit (original)
    adx_val = adx(high, low, close, timeperiod=params["adx_window"])
    trend_exit = adx_val < params["adx_exit"]

    # Layer 2: Momentum reversal exit
    return_1 = fillna(pct_change(close, periods=1), value=0)
    return_roll = rolling_mean(return_1, window=params["return_window"])
    mom_exit = (position > 0) & (return_roll < -0.0002) | \
               (position < 0) & (return_roll > 0.0002)

    # Layer 3: Volatility explosion exit (trend exhaustion)
    natr_val = natr(high, low, close, timeperiod=14)
    natr_ma = sma(natr_val, timeperiod=14)
    vol_exit = natr_val > natr_ma * params.get("vol_exit_mult", 2.0)

    return trend_exit | mom_exit | vol_exit
```

### 2.2 Thêm drawdown protection ở cấp `run.py`

```python
def apply_drawdown_protection(equity_curve: np.ndarray,
                              max_dd_allowed: float = -0.10,
                              lookback: int = 20) -> np.ndarray:
    """
    Returns boolean array: True = freeze (set position=0).
    Freeze khi trailing drawdown > max_dd_allowed.
    Unfreeze khi equity phục hồi trên peak * (1 - max_dd_allowed / 2).
    """
    peak = np.maximum.accumulate(equity_curve)
    dd = (equity_curve - peak) / peak
    frozen = np.zeros(len(equity_curve), dtype=bool)
    in_drawdown = False
    for i in range(lookback, len(equity_curve)):
        if not in_drawdown and dd[i] < max_dd_allowed:
            in_drawdown = True
            frozen[i] = True
        elif in_drawdown:
            frozen[i] = True
            if equity_curve[i] >= peak[i] * (1 - abs(max_dd_allowed) / 2):
                in_drawdown = False
                frozen[i] = False
    return frozen
```

### 2.3 Sửa tất cả templates trong `tools/generate_strategies.py`

**Pattern mới cho mỗi template:**

```python
exit_setup = (adx_val < {adx_exit})

# Thêm return_roll exit nếu template có return_roll
exit_setup = exit_setup | (return_roll < -0.0002) | (return_roll > 0.0002)

# Thêm vol exit nếu template có natr
exit_setup = exit_setup | (natr_val > natr_ma * {vol_exit_mult})
```

**Tham số mới cần thêm:**
- `vol_exit_mult = 2.0` (default, có thể override per template)
- `return_exit_threshold = 0.0002` (default)

### 2.4 Thêm `backtest/backtest.py` — Backtest engine chuẩn hóa

Wrap toàn bộ logic vào 1 hàm:

```python
def backtest(df: pd.DataFrame, position_func: callable,
             params: dict, exit_conditions: dict = None,
             dd_protection: bool = True) -> pd.DataFrame:
    """
    1. Compute position từ position_func
    2. Apply exit conditions override
    3. Apply drawdown protection
    4. Compute returns & equity
    5. Return result_df with all columns
    """
```

---

## Implementation Order

### Step 1: `backtest/regime.py` (1 session)
- Implement `detect_regime()` function
- Write unit test with known 2020/2021/2022 data
- Verify: 2020 = high vol + ranging, 2021 = trending, 2022 = weak/retrend

### Step 2: `backtest/exit_conditions.py` (1 session)
- Implement `should_exit()` with 3-layer logic
- Implement `apply_drawdown_protection()`
- Test on synthetic data

### Step 3: Sửa generate_strategies.py (1 session)
- Thêm `vol_exit_mult` vào tất cả templates có NATR
- Thêm `return_exit_threshold` vào tất cả templates có return_roll
- Thêm `exit_setup` expansion vào các code templates
- Regenerate output

### Step 4: Sửa run.py (1 session)
- Import regime, exit_conditions
- Thêm regime detection trước loop
- Thêm regime filter trong loop
- Thêm drawdown protection sau khi compute positions

### Step 5: Create strategy_signatures.py (1 session)
- `BUILDER_REGIME_MAP` với assignment rules cho từng thesis
- Dynamic mode: chạy backtest 1 lần → auto-generate signature từ kết quả

### Step 6: `backtest/backtest.py` (1 session)
- Wrap engine
- Test full pipeline

---

## Tác động kỳ vọng

| Metric | Before (avg) | After (estimated) |
|--------|-------------|-------------------|
| Sharpe 2020 | 0.19 | > 0.8 |
| Sharpe 2021 | 2.13 | > 2.0 (giữ nguyên) |
| Sharpe 2022 | -0.03 | > 0.3 |
| Max DD 2022 | -8.17% | < -5% |
| Drawdown recovery | Không hồi phục | Có hồi phục (trailing stop) |
| Strategy yield | 100% chạy mọi lúc | ~40-60% được chạy tùy regime |

---

## Rủi ro

1. **Regime detection noise**: ADX/NATR cũng có thể cho tín hiệu sai → cần threshold tuning
2. **Data frequency**: Regime detection trên daily data sẽ khác với intraday → cần separate detection per TF
3. **Signature cold start**: Ban đầu phải dùng `BUILDER_REGIME_MAP` (rules-based) trước khi có đủ data để build dynamic signature
