
"""
name:    XMGapFast_15min
summary: Gap: Gap(Fast+0.2%) — 15min
thesis:  cross_market | 15min
idea:    Tight gap capture
"""
class CustomStrategy(SimpleAlgorithm):

    roc_window = 5

    def __algorithm__(self):
        close = self.data.pv_close
        open_price = self.data.pv_open
        dji_close = self.data.pv_dji_close

        dji_roc = self.feat.roc(dji_close, timeperiod=self.roc_window)
        gap = (open_price / close - 1) * 100
        dji_direction = dji_roc > 0

        long_setup = dji_direction & (gap < 0.5)
        short_setup = (~dji_direction) & (gap > -0.5)
        exit_setup = self.op.crossed_above(gap, 0.5) | self.op.crossed_below(gap, -0.5)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
