
"""
name:    MomCascF20M40S40_30min
summary: Cascade: ROC(20)>ROC(40)>ROC(40) — 30min
thesis:  momentum | 30min
idea:    Momentum acceleration
"""
class CustomStrategy(SimpleAlgorithm):

    fast_window = 20
    mid_window = 40
    slow_window = 40

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
