
"""
name:    MRQFT_5min
summary: Quantile Rev: Q95%/Q5%(8) — 5min
thesis:  mean_reversion | 5min
idea:    Quantile extreme reversion
"""
class CustomStrategy(SimpleAlgorithm):

    q_window = 8
    q_high = 0.95
    q_low = 0.05

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
