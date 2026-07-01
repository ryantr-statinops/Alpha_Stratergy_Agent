"""
name:    Q20ADX
summary: Long when close > Q80(20) and ADX > 20
idea:    Quantile breakout with trend strength filter
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        upper = self.feat.rolling_quantile(close, 20, 0.8)
        lower = self.feat.rolling_quantile(close, 20, 0.2)
        adx = self.feat.adx(high, low, close, timeperiod=14)
        

        long_setup = (close > upper) & (adx > 20)
        short_setup = (close < lower) & (adx > 20)
        exit_long = self.op.crossed_below(close, upper) | adx < 15
        exit_short = self.op.crossed_above(close, lower) | adx < 15
        exit_setup = exit_long | exit_short

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
