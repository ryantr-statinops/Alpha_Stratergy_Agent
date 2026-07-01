"""
name:    MACross5_20
summary: Short when MA5 crosses below MA20
idea:    Trend reversal capture with fast/slow moving average crossover
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close

        fast_mean = self.feat.rolling_mean(close, window=5)
        slow_mean = self.feat.rolling_mean(close, window=20)

        long_setup = self.op.crossed_above(fast_mean, slow_mean)
        short_setup = self.op.crossed_below(fast_mean, slow_mean)
        exit_setup = self.op.crossed_below(fast_mean, slow_mean) | self.op.crossed_above(fast_mean, slow_mean)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
