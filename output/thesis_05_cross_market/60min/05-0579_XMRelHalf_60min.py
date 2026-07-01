
"""
name:    XMRelHalf_60min
summary: Relative: Ratio(30/60) — 60min
thesis:  cross_market | 60min
idea:    Cross-market relative strength
"""
class CustomStrategy(SimpleAlgorithm):

    roc_window = 30
    sma_window = 60

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close

        ratio = close / vn30_close
        ratio_sma = self.feat.sma(ratio, timeperiod=self.sma_window)
        ratio_roc = self.feat.roc(ratio, timeperiod=self.roc_window)

        long_setup = (ratio > ratio_sma) & (ratio_roc > 0)
        short_setup = (ratio < ratio_sma) & (ratio_roc < 0)
        exit_setup = self.op.crossed_below(ratio, ratio_sma) | self.op.crossed_above(ratio, ratio_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
