# syntax_feature_v2 — Template cung cấp feature functions mới

## sumary
mỗi 4 dòng là 4 nội dung của 1 feature:
ví dụ:
sma_panel
Returns: PanelT
self.feat.sma_panel(close: PanelT)
PanelT equivalent of the sma time-series feature.

## list:

sma_panel
Returns: PanelT
self.feat.sma_panel(close: PanelT)
PanelT equivalent of the sma time-series feature.
ema_panel
Returns: PanelT
self.feat.ema_panel(series: PanelT)
PanelT equivalent of the ema time-series feature.
rolling_zscore_panel
Returns: PanelT
self.feat.rolling_zscore_panel(s1: PanelT)
PanelT equivalent of the rolling_zscore time-series feature.
returns_panel
Returns: PanelT
self.feat.returns_panel(series: PanelT)
PanelT equivalent of the returns time-series feature.
log_returns_panel
Returns: PanelT
self.feat.log_returns_panel(series: PanelT)
PanelT equivalent of the log_returns time-series feature.
delta_panel
Returns: PanelT
self.feat.delta_panel(series: PanelT)
PanelT equivalent of the delta time-series feature.
safe_divide_panel
Returns: PanelT
self.feat.safe_divide_panel(numerator: PanelT, denominator: PanelT)
PanelT equivalent of the safe_divide time-series feature.
rolling_mean_panel
Returns: PanelT
self.feat.rolling_mean_panel(s1: PanelT)
PanelT equivalent of the rolling_mean time-series feature.
rolling_std_panel
Returns: PanelT
self.feat.rolling_std_panel(s1: PanelT)
PanelT equivalent of the rolling_std time-series feature.
rolling_sum_panel
Returns: PanelT
self.feat.rolling_sum_panel(s1: PanelT)
PanelT equivalent of the rolling_sum time-series feature.
rolling_min_panel
Returns: PanelT
self.feat.rolling_min_panel(s1: PanelT)
PanelT equivalent of the rolling_min time-series feature.
rolling_max_panel
Returns: PanelT
self.feat.rolling_max_panel(s1: PanelT)
PanelT equivalent of the rolling_max time-series feature.
rolling_rank_panel
Returns: PanelT
self.feat.rolling_rank_panel(s1: PanelT)
PanelT equivalent of the rolling_rank time-series feature.
rolling_percentile_rank_panel
Returns: PanelT
self.feat.rolling_percentile_rank_panel(s1: PanelT)
PanelT equivalent of the rolling_percentile_rank time-series feature.
rolling_correlation_panel
Returns: PanelT
self.feat.rolling_correlation_panel(s1: PanelT, s2: PanelT)
PanelT equivalent of the rolling_correlation time-series feature.
rolling_covariance_panel
Returns: PanelT
self.feat.rolling_covariance_panel(s1: PanelT, s2: PanelT)
PanelT equivalent of the rolling_covariance time-series feature.
hlc3_panel
Returns: PanelT
self.feat.hlc3_panel(high: PanelT, low: PanelT, close: PanelT)
PanelT equivalent of the hlc3 time-series feature.
typprice_panel
Returns: PanelT
self.feat.typprice_panel(high: PanelT, low: PanelT, close: PanelT)
PanelT equivalent of the typprice time-series feature.
medprice_panel
Returns: PanelT
self.feat.medprice_panel(high: PanelT, low: PanelT)
PanelT equivalent of the medprice time-series feature.
wclprice_panel
Returns: PanelT
self.feat.wclprice_panel(high: PanelT, low: PanelT, close: PanelT)
PanelT equivalent of the wclprice time-series feature.
ohlc4_panel
Returns: PanelT
self.feat.ohlc4_panel(open_: PanelT, high: PanelT, low: PanelT, close: PanelT)
PanelT equivalent of the ohlc4 time-series feature.
vwap_panel
Returns: PanelT
self.feat.vwap_panel(high: PanelT, low: PanelT, close: PanelT, volume: PanelT)
PanelT equivalent of the vwap time-series feature.
rolling_vwap_panel
Returns: PanelT
self.feat.rolling_vwap_panel(high: PanelT, low: PanelT, close: PanelT, volume: PanelT)
PanelT equivalent of the rolling_vwap time-series feature.
close_location_panel
Returns: PanelT
self.feat.close_location_panel(high: PanelT, low: PanelT, close: PanelT)
PanelT equivalent of the close_location time-series feature.
range_pct_panel
Returns: PanelT
self.feat.range_pct_panel(high: PanelT, low: PanelT, close: PanelT)
PanelT equivalent of the range_pct time-series feature.
atr_panel
Returns: PanelT
self.feat.atr_panel(high: PanelT, low: PanelT, close: PanelT)
PanelT equivalent of the atr time-series feature.
natr_panel
Returns: PanelT
self.feat.natr_panel(high: PanelT, low: PanelT, close: PanelT)
PanelT equivalent of the natr time-series feature.
volume_z_panel
Returns: PanelT
self.feat.volume_z_panel(volume: PanelT)
PanelT equivalent of the volume_z time-series feature.
rolling_value_panel
Returns: PanelT
self.feat.rolling_value_panel(close: PanelT, volume: PanelT)
PanelT equivalent of the rolling_value time-series feature.
amihud_illiquidity_panel
Returns: PanelT
self.feat.amihud_illiquidity_panel(close: PanelT, volume: PanelT)
PanelT equivalent of the amihud_illiquidity time-series feature.
cmf_panel
Returns: PanelT
self.feat.cmf_panel(high: PanelT, low: PanelT, close: PanelT, volume: PanelT)
PanelT equivalent of the cmf time-series feature.
rsi_panel
Returns: PanelT
self.feat.rsi_panel(close: PanelT)
PanelT equivalent of the rsi time-series feature.
macd_panel
Returns: PanelT
self.feat.macd_panel(close: PanelT, output='macd')
PanelT equivalent of the macd time-series feature.
bbands_panel
Returns: PanelT
self.feat.bbands_panel(close: PanelT, output='upper')
PanelT equivalent of the bbands time-series feature.
donchian_upper_panel
Returns: PanelT
self.feat.donchian_upper_panel(high: PanelT)
PanelT equivalent of the donchian_upper time-series feature.
donchian_lower_panel
Returns: PanelT
self.feat.donchian_lower_panel(low: PanelT)
PanelT equivalent of the donchian_lower time-series feature.