
"""
name:    MRBBXExtreme_30min
summary: BBands Rev: BBands(4STD) — 30min
thesis:  mean_reversion | 30min
idea:    Bollinger Band reversion
"""
class CustomStrategy(SimpleAlgorithm):

    bbands_window = 40
    nbdev = 4

    return_window = 8
    return_threshold = 0.0003
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        upper, mid_band, lower = self.feat.bbands(
            close, timeperiod=self.bbands_window, nbdevup=self.nbdev, nbdevdn=self.nbdev
        )

        long_setup = (close < lower) & (return_roll > 0)
        short_setup = (close > upper) & (return_roll < 0)
        exit_setup = (self.op.crossed_above(close, mid_band) | self.op.crossed_below(close, mid_band)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
