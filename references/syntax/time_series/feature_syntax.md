# Time-Series Feature Syntax

Canonical API catalog for Round 2 `time_series` features. All inputs and outputs are `SeriesT` unless a tuple is explicitly documented. Data accessors come from the shared [`../data_syntax.md`](../data_syntax.md) catalog without `_panel` suffixes.

## Usage Contract

1. Call features only through `self.feat` inside `CustomStrategy.__algorithm__()`.
2. Pass every period/window/threshold explicitly in strategy code. Defaults below document the runtime signature; they are not research recommendations.
3. Select research values from [`parameters.md`](parameters.md) and preregister them before simulation.
4. Never mix these primitives with `PanelT` data or cross-sectional portfolio APIs.
5. Unpack every multi-output feature completely.
6. Expect warm-up missing values for rolling and lookback-dependent features.
7. Initial status is `CATALOG_ONLY` unless repository evidence explicitly promotes it.
8. Documentation type annotations shown here must not be copied into strategy code.

## Evidence Labels

| Label | Meaning |
|---|---|
| `CATALOG_ONLY` | Present in the user-provided API catalog |
| `EXAMPLE_VERIFIED` | Present in an approved strategy example |
| `VERIFY_PASSED` | XNOQuant verify accepted a strategy using it |
| `SIMULATE_PASSED` | XNOQuant simulation completed |
| `BEHAVIOR_VERIFIED` | Output order, warm-up, missingness, and edge behavior were checked |
| `PARTIAL_SIGNATURE` | Source signature is incomplete; do not generate strategy usage |

## Signature Convention

Every row represents `self.feat.<signature>`. `None` defaults do not make an input optional in generated strategy code; pass the intended `SeriesT` explicitly.


## Trend Strength and Direction

| Feature | Signature after `self.feat.` | Returns |
|---|---|---|
| `adx` | `adx(high=None, low=None, close=None, timeperiod=14)` | `SeriesT` |
| `adxr` | `adxr(high=None, low=None, close=None, timeperiod=14)` | `SeriesT` |
| `dx` | `dx(high=None, low=None, close=None, timeperiod=14)` | `SeriesT` |
| `plus_di` | `plus_di(high=None, low=None, close=None, timeperiod=14)` | `SeriesT` |
| `minus_di` | `minus_di(high=None, low=None, close=None, timeperiod=14)` | `SeriesT` |
| `plus_dm` | `plus_dm(high=None, low=None, timeperiod=14)` | `SeriesT` |
| `minus_dm` | `minus_dm(high=None, low=None, timeperiod=14)` | `SeriesT` |
| `aroon` | `aroon(high=None, low=None, timeperiod=14)` | `tuple[SeriesT, SeriesT] (down, up)` |
| `aroonosc` | `aroonosc(high=None, low=None, timeperiod=14)` | `SeriesT` |
| `sar` | `sar(high=None, low=None, acceleration=0, maximum=0)` | `SeriesT` |
| `sarext` | `sarext(high=None, low=None, startvalue=0, offsetonreverse=0, ...)` | `SeriesT; PARTIAL SIGNATURE` **BLOCKED** |

## Moving Averages and Trend Lines

| Feature | Signature after `self.feat.` | Returns |
|---|---|---|
| `sma` | `sma(close=None, timeperiod=30)` | `SeriesT` |
| `ema` | `ema(series=None, timeperiod=30)` | `SeriesT` |
| `dema` | `dema(series=None, timeperiod=30)` | `SeriesT` |
| `tema` | `tema(series=None, timeperiod=30)` | `SeriesT` |
| `t3` | `t3(series=None, timeperiod=5, vfactor=0)` | `SeriesT` |
| `trima` | `trima(series=None, timeperiod=30)` | `SeriesT` |
| `wma` | `wma(series=None, timeperiod=30)` | `SeriesT` |
| `ma` | `ma(series=None, timeperiod=30, matype=0)` | `SeriesT` |
| `kama` | `kama(series=None, timeperiod=30)` | `SeriesT` |
| `mama` | `mama(series=None, fastlimit=0, slowlimit=0)` | `tuple[SeriesT, SeriesT] (mama, fama)` |
| `mavp` | `mavp(series=None, periods=None, minperiod=2, maxperiod=30, matype=0)` | `SeriesT` |
| `ht_trendline` | `ht_trendline(series=None)` | `SeriesT` |
| `midpoint` | `midpoint(series=None, timeperiod=14)` | `SeriesT` |
| `midprice` | `midprice(high=None, low=None, timeperiod=14)` | `SeriesT` |

