
"""
name:    MRBBTight_30min
summary: BBands Rev: BBands(2.5STD) — 30min
thesis:  mean_reversion | 30min
idea:    Bollinger Band reversion
"""
class CustomStrategy(SimpleAlgorithm):

    bbands_window = 40

    def __algorithm__(self):
        close = self.data.pv_close

        upper, mid_band, lower = self.feat.bbands(
            close, timeperiod=self.bbands_window, nbdevup=2, nbdevdn=2
        )

        long_setup = close < lower
        short_setup = close > upper
        exit_setup = self.op.crossed_above(close, mid_band) | self.op.crossed_below(close, mid_band)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
