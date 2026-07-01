
"""
name:    XMDJIXSlow_15min
summary: DJI: DJI(52) — 15min
thesis:  cross_market | 15min
idea:    Global momentum spillover
"""
class CustomStrategy(SimpleAlgorithm):

    roc_window = 52

    return_window = 5
    return_threshold = 0.0002
    position_close_after_n_candles = 24

    def __algorithm__(self):
        close = self.data.pv_close
        dji_close = self.data.pv_dji_close
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        dji_roc = self.feat.roc(dji_close, timeperiod=self.roc_window)
        fut_roc = self.feat.roc(close, timeperiod=self.roc_window)

        long_setup = ((dji_roc > 0) & (fut_roc > 0)) & (return_roll > 0)
        short_setup = ((dji_roc < 0) & (fut_roc < 0)) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(fut_roc, 0) | self.op.crossed_above(fut_roc, 0)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
