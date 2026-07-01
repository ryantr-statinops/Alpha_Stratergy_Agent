
"""
name:    MomCMOMid_60min
summary: CMO: CMO(60) — 60min
thesis:  momentum | 60min
idea:    CMO momentum oscillator
"""
class CustomStrategy(SimpleAlgorithm):

    cmo_window = 60

    return_window = 14
    return_threshold = 0.0005
    position_close_after_n_candles = 6

    def __algorithm__(self):
        close = self.data.pv_close
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        cmo = self.feat.cmo(close, timeperiod=self.cmo_window)

        long_setup = (cmo > 0) & (return_roll > 0)
        short_setup = (cmo < 0) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(cmo, 0) | self.op.crossed_above(cmo, 0)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
