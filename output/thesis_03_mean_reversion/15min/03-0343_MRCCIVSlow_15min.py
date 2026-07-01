
"""
name:    MRCCIVSlow_15min
summary: CCI: CCI(78) — 15min
thesis:  mean_reversion | 15min
idea:    CCI extreme reversion
"""
class CustomStrategy(SimpleAlgorithm):

    cci_window = 78

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        cci = self.feat.cci(high, low, close, timeperiod=self.cci_window)

        long_setup = cci < -100
        short_setup = cci > 100
        exit_setup = self.op.crossed_above(cci, 0) | self.op.crossed_below(cci, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
