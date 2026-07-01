"""
name:    Mean14ADX
summary: Long when close > mean(14) and ADX > 20
idea:    Trend strength filter with ADX to avoid sideways markets
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        mean = self.feat.rolling_mean(close, window=14)
        adx = self.feat.adx(high, low, close, timeperiod=14)
        

        long_setup = (close > mean) & (adx > 20)
        short_setup = (close < mean) & (adx > 20)
        exit_long = self.op.crossed_below(close, mean) | adx < 14
        exit_short = self.op.crossed_above(close, mean) | adx < 14
        exit_setup = exit_long | exit_short

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
