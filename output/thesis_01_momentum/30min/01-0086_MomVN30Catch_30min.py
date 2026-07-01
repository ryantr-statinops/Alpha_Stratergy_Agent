
"""
name:    MomVN30Catch_30min
summary: Momentum+VN30: ROC(mid)+VN30 catch — 30min
thesis:  momentum | 30min
idea:    Catch-up momentum VN30
"""
class CustomStrategy(SimpleAlgorithm):

    roc_window = 40

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close

        roc_fut = self.feat.roc(close, timeperiod=self.roc_window)
        roc_vn30 = self.feat.roc(vn30_close, timeperiod=self.roc_window)

        long_setup = (roc_fut > 0) & (roc_vn30 > 0)
        short_setup = (roc_fut < 0) & (roc_vn30 < 0)
        exit_setup = self.op.crossed_below(roc_fut, 0) | self.op.crossed_above(roc_fut, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
