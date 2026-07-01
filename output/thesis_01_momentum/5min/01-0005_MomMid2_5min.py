
"""
name:    MomMid2_5min
summary: Momentum: ROC(14) strength-2 — 5min
thesis:  momentum | 5min
idea:    ROC momentum with 2-period smoothing
"""
class CustomStrategy(SimpleAlgorithm):

    roc_window = 14

    return_window = 3
    return_threshold = 0.0001
    position_close_after_n_candles = 72

    def __algorithm__(self):
        close = self.data.pv_close
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        roc = self.feat.roc(close, timeperiod=self.roc_window)
        roc_smooth = self.feat.sma(roc, timeperiod=2)

        long_setup = (roc_smooth > 0) & (return_roll > 0)
        short_setup = (roc_smooth < 0) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(roc_smooth, 0) | self.op.crossed_above(roc_smooth, 0)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
