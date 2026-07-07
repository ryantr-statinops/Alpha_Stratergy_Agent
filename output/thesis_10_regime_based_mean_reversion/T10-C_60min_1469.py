"""
name:    T10-C
summary: Regime Band Oscillator
idea:    Same regime filter + Bollinger Bands; bull: buy lower band touch; bear: sell upper band touch; sideways: wider quantile extremes.
"""
class CustomStrategy(SimpleAlgorithm):
    sideways_buffer = 0.02
    adx_exit = 12
    atr_stop_mult = 2.5


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        ma200 = self.feat.sma(close, timeperiod=200)
        ratio = close / ma200
        warmup = ma200 > 0

        bull = warmup & (ratio > 1 + self.sideways_buffer)
        bear = warmup & (ratio < 1 - self.sideways_buffer)
        sideways = warmup & ~bull & ~bear

        upper, mid, lower = self.feat.bbands(close, timeperiod=20, nbdevup=2.0, nbdevdn=2.0)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        atr = self.feat.atr(high, low, close, timeperiod=14)

        lower_q = self.feat.rolling_quantile(close, window=20, q=0.1)
        upper_q = self.feat.rolling_quantile(close, window=20, q=0.9)

        trailing_high = self.feat.rolling_max(high, window=10)
        trailing_low = self.feat.rolling_min(low, window=10)
        no_long_stop = close >= trailing_high - self.atr_stop_mult * atr
        no_short_stop = close <= trailing_low + self.atr_stop_mult * atr
        trailing_stop = (
            (close < trailing_high - self.atr_stop_mult * atr) |
            (close > trailing_low + self.atr_stop_mult * atr)
        )

        dip_long = bull & (close < lower) & (adx_val > self.adx_exit) & no_long_stop
        rally_short = bear & (close > upper) & (adx_val > self.adx_exit) & no_short_stop
        mr_long = sideways & (close < lower_q) & (adx_val > self.adx_exit) & no_long_stop
        mr_short = sideways & (close > upper_q) & (adx_val > self.adx_exit) & no_short_stop

        long_setup = dip_long | mr_long
        short_setup = rally_short | mr_short
        exit_setup = (
            self.op.crossed_above(close, mid) |
            self.op.crossed_below(close, mid) |
            self.op.crossed_above(close, lower_q) |
            self.op.crossed_below(close, upper_q) |
            (adx_val < self.adx_exit) |
            trailing_stop
        )

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

