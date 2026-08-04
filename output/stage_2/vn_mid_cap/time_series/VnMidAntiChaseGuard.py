"""
name:    VnMidAntiChaseGuard
summary: Long mid-cap uptrends but scale down when momentum is overextended.
idea:    Chasing a mid-cap top is the classic way to give back a trend. In an
         uptrend, cut the position to half when RSI is overbought or price has
         risen for four consecutive sessions; keep full size otherwise. Exit
         when the uptrend itself breaks.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close

        ema_slow = self.feat.ema(close, timeperiod=30)
        rsi_val = self.feat.rsi(close, timeperiod=9)

        ret1 = self.op.fillna(self.op.pct_change(close, periods=1), 0)
        ret2 = self.op.fillna(self.op.pct_change(close, periods=2), 0)
        ret3 = self.op.fillna(self.op.pct_change(close, periods=3), 0)
        ret4 = self.op.fillna(self.op.pct_change(close, periods=4), 0)
        up_streak = (ret1 > 0) & (ret2 > 0) & (ret3 > 0) & (ret4 > 0)

        known = (
            self.op.notna(ema_slow)
            & self.op.notna(rsi_val)
            & (close > 0)
        )

        base_long = known & (close > ema_slow)
        chase_guard = (rsi_val > 75) | (up_streak >= 4)

        weak_long = base_long & chase_guard
        strong_long = base_long & ~chase_guard
        exit_setup = known & (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
