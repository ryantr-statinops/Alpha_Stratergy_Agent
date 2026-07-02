
"""
name:    MomCMOSlow2_15min
summary: CMO: CMO(20) — 15min
thesis:  momentum | 15min
idea:    CMO momentum oscillator
"""
class CustomStrategy(SimpleAlgorithm):

    cmo_window = 20

    return_window = 5
    return_threshold = 0.0002
    position_close_after_n_candles = 24
    adx_window = 10

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=10)

        cmo = self.feat.cmo(close, timeperiod=self.cmo_window)

        long_setup = ((cmo > 0) & (return_roll > 0)) & (adx > 22)
        short_setup = ((cmo < 0) & (return_roll < 0)) & (adx > 22)
        exit_setup = ((self.op.crossed_below(cmo, 0) | self.op.crossed_above(cmo, 0)) | (abs(return_roll) < self.return_threshold)) | (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
