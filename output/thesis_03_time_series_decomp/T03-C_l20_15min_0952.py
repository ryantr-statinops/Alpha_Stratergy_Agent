"""
name:    T03-C_l20
summary: LinReg Slope Trend
idea:    Trade linear regression slope direction with angle filter and price-forecast gap for entry timing.
"""
class CustomStrategy(SimpleAlgorithm):
    lr_window = 20
    thesis_group = "03"

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        slope = self.feat.linearreg_slope(close, timeperiod=self.lr_window)
        angle = self.feat.linearreg_angle(close, timeperiod=self.lr_window)
        forecast = self.feat.tsf(close, timeperiod=self.lr_window)
        adx_val = self.feat.adx(high, low, close, timeperiod=10)

        long_setup = (slope > 0) & (angle > 5) & (close < forecast) & (adx_val > 22)
        short_setup = (slope < 0) & (angle < -5) & (close > forecast) & (adx_val > 22)
        exit_setup = self.op.crossed_below(slope, 0) | self.op.crossed_above(slope, 0) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

