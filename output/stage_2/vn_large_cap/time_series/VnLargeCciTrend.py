"""
name:    VnLargeCciTrend
summary: Long large caps when CCI confirms strong momentum in an uptrend.
idea:    CCI crossing above +100 signals the start of a strong directional
         move in large caps. Combined with an EMA uptrend filter, this
         captures the acceleration phase of established trends.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        ema_slow = self.feat.ema(close, timeperiod=30)
        cci_val = self.feat.cci(high, low, close, timeperiod=20)

        known = (
            self.op.notna(ema_slow)
            & self.op.notna(cci_val)
            & (close > 0)
        )

        base_long = known & (cci_val > 100) & (close > ema_slow)
        strong_long = base_long & (cci_val > 150)
        exit_setup = known & ((cci_val < 0) | (close < ema_slow))

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_long, position=0.5)
        self.set_positions(strong_long, position=1)
