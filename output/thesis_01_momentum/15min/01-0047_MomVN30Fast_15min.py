
"""
name:    MomVN30Fast_15min
summary: Momentum+VN30: ROC(13) + VN30 — 15min
thesis:  momentum | 15min
idea:    Cross-market momentum with VN30
"""
class CustomStrategy(SimpleAlgorithm):

    roc_window = 13

    return_window = 5
    return_threshold = 0.0002
    position_close_after_n_candles = 24

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        roc_fut = self.feat.roc(close, timeperiod=self.roc_window)
        roc_vn30 = self.feat.roc(vn30_close, timeperiod=self.roc_window)

        long_setup = ((roc_fut > 0) & (roc_vn30 > 0)) & (return_roll > 0)
        short_setup = ((roc_fut < 0) & (roc_vn30 < 0)) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(roc_fut, 0) | self.op.crossed_above(roc_fut, 0)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
