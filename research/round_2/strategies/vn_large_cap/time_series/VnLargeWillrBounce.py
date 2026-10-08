"""
name:    VnLargeWillrBounce
summary: Long large caps when Williams %R bounces from oversold in uptrend.
idea:    Williams %R recovering from the -80 oversold zone within a confirmed
         uptrend captures mean-reversion bounces in large caps. The indicator
         is sensitive to short-term extremes while the EMA filter keeps
         trades aligned with the broader trend.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        ema_slow = self.feat.ema(close, timeperiod=30)
        willr_val = self.feat.willr(high, low, close, timeperiod=14)
        willr_rising = self.op.fillna(self.op.pct_change(willr_val, periods=3), 0)

        known = (
            self.op.notna(ema_slow)
            & self.op.notna(willr_val)
            & (close > 0)
        )

        base_long = known & (willr_val > -50) & (willr_val < -20) & (close > ema_slow)
        strong_long = base_long & (willr_rising > 0)
        exit_setup = known & ((willr_val < -80) | (close < ema_slow))

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_long, position=0.5)
        self.set_positions(strong_long, position=1)