## Momentum and Oscillators

| Feature | Signature after `self.feat.` | Returns |
|---|---|---|
| `macd` | `macd(close=None, fastperiod=12, slowperiod=26, signalperiod=9)` | `tuple[SeriesT, SeriesT, SeriesT]` |
| `macdext` | `macdext(series=None, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)` | `tuple[SeriesT, SeriesT, SeriesT]` |
| `macdfix` | `macdfix(series=None, signalperiod=9)` | `tuple[SeriesT, SeriesT, SeriesT]` |
| `roc` | `roc(close=None, timeperiod=10)` | `SeriesT` |
| `rocp` | `rocp(series=None, timeperiod=10)` | `SeriesT` |
| `rocr` | `rocr(series=None, timeperiod=10)` | `SeriesT` |
| `rocr100` | `rocr100(series=None, timeperiod=10)` | `SeriesT` |
| `momentum` | `momentum(series=None, timeperiod=10)` | `SeriesT` |
| `rsi` | `rsi(close=None, timeperiod=14)` | `SeriesT` |
| `apo` | `apo(series=None, fastperiod=12, slowperiod=26, matype=0)` | `SeriesT` |
| `ppo` | `ppo(series=None, fastperiod=12, slowperiod=26, matype=0)` | `SeriesT` |
| `bop` | `bop(open_=None, high=None, low=None, close=None)` | `SeriesT` |
| `cci` | `cci(high=None, low=None, close=None, timeperiod=14)` | `SeriesT` |
| `cmo` | `cmo(series=None, timeperiod=14)` | `SeriesT` |
| `mfi` | `mfi(high=None, low=None, close=None, volume=None, timeperiod=14)` | `SeriesT` |
| `stoch` | `stoch(high=None, low=None, close=None, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)` | `tuple[SeriesT, SeriesT] (slowk, slowd)` |
| `stochf` | `stochf(high=None, low=None, close=None, fastk_period=5, fastd_period=3, fastd_matype=0)` | `tuple[SeriesT, SeriesT] (fastk, fastd)` |
| `stochrsi` | `stochrsi(series=None, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)` | `tuple[SeriesT, SeriesT] (fastk, fastd)` |
| `trix` | `trix(close=None, timeperiod=30)` | `SeriesT` |
| `ultosc` | `ultosc(high=None, low=None, close=None, timeperiod1=7, timeperiod2=14, timeperiod3=28)` | `SeriesT` |
| `willr` | `willr(high=None, low=None, close=None, timeperiod=14)` | `SeriesT` |

## Volume, Flow, VWAP

| Feature | Signature after `self.feat.` | Returns |
|---|---|---|
| `obv` | `obv(close=None, volume=None)` | `SeriesT` |
| `ad` | `ad(high=None, low=None, close=None, volume=None)` | `SeriesT` |
| `adosc` | `adosc(high=None, low=None, close=None, volume=None, fastperiod=3, slowperiod=10)` | `SeriesT` |
| `vwap` | `vwap(high, low, close, volume)` | `SeriesT` |
| `rolling_vwap` | `rolling_vwap(high, low, close, volume, window=20)` | `SeriesT` |

## Volatility and Bands

