"""
name:    MACross10_30
summary: Long when MA10 crosses above MA30
idea:    Medium-term trend crossover system
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close

        fast_mean = self.feat.rolling_mean(close, window=10)
        slow_mean = self.feat.rolling_mean(close, window=30)

        long_setup = self.op.crossed_above(fast_mean, slow_mean)
        short_setup = self.op.crossed_below(fast_mean, slow_mean)
        exit_setup = self.op.crossed_below(fast_mean, slow_mean) | self.op.crossed_above(fast_mean, slow_mean)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
