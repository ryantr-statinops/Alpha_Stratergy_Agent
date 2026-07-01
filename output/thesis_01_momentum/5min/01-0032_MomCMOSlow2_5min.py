
"""
name:    MomCMOSlow2_5min
summary: CMO: CMO(14) — 5min
thesis:  momentum | 5min
idea:    CMO momentum oscillator
"""
class CustomStrategy(SimpleAlgorithm):

    cmo_window = 14

    def __algorithm__(self):
        close = self.data.pv_close

        cmo = self.feat.cmo(close, timeperiod=self.cmo_window)

        long_setup = cmo > 0
        short_setup = cmo < 0
        exit_setup = self.op.crossed_below(cmo, 0) | self.op.crossed_above(cmo, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