| Feature | Signature after `self.feat.` | Returns |
|---|---|---|
| `atr` | `atr(high=None, low=None, close=None, timeperiod=14)` | `SeriesT` |
| `natr` | `natr(high=None, low=None, close=None, timeperiod=14)` | `SeriesT` |
| `trange` | `trange(high=None, low=None, close=None)` | `SeriesT` |
| `bbands` | `bbands(close=None, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)` | `tuple[SeriesT, SeriesT, SeriesT] (upper, middle, lower)` |

## Cycle Indicators

| Feature | Signature after `self.feat.` | Returns |
|---|---|---|
| `dcperiod` | `dcperiod(close=None)` | `SeriesT` |
| `sine` | `sine(close)` | `tuple[SeriesT, SeriesT] (sine, leadsine)` |
| `trendmode` | `trendmode(close=None)` | `SeriesT` |

## Price Transforms

| Feature | Signature after `self.feat.` | Returns |
|---|---|---|
| `avgprice` | `avgprice(open_=None, high=None, low=None, close=None)` | `SeriesT` |
| `medprice` | `medprice(high=None, low=None)` | `SeriesT` |
| `typprice` | `typprice(high=None, low=None, close=None)` | `SeriesT` |
| `wclprice` | `wclprice(high=None, low=None, close=None)` | `SeriesT` |
| `hlc3` | `hlc3(high=None, low=..., close=...)` | `SeriesT; SOURCE TRUNCATED` **BLOCKED** |

## Statistics and Regression

| Feature | Signature after `self.feat.` | Returns |
|---|---|---|
| `beta` | `beta(s1, s2, timeperiod=5)` | `SeriesT` |
| `correl` | `correl(s1, s2, timeperiod=30)` | `SeriesT` |
| `linearreg` | `linearreg(s1, timeperiod=14)` | `SeriesT` |
| `linearreg_angle` | `linearreg_angle(s1, timeperiod=14)` | `SeriesT` |
| `linearreg_intercept` | `linearreg_intercept(s1, timeperiod=14)` | `SeriesT` |
| `linearreg_slope` | `linearreg_slope(s1, timeperiod=14)` | `SeriesT` |
| `stddev` | `stddev(s1, timeperiod=5, nbdev=1)` | `SeriesT` |
| `tsf` | `tsf(s1, timeperiod=14)` | `SeriesT` |
| `var` | `var(s1, timeperiod=5, nbdev=1)` | `SeriesT` |

## Element-wise Math

| Feature | Signature after `self.feat.` | Returns |
|---|---|---|
| `acos` | `acos(s1)` | `SeriesT` |
| `asin` | `asin(s1)` | `SeriesT` |
| `atan` | `atan(s1)` | `SeriesT` |
| `ceil` | `ceil(s1)` | `SeriesT` |
| `cos` | `cos(s1)` | `SeriesT` |
| `cosh` | `cosh(s1)` | `SeriesT` |
| `exp` | `exp(s1)` | `SeriesT` |
| `floor` | `floor(s1)` | `SeriesT` |
| `ln` | `ln(s1)` | `SeriesT` |
| `log10` | `log10(s1)` | `SeriesT` |
| `sin` | `sin(s1)` | `SeriesT` |
| `sinh` | `sinh(s1)` | `SeriesT` |
| `sqrt` | `sqrt(s1)` | `SeriesT` |
| `tan` | `tan(s1)` | `SeriesT` |
| `tanh` | `tanh(s1)` | `SeriesT` |

## Element-wise Arithmetic

| Feature | Signature after `self.feat.` | Returns |
|---|---|---|
| `add` | `add(s1, s2)` | `SeriesT` |
| `div` | `div(s1, s2)` | `SeriesT` |
| `mult` | `mult(s1, s2)` | `SeriesT` |
| `sub` | `sub(s1, s2)` | `SeriesT` |

## Period Extrema and Aggregation

