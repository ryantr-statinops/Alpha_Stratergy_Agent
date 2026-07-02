"""
name:    T05-F_r20
summary: Relative Strength Ratio
idea:    Trade futures-to-VN30 ratio trend via SMA, ROC, and linear regression slope.
"""
class CustomStrategy(SimpleAlgorithm):
    rs_window = 20


    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close

        ratio = close / vn30_close
        ratio_sma = self.feat.sma(ratio, timeperiod=self.rs_window)
        ratio_roc = self.feat.roc(ratio, timeperiod=self.rs_window)
        ratio_slope = self.feat.linearreg_slope(ratio, timeperiod=self.rs_window)

        long_setup = (ratio > ratio_sma) & (ratio_roc > 0) & (ratio_slope > 0)
        short_setup = (ratio < ratio_sma) & (ratio_roc < 0) & (ratio_slope < 0)
        exit_setup = self.op.crossed_below(ratio, ratio_sma) | self.op.crossed_above(ratio, ratio_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

