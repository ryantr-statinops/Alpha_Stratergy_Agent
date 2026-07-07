"""
name:    T10-C
summary: Regime Band Oscillator
idea:    Same regime filter + Bollinger Bands; bull: buy lower band touch; bear: sell upper band touch; sideways: wider quantile extremes.
"""
class CustomStrategy(SimpleAlgorithm):
    sideways_buffer = 0.02
    adx_entry = 20
    adx_exit = 15
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

        ma20 = self.feat.sma(close, timeperiod=20)
        upper, mid, lower = self.feat.bbands(close, timeperiod=20, nbdevup=2.0, nbdevdn=2.0)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        atr = self.feat.atr(high, low, close, timeperiod=14)

        lower_q = self.feat.rolling_quantile(close, window=20, q=0.1)
        upper_q = self.feat.rolling_quantile(close, window=20, q=0.9)

        no_long_trend = close >= ma20 - self.atr_stop_mult * atr
        no_short_trend = close <= ma20 + self.atr_stop_mult * atr
        no_long_mr = close >= lower_q - self.atr_stop_mult * atr
        no_short_mr = close <= upper_q + self.atr_stop_mult * atr
        atr_stop = (
            (close < ma20 - self.atr_stop_mult * atr) |
            (close > ma20 + self.atr_stop_mult * atr)
        )

        dip_long = bull & (close < lower) & (adx_val > self.adx_entry) & no_long_trend
        rally_short = bear & (close > upper) & (adx_val > self.adx_entry) & no_short_trend
        mr_long = sideways & (close < lower_q) & (adx_val < self.adx_entry) & no_long_mr
        mr_short = sideways & (close > upper_q) & (adx_val < self.adx_entry) & no_short_mr

        long_setup = dip_long | mr_long
        short_setup = rally_short | mr_short
        exit_setup = (
            self.op.crossed_above(close, mid) |
            self.op.crossed_below(close, mid) |
            (adx_val < self.adx_exit) |
            (adx_val > self.adx_entry) |
            atr_stop
        )

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)

