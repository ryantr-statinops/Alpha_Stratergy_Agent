
"""
name:    MomCascF6M10S20_30min
summary: Cascade: ROC(6)>ROC(10)>ROC(20) — 30min
thesis:  momentum | 30min
idea:    Momentum acceleration
"""
class CustomStrategy(SimpleAlgorithm):

    fast_window = 6
    mid_window = 10
    slow_window = 20

    return_window = 8
    return_threshold = 0.0003
    position_close_after_n_candles = 12
    adx_window = 14

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=14)

        roc_fast = self.feat.roc(close, timeperiod=self.fast_window)
        roc_mid = self.feat.roc(close, timeperiod=self.mid_window)
        roc_slow = self.feat.roc(close, timeperiod=self.slow_window)

        long_setup = (((roc_fast > roc_mid) & (roc_mid > roc_slow) & (roc_slow > 0)) & (return_roll > 0)) & (adx > 22)
        short_setup = (((roc_fast < roc_mid) & (roc_mid < roc_slow) & (roc_slow < 0)) & (return_roll < 0)) & (adx > 22)
        exit_setup = ((self.op.crossed_below(roc_fast, 0) | self.op.crossed_above(roc_fast, 0)) | (abs(return_roll) < self.return_threshold)) | (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
