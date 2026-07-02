"""
name:    T05-B_r8
summary: VN30 Momentum Confirmation
idea:    Require both futures and VN30 index momentum in the same direction for aligned entries.
"""
class CustomStrategy(SimpleAlgorithm):
    roc_window = 8
    thesis_group = "05"

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close

        fut_roc = self.feat.roc(close, timeperiod=self.roc_window)
        vn30_roc = self.feat.roc(vn30_close, timeperiod=self.roc_window)

        long_setup = (fut_roc > 0) & (vn30_roc > 0)
        short_setup = (fut_roc < 0) & (vn30_roc < 0)
        exit_setup = self.op.crossed_below(fut_roc, 0) | self.op.crossed_above(fut_roc, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

