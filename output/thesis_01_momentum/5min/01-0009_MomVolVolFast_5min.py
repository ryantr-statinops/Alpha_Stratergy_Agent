
"""
name:    MomVolVolFast_5min
summary: Momentum+Volume: ROC(8) + volume surge — 5min
thesis:  momentum | 5min
idea:    Momentum + volume confirmation
"""
class CustomStrategy(SimpleAlgorithm):

    roc_window = 8
    vol_window = 14

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        roc = self.feat.roc(close, timeperiod=self.roc_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        long_setup = (roc > 0) & (volume > vol_sma)
        short_setup = (roc < 0) & (volume > vol_sma)
        exit_setup = self.op.crossed_below(roc, 0) | self.op.crossed_above(roc, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
