# Feature Syntax Reference (Round 2)

Use this file as the canonical catalog for `self.feat.*` on the Round 2 equity model.

## Mode Contract

`self.feat.*` functions come in two families, matching the two execution modes:

| Mode | Feature family | Shape | Example |
|---|---|---|---|
| `time_series` | suffix-less features with `timeperiod` params | one time series per symbol | `self.feat.ema(close, timeperiod=8)` |
| `cross_sectional` | `_panel` features on `PanelT` | time × symbol panel | `self.feat.ema_panel(series)` |

- In `time_series` mode the feature returns a single time series for the symbol being evaluated.
- In `cross_sectional` mode the feature takes a `PanelT` (time × symbol) and returns a `PanelT`.
- Use the `_panel` form **only** with `_panel` data fields; never mix families (see `data_syntax.md`).
- Supported cross-sectional features are documented below; `stage_2_guideline.md` explicitly guarantees
  `safe_divide_panel`, `ema_panel`, `sma_panel`, `rolling_zscore_panel`.

## Section Index


| Trend / Moving Average | [jump](#trend-moving-average) |
| Statistics / Volatility / Rolling Window | [jump](#statistics-volatility-rolling-window) |
| Price Transforms / Returns | [jump](#price-transforms-returns) |
| Volume / Flow | [jump](#volume-flow) |
| Momentum / Oscillator / Breakout | [jump](#momentum-oscillator-breakout) |

## Quick Lookup

| Group | Representative functions |
|---|---|
| Trend / Moving Average | `sma_panel`, `ema_panel` |
| Momentum / Oscillator / Breakout | `rsi_panel`, `macd_panel`, `bbands_panel`, `donchian_upper_panel` |
| Statistics / Volatility / Rolling Window | `rolling_zscore_panel`, `rolling_mean_panel`, `rolling_rank_panel`, `atr_panel`, `volume_z_panel` |
| Price Transforms / Returns | `returns_panel`, `log_returns_panel`, `delta_panel`, `safe_divide_panel`, `hlc3_panel` |
| Volume / Flow | `vwap_panel`, `rolling_vwap_panel`, `amihud_illiquidity_panel`, `cmf_panel` |

## Reading Tips

- Prefer `safe_divide_panel` over raw division when constructing ratios (avoids div-by-zero/negative denominator).
- Use `ema_panel` / `sma_panel` for cross-sectional trend; `rolling_zscore_panel` for cross-sectional value signals.
- In `time_series` mode drop the `_panel` suffix and add `timeperiod=` (see `parameters.md`).


## Trend / Moving Average

| Name | Returns | Syntax | Description |
|---|---|---|---|
| `sma_panel` | `PanelT` | `self.feat.sma_panel(close: PanelT)` | PanelT equivalent of the sma time-series feature. |
| `ema_panel` | `PanelT` | `self.feat.ema_panel(series: PanelT)` | PanelT equivalent of the ema time-series feature. |

## Statistics / Volatility / Rolling Window

| Name | Returns | Syntax | Description |
|---|---|---|---|
| `rolling_zscore_panel` | `PanelT` | `self.feat.rolling_zscore_panel(s1: PanelT)` | PanelT equivalent of the rolling_zscore time-series feature. |
| `rolling_mean_panel` | `PanelT` | `self.feat.rolling_mean_panel(s1: PanelT)` | PanelT equivalent of the rolling_mean time-series feature. |
| `rolling_std_panel` | `PanelT` | `self.feat.rolling_std_panel(s1: PanelT)` | PanelT equivalent of the rolling_std time-series feature. |
| `rolling_sum_panel` | `PanelT` | `self.feat.rolling_sum_panel(s1: PanelT)` | PanelT equivalent of the rolling_sum time-series feature. |
| `rolling_min_panel` | `PanelT` | `self.feat.rolling_min_panel(s1: PanelT)` | PanelT equivalent of the rolling_min time-series feature. |
| `rolling_max_panel` | `PanelT` | `self.feat.rolling_max_panel(s1: PanelT)` | PanelT equivalent of the rolling_max time-series feature. |
| `rolling_rank_panel` | `PanelT` | `self.feat.rolling_rank_panel(s1: PanelT)` | PanelT equivalent of the rolling_rank time-series feature. |
| `rolling_percentile_rank_panel` | `PanelT` | `self.feat.rolling_percentile_rank_panel(s1: PanelT)` | PanelT equivalent of the rolling_percentile_rank time-series feature. |
| `rolling_correlation_panel` | `PanelT` | `self.feat.rolling_correlation_panel(s1: PanelT, s2: PanelT)` | PanelT equivalent of the rolling_correlation time-series feature. |
| `rolling_covariance_panel` | `PanelT` | `self.feat.rolling_covariance_panel(s1: PanelT, s2: PanelT)` | PanelT equivalent of the rolling_covariance time-series feature. |
| `rolling_vwap_panel` | `PanelT` | `self.feat.rolling_vwap_panel(high: PanelT, low: PanelT, close: PanelT, volume: PanelT)` | PanelT equivalent of the rolling_vwap time-series feature. |
| `atr_panel` | `PanelT` | `self.feat.atr_panel(high: PanelT, low: PanelT, close: PanelT)` | PanelT equivalent of the atr time-series feature. |
| `natr_panel` | `PanelT` | `self.feat.natr_panel(high: PanelT, low: PanelT, close: PanelT)` | PanelT equivalent of the natr time-series feature. |
| `volume_z_panel` | `PanelT` | `self.feat.volume_z_panel(volume: PanelT)` | PanelT equivalent of the volume_z time-series feature. |
| `rolling_value_panel` | `PanelT` | `self.feat.rolling_value_panel(close: PanelT, volume: PanelT)` | PanelT equivalent of the rolling_value time-series feature. |

## Price Transforms / Returns

| Name | Returns | Syntax | Description |
|---|---|---|---|
| `returns_panel` | `PanelT` | `self.feat.returns_panel(series: PanelT)` | PanelT equivalent of the returns time-series feature. |
| `log_returns_panel` | `PanelT` | `self.feat.log_returns_panel(series: PanelT)` | PanelT equivalent of the log_returns time-series feature. |
| `delta_panel` | `PanelT` | `self.feat.delta_panel(series: PanelT)` | PanelT equivalent of the delta time-series feature. |
| `safe_divide_panel` | `PanelT` | `self.feat.safe_divide_panel(numerator: PanelT, denominator: PanelT)` | PanelT equivalent of the safe_divide time-series feature. |
| `hlc3_panel` | `PanelT` | `self.feat.hlc3_panel(high: PanelT, low: PanelT, close: PanelT)` | PanelT equivalent of the hlc3 time-series feature. |
| `typprice_panel` | `PanelT` | `self.feat.typprice_panel(high: PanelT, low: PanelT, close: PanelT)` | PanelT equivalent of the typprice time-series feature. |
| `medprice_panel` | `PanelT` | `self.feat.medprice_panel(high: PanelT, low: PanelT)` | PanelT equivalent of the medprice time-series feature. |
| `wclprice_panel` | `PanelT` | `self.feat.wclprice_panel(high: PanelT, low: PanelT, close: PanelT)` | PanelT equivalent of the wclprice time-series feature. |
| `ohlc4_panel` | `PanelT` | `self.feat.ohlc4_panel(open_: PanelT, high: PanelT, low: PanelT, close: PanelT)` | PanelT equivalent of the ohlc4 time-series feature. |

## Volume / Flow

| Name | Returns | Syntax | Description |
|---|---|---|---|
| `vwap_panel` | `PanelT` | `self.feat.vwap_panel(high: PanelT, low: PanelT, close: PanelT, volume: PanelT)` | PanelT equivalent of the vwap time-series feature. |
| `amihud_illiquidity_panel` | `PanelT` | `self.feat.amihud_illiquidity_panel(close: PanelT, volume: PanelT)` | PanelT equivalent of the amihud_illiquidity time-series feature. |
| `cmf_panel` | `PanelT` | `self.feat.cmf_panel(high: PanelT, low: PanelT, close: PanelT, volume: PanelT)` | PanelT equivalent of the cmf time-series feature. |

## Momentum / Oscillator / Breakout

| Name | Returns | Syntax | Description |
|---|---|---|---|
| `close_location_panel` | `PanelT` | `self.feat.close_location_panel(high: PanelT, low: PanelT, close: PanelT)` | PanelT equivalent of the close_location time-series feature. |
| `range_pct_panel` | `PanelT` | `self.feat.range_pct_panel(high: PanelT, low: PanelT, close: PanelT)` | PanelT equivalent of the range_pct time-series feature. |
| `rsi_panel` | `PanelT` | `self.feat.rsi_panel(close: PanelT)` | PanelT equivalent of the rsi time-series feature. |
| `macd_panel` | `PanelT` | `self.feat.macd_panel(close: PanelT, output='macd')` | PanelT equivalent of the macd time-series feature. |
| `bbands_panel` | `PanelT` | `self.feat.bbands_panel(close: PanelT, output='upper')` | PanelT equivalent of the bbands time-series feature. |
| `donchian_upper_panel` | `PanelT` | `self.feat.donchian_upper_panel(high: PanelT)` | PanelT equivalent of the donchian_upper time-series feature. |
| `donchian_lower_panel` | `PanelT` | `self.feat.donchian_lower_panel(low: PanelT)` | PanelT equivalent of the donchian_lower time-series feature. |


## Time-Series Mode Notes

In `time_series` mode the same indicators are available without the `_panel` suffix and accept a
`timeperiod` parameter, for example (see `template_example/VN-TOP10-BANK/`):

```python
ema_fast = self.feat.ema(close, timeperiod=8)
sma_base = self.feat.sma(volume, timeperiod=10)
rsi = self.feat.rsi(close, timeperiod=7)
atr = self.feat.atr(high, low, close, timeperiod=14)
```

- Keep indicator parameters inside the allowed timeperiod convention (`syntax/parameters.md`).
- Do not reimplement an indicator that the framework already provides.
