"""
name:    VnMidEmaTrendRide
summary: Long mid caps riding a 10/30 EMA golden cross uptrend.
idea:    Mid-cap uptrends climb steadily for 20-45 sessions. A fast EMA stacked
         above the slow average plus a positive daily return confirms momentum;
         a close below the slow average ends the trend. Sizing scales with the
         fast average sitting above the slow average.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close

        ema_fast = self.feat.ema(close, timeperiod=10)
        ema_slow = self.feat.ema(close, timeperiod=30)
        ret_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)

        known = self.op.notna(ema_fast) & self.op.notna(ema_slow) & (close > 0)

        weak_long = known & (close > ema_slow) & (ret_1 > 0)
        strong_long = weak_long & (ema_fast > ema_slow)
        exit_setup = known & (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)