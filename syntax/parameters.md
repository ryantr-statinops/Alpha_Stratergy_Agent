# Parameter Reference for 15min VNFuture

1 session = ~10 bars (02:00-04:30 = 2.5h). All parameters are chosen to fit within one session.

## Trend / Moving Average

| Feature | Parameter | Value | Rationale |
|---------|-----------|-------|-----------|
| adx | timeperiod | 10 | Per vietnam_market_characteristics.md |
| sma | timeperiod | 10 | 1 session = 2.5h |
| ema | timeperiod | 10 | 1 session = 2.5h |
| macd | fastperiod | 5 | 75min fast EMA |
| macd | slowperiod | 13 | 3.25h slow EMA |
| macd | signalperiod | 5 | 75min signal line |
| sar | acceleration | 0.02 | TA-Lib standard |
| sar | maximum | 0.2 | TA-Lib standard |
| mama | fastlimit | 0.5 | TA-Lib standard |
| mama | slowlimit | 0.05 | TA-Lib standard |
| ht_trendline | (none) | — | Self-adaptive, no parameter |

## Momentum / Oscillator

| Feature | Parameter | Value | Rationale |
|---------|-----------|-------|-----------|
| rsi | timeperiod | 10 | 1 session = 2.5h |
| stoch | fastk_period | 10 | 1 session |
| stoch | slowk_period | 3 | 45min smoothing |
| stoch | slowd_period | 3 | 45min smoothing |
| stochrsi | timeperiod | 10 | 1 session |
| stochrsi | fastk_period | 5 | Responsive on 15min |
| stochrsi | fastd_period | 3 | Standard smoothing |
| cci | timeperiod | 10 | 1 session |
| cmo | timeperiod | 10 | 1 session |
| willr | timeperiod | 10 | 1 session |
| aroonosc | timeperiod | 10 | 1 session |
| mfi | timeperiod | 10 | 1 session |
| momentum | timeperiod | 5 | 75min impulse |
| roc | timeperiod | 5 | 75min rate of change |
| ppo | fastperiod | 5 | 75min fast EMA |
| ppo | slowperiod | 13 | 3.25h slow EMA |
| ppo | signalperiod | 5 | 75min signal line |
| trix | timeperiod | 10 | 1 session |
| ultosc | timeperiod1 | 5 | Short period |
| ultosc | timeperiod2 | 10 | Medium period |
| ultosc | timeperiod3 | 20 | Long period (~1 day) |

## Volatility

| Feature | Parameter | Value | Rationale |
|---------|-----------|-------|-----------|
| bbands | timeperiod | 10 | 1 session |
| bbands | nbdevup | 2 | Standard |
| bbands | nbdevdn | 2 | Standard |
| atr | timeperiod | 10 | 1 session |
| price_z | timeperiod | 10 | 1 session |
| volume_z | timeperiod | 10 | 1 session |

## Volume / Flow

| Feature | Parameter | Value | Rationale |
|---------|-----------|-------|-----------|
| cmf | timeperiod | 10 | 1 session |
| obv (rolling_mean) | window | 10 | 1 session signal line |
| ad (rolling_mean) | window | 10 | 1 session signal line |

## Statistics / Rolling Window

| Feature | Parameter | Value | Rationale |
|---------|-----------|-------|-----------|
| rolling_mean | window | 10 | 1 session |
| rolling_rank | window | 10 | 1 session |
| rolling_zscore | window | 10 | 1 session |
| rolling_argmax | window | 10 | 1 session |
| rolling_argmin | window | 10 | 1 session |
| donchian_upper | timeperiod | 10 | 1 session |
| donchian_lower | timeperiod | 10 | 1 session |
| linearreg_slope | timeperiod | 10 | 1 session |
| linearreg_angle | timeperiod | 10 | 1 session |
| tsf | timeperiod | 10 | 1 session |
| linearreg | timeperiod | 10 | 1 session |
| correl | timeperiod | 20 | Needs more data points |
| beta | timeperiod | 10 | 1 session |

## Candlestick Patterns

| Feature | Parameter | Value | Rationale |
|---------|-----------|-------|-----------|
| All patterns | (none) | — | Self-contained, no timeperiod |

## Features Without Timeperiod (keep as-is)

bop, obv, ad, ht_trendline, trange, dcperiod, sine, trendmode
