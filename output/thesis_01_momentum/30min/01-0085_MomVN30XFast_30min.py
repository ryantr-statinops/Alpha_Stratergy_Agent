
"""
name:    MomVN30XFast_30min
summary: Momentum+VN30: ROC(ultra)+VN30 — 30min
thesis:  momentum | 30min
idea:    Ultra-fast VN30 momentum
"""
class CustomStrategy(SimpleAlgorithm):

    roc_window = 10

    return_window = 8
    return_threshold = 0.0003
    position_close_after_n_candles = 12
    adx_window = 14

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=14)

        roc_fut = self.feat.roc(close, timeperiod=self.roc_window)
        roc_vn30 = self.feat.roc(vn30_close, timeperiod=self.roc_window)

        long_setup = (((roc_fut > 0) & (roc_vn30 > 0)) & (return_roll > 0)) & (adx > 22)
        short_setup = (((roc_fut < 0) & (roc_vn30 < 0)) & (return_roll < 0)) & (adx > 22)
        exit_setup = ((self.op.crossed_below(roc_fut, 0) | self.op.crossed_above(roc_fut, 0)) | (abs(return_roll) < self.return_threshold)) | (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
