
"""
name:    MomFast_60min
summary: Momentum: ROC(30) — 60min
thesis:  momentum | 60min
idea:    Pure momentum: ROC direction
"""
class CustomStrategy(SimpleAlgorithm):

    roc_window = 30

    return_window = 14
    return_threshold = 0.0005
    position_close_after_n_candles = 6

    def __algorithm__(self):
        close = self.data.pv_close
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        roc = self.feat.roc(close, timeperiod=self.roc_window)

        long_setup = (roc > 0) & (return_roll > 0)
        short_setup = (roc < 0) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(roc, 0) | self.op.crossed_above(roc, 0)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