| Feature | Signature after `self.feat.` | Returns |
|---|---|---|
| `max` | `max(s1, timeperiod=30)` | `SeriesT` |
| `maxindex` | `maxindex(s1, timeperiod=30)` | `SeriesT` |
| `min` | `min(s1, timeperiod=30)` | `SeriesT` |
| `minindex` | `minindex(s1, timeperiod=30)` | `SeriesT` |
| `minmax` | `minmax(s1, timeperiod=30)` | `tuple[SeriesT, SeriesT] (min, max)` |
| `minmaxindex` | `minmaxindex(s1, timeperiod=30)` | `tuple[SeriesT, SeriesT] (min index, max index)` |
| `sum` | `sum(s1, timeperiod=30)` | `SeriesT` |

## Rolling Features

| Feature | Signature after `self.feat.` | Returns |
|---|---|---|
| `rolling_mean` | `rolling_mean(s1, window=20)` | `SeriesT` |
| `rolling_max` | `rolling_max(s1, window=20)` | `SeriesT` |
| `rolling_min` | `rolling_min(s1, window=20)` | `SeriesT` |
| `rolling_std` | `rolling_std(s1, window=20)` | `SeriesT` |
| `rolling_sum` | `rolling_sum(s1, window=20)` | `SeriesT` |
| `rolling_prod` | `rolling_prod(s1, window=20)` | `SeriesT` |
| `rolling_rank` | `rolling_rank(s1, window=20)` | `SeriesT` |
| `rolling_correlation` | `rolling_correlation(s1, s2, window=20)` | `SeriesT` |
| `rolling_covariance` | `rolling_covariance(s1, s2, window=20)` | `SeriesT` |
| `rolling_median` | `rolling_median(s1, window=20)` | `SeriesT` |
| `rolling_quantile` | `rolling_quantile(s1, window=20, q=0.5)` | `SeriesT` |
| `rolling_percentile_rank` | `rolling_percentile_rank(s1, window=20, method='average')` | `SeriesT` |
| `rolling_zscore` | `rolling_zscore(s1, window=20)` | `SeriesT` |
| `rolling_mad` | `rolling_mad(s1, window=20)` | `SeriesT` |
| `rolling_argmax` | `rolling_argmax(s1, window=20)` | `SeriesT; bars since latest maximum` |
| `rolling_argmin` | `rolling_argmin(s1, window=20)` | `SeriesT; bars since latest minimum` |

## Candlestick Pattern Recognition

All catalogued candlestick functions share the documented call shape below and return `SeriesT` pattern codes:

```python
pattern = self.feat.<name>(
    open_price,
    high,
    low,
    close,
)
```

Do not treat the result as Boolean until exact signed output values are behavior-verified. Use `open_price`, never the variable name `open`.

