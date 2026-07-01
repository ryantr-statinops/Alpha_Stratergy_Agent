
"""
name:    XMRelFastSlow_15min
summary: Relative: Ratio(10/34) — 15min
thesis:  cross_market | 15min
idea:    Cross-market relative strength
"""
class CustomStrategy(SimpleAlgorithm):

    roc_window = 10
    sma_window = 34

    return_window = 5
    return_threshold = 0.0002
    position_close_after_n_candles = 24

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        ratio = close / vn30_close
        ratio_sma = self.feat.sma(ratio, timeperiod=self.sma_window)
        ratio_roc = self.feat.roc(ratio, timeperiod=self.roc_window)

        long_setup = ((ratio > ratio_sma) & (ratio_roc > 0)) & (return_roll > 0)
        short_setup = ((ratio < ratio_sma) & (ratio_roc < 0)) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(ratio, ratio_sma) | self.op.crossed_above(ratio, ratio_sma)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
