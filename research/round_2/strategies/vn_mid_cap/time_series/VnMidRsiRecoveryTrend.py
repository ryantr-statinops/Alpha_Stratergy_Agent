"""
name:    VnMidRsiRecoveryTrend
summary: Long mid caps on RSI recovery inside a fast EMA uptrend.
idea:    RSI recovery above 48 after a pullback confirms renewed buying in a
         mid-cap uptrend using the active momentum profile. The exit at RSI
         below 42 adds a hysteresis band so a single noisy bar does not whip
         the position. Exit also when the trend itself breaks.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)
        rsi_val = self.feat.rsi(close, timeperiod=7)

        known = (
            self.op.notna(ema_fast)
            & self.op.notna(ema_slow)
            & self.op.notna(rsi_val)
            & (close > 0)
        )

        weak_long = known & (rsi_val > 48) & (ema_fast > ema_slow) & (close > ema_slow)
        strong_long = weak_long & (rsi_val > 55)
        exit_setup = known & ((rsi_val < 42) | (close < ema_slow))

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)