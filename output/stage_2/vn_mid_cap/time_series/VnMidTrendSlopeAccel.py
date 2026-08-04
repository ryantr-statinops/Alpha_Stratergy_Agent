"""
name:    VnMidTrendSlopeAccel
summary: Long mid caps on a rising linear-regression trend slope.
idea:    A positive and accelerating linear-regression slope captures the steep
         directional waves of mid caps. Requiring the slope above zero and the
         strong state on the slope rising over three bars filters acceleration.
         Exit when the slope rolls over or price loses the slow average.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close

        slope = self.feat.linearreg_slope(close, timeperiod=14)
        ema_slow = self.feat.ema(close, timeperiod=30)

        known = self.op.notna(slope) & self.op.notna(ema_slow) & (close > 0)

        weak_long = known & (slope > 0) & (close > ema_slow)
        strong_long = weak_long & self.op.rising(slope, 3)
        exit_setup = known & ((slope < 0) | (close < ema_slow))

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)