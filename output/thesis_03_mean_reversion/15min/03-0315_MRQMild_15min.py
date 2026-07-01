
"""
name:    MRQMild_15min
summary: Quantile Rev: Q85%/Q15%(26) — 15min
thesis:  mean_reversion | 15min
idea:    Quantile extreme reversion
"""
class CustomStrategy(SimpleAlgorithm):

    q_window = 26

    def __algorithm__(self):
        close = self.data.pv_close

        upper = self.feat.rolling_quantile(close, self.q_window, 0.90)
        lower = self.feat.rolling_quantile(close, self.q_window, 0.10)

        long_setup = close < lower
        short_setup = close > upper
        exit_setup = self.op.crossed_above(close, lower) | self.op.crossed_below(close, upper)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
