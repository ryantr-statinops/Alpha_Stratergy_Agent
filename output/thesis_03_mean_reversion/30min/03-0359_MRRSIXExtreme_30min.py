
"""
name:    MRRSIXExtreme_30min
summary: RSI Rev: RSI(15/85) — 30min
thesis:  mean_reversion | 30min
idea:    RSI extreme mean reversion
"""
class CustomStrategy(SimpleAlgorithm):

    rsi_window = 14
    rsi_low = 15
    rsi_high = 85

    def __algorithm__(self):
        close = self.data.pv_close

        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)

        long_setup = rsi < self.rsi_low
        short_setup = rsi > self.rsi_high
        exit_setup = self.op.crossed_above(rsi, 50) | self.op.crossed_below(rsi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
