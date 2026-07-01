"""
name:    MeanLevel14
summary: Long when close > rolling_mean(14)
idea:    Basic mean reversion with 14-period rolling average
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close

        mean = self.feat.rolling_mean(close, window=14)

        long_setup = close > mean
        short_setup = close < mean
        exit_setup = self.op.crossed_below(close, mean) | self.op.crossed_above(close, mean)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