| Feature | Signature after `self.feat.` | Returns |
|---|---|---|
| `two_crows` | `two_crows(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `three_black_crows` | `three_black_crows(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `three_inside_up_down` | `three_inside_up_down(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `three_line_strike` | `three_line_strike(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `three_outside_up_down` | `three_outside_up_down(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `three_stars_in_south` | `three_stars_in_south(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `three_white_soldiers` | `three_white_soldiers(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `abandoned_baby` | `abandoned_baby(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `advance_block` | `advance_block(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `belt_hold` | `belt_hold(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `breakaway` | `breakaway(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `closing_marubozu` | `closing_marubozu(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `concealing_baby_swallow` | `concealing_baby_swallow(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `counterattack` | `counterattack(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `dark_cloud_cover` | `dark_cloud_cover(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `doji` | `doji(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `doji_star` | `doji_star(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `dragonfly_doji` | `dragonfly_doji(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `engulfing_pattern` | `engulfing_pattern(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `evening_doji_star` | `evening_doji_star(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `evening_star` | `evening_star(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `gap_sidesidewhite` | `gap_sidesidewhite(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `gravestone_doji` | `gravestone_doji(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `hammer` | `hammer(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `hanging_man` | `hanging_man(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `harami_pattern` | `harami_pattern(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `harami_cross_pattern` | `harami_cross_pattern(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `high_wave_candle` | `high_wave_candle(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `hikkake_pattern` | `hikkake_pattern(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `modified_hikkake_pattern` | `modified_hikkake_pattern(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `homing_pigeon` | `homing_pigeon(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `identical_three_crows` | `identical_three_crows(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `in_neck_pattern` | `in_neck_pattern(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `inverted_hammer` | `inverted_hammer(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `kicking` | `kicking(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `kicking_by_length` | `kicking_by_length(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `ladder_bottom` | `ladder_bottom(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `long_legged_doji` | `long_legged_doji(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `long_line_candle` | `long_line_candle(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `marubozu` | `marubozu(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `matching_low` | `matching_low(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `mat_hold` | `mat_hold(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `morning_doji_star` | `morning_doji_star(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `morning_star` | `morning_star(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `on_neck_pattern` | `on_neck_pattern(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `piercing_pattern` | `piercing_pattern(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `rickshaw_man` | `rickshaw_man(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `rising_falling_three_methods` | `rising_falling_three_methods(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `separating_lines` | `separating_lines(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `shooting_star` | `shooting_star(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `short_line_candle` | `short_line_candle(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `spinning_top` | `spinning_top(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `stalled_pattern` | `stalled_pattern(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `stick_sandwich` | `stick_sandwich(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `takuri` | `takuri(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `thrusting_pattern` | `thrusting_pattern(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `tristar_pattern` | `tristar_pattern(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `unique_3_river` | `unique_3_river(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `upside_gap_two_crows` | `upside_gap_two_crows(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |
| `xside_gap_3methods` | `xside_gap_3methods(open_=None, high=None, low=None, close=None)` | `SeriesT` pattern code |

## Multi-Output Rules

| Feature family | Required unpacking |
|---|---|
| `macd`, `macdext`, `macdfix` | `macd_line, signal_line, histogram` |
| `bbands` | `upper, middle, lower` |
| `mama` | `mama_line, fama_line` |
| `aroon` | `aroon_down, aroon_up` |
| `stoch` | `slow_k, slow_d` |
| `stochf`, `stochrsi` | `fast_k, fast_d` |
| `sine` | `sine_line, lead_sine` |
| `minmax` | `minimum, maximum` |
| `minmaxindex` | `minimum_index, maximum_index` |

## Domain and Safety Guards

| Feature | Required research check |
|---|---|
| `sqrt` | Input must be non-negative |
| `ln`, `log10` | Input must be strictly positive |
| `acos`, `asin` | Input must remain in `[-1, 1]` |
| `div` | Denominator-zero behavior must be verified |
| `exp` | Extreme inputs can overflow |
| `mavp` | Period series, bounds, missingness, and causality need verification |
| `sar`, `mama`, `t3` | Zero-valued runtime defaults need verification; pass approved values explicitly |

Native operators (`+`, `-`, `*`, `/`) remain preferred over `add`, `sub`, `mult`, and `div` when the strategy framework supports the same expression clearly.

## Known Incomplete Source Entries

- `sarext`: the supplied signature ended in `...`; strategy usage is blocked until all acceleration parameters and defaults are documented.
- `hlc3`: the supplied source was truncated after `high`/`lo`; the row is retained only as an inventory marker and must not be generated into code.

## Research Notes

- Oscillator labels such as “overbought” and “oversold” are descriptive conventions, not automatic entry rules.
- Pattern-recognition functions are observations, not complete economic hypotheses.
- `beta` and `correl` require an explicitly selected comparison series; VN30 can be a documented proxy but is not a complete risk model.
- Fundamental observations forward-filled on a daily timeline do not become independent daily observations when passed through rolling features.
