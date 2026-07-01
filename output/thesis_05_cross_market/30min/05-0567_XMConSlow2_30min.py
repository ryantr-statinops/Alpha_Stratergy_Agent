
"""
name:    XMConSlow2_30min
summary: Consensus: Consensus(28) — 30min
thesis:  cross_market | 30min
idea:    3-market consensus signal
"""
class CustomStrategy(SimpleAlgorithm):

    roc_window = 28

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        dji_close = self.data.pv_dji_close

        fut_roc = self.feat.roc(close, timeperiod=self.roc_window)
        vn30_roc = self.feat.roc(vn30_close, timeperiod=self.roc_window)
        dji_roc = self.feat.roc(dji_close, timeperiod=self.roc_window)

        bullish = (fut_roc > 0) & (vn30_roc > 0) & (dji_roc > 0)
        bearish = (fut_roc < 0) & (vn30_roc < 0) & (dji_roc < 0)

        long_setup = bullish
        short_setup = bearish
        exit_setup = (~bullish) & (~bearish)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
