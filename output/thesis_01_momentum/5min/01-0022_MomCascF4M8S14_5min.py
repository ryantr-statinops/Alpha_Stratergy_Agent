
"""
name:    MomCascF4M8S14_5min
summary: Cascade: ROC(4)>ROC(8)>ROC(14) — 5min
thesis:  momentum | 5min
idea:    Momentum acceleration
"""
class CustomStrategy(SimpleAlgorithm):

    fast_window = 4
    mid_window = 8
    slow_window = 14

    def __algorithm__(self):
        close = self.data.pv_close

        roc_fast = self.feat.roc(close, timeperiod=self.fast_window)
        roc_mid = self.feat.roc(close, timeperiod=self.mid_window)
        roc_slow = self.feat.roc(close, timeperiod=self.slow_window)

        long_setup = (roc_fast > roc_mid) & (roc_mid > roc_slow) & (roc_slow > 0)
        short_setup = (roc_fast < roc_mid) & (roc_mid < roc_slow) & (roc_slow < 0)
        exit_setup = self.op.crossed_below(roc_fast, 0) | self.op.crossed_above(roc_fast, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
