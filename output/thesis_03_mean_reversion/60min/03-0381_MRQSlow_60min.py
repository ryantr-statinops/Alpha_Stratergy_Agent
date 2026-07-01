
"""
name:    MRQSlow_60min
summary: Quantile Rev: Q90%/Q10%(100) — 60min
thesis:  mean_reversion | 60min
idea:    Quantile extreme reversion
"""
class CustomStrategy(SimpleAlgorithm):

    q_window = 100
    q_high = 0.9
    q_low = 0.1

    def __algorithm__(self):
        close = self.data.pv_close

        upper = self.feat.rolling_quantile(close, self.q_window, self.q_high)
        lower = self.feat.rolling_quantile(close, self.q_window, self.q_low)

        long_setup = close < lower
        short_setup = close > upper
        exit_setup = self.op.crossed_above(close, lower) | self.op.crossed_below(close, upper)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
