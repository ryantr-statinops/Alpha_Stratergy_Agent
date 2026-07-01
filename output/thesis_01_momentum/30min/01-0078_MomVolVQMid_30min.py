
"""
name:    MomVolVQMid_30min
summary: Momentum+Volume: ROC(40) + volume Q80 — 30min
thesis:  momentum | 30min
idea:    Momentum + volume quantile
"""
class CustomStrategy(SimpleAlgorithm):

    roc_window = 40
    vol_window = 26

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        roc = self.feat.roc(close, timeperiod=self.roc_window)
        vol_q80 = self.feat.rolling_quantile(volume, self.vol_window, 0.80)

        long_setup = (roc > 0) & (volume > vol_q80)
        short_setup = (roc < 0) & (volume > vol_q80)
        exit_setup = self.op.crossed_below(roc, 0) | self.op.crossed_above(roc, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
