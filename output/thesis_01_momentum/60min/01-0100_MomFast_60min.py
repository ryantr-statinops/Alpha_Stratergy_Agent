
"""
name:    MomFast_60min
summary: Momentum: ROC(30) — 60min
thesis:  momentum | 60min
idea:    Pure momentum: ROC direction
"""
class CustomStrategy(SimpleAlgorithm):

    roc_window = 30

    def __algorithm__(self):
        close = self.data.pv_close

        roc = self.feat.roc(close, timeperiod=self.roc_window)

        long_setup = roc > 0
        short_setup = roc < 0
        exit_setup = self.op.crossed_below(roc, 0) | self.op.crossed_above(roc, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
