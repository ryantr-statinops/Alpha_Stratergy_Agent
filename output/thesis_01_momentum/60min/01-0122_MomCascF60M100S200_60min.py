
"""
name:    MomCascF60M100S200_60min
summary: Cascade: ROC(60)>ROC(100)>ROC(200) — 60min
thesis:  momentum | 60min
idea:    Momentum acceleration
"""
class CustomStrategy(SimpleAlgorithm):

    fast_window = 60
    mid_window = 100
    slow_window = 200

    return_window = 14
    return_threshold = 0.0005
    position_close_after_n_candles = 6

    def __algorithm__(self):
        close = self.data.pv_close
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        roc_fast = self.feat.roc(close, timeperiod=self.fast_window)
        roc_mid = self.feat.roc(close, timeperiod=self.mid_window)
        roc_slow = self.feat.roc(close, timeperiod=self.slow_window)

        long_setup = ((roc_fast > roc_mid) & (roc_mid > roc_slow) & (roc_slow > 0)) & (return_roll > 0)
        short_setup = ((roc_fast < roc_mid) & (roc_mid < roc_slow) & (roc_slow < 0)) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(roc_fast, 0) | self.op.crossed_above(roc_fast, 0)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
