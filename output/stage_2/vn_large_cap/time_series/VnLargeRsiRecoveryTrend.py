"""
name:    VnLargeRsiRecoveryTrend
summary: Long large caps with RSI recovery over an EMA uptrend.
idea:    Large caps show mean-reversion bounces when RSI recovers from
         oversold within a confirmed uptrend. RSI7 crossing above 48
         signals the pullback is over while EMA stacking confirms the
         broader trend is still intact.
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

        base_long = known & (rsi_val > 48) & (close > ema_fast) & (ema_fast > ema_slow)
        strong_long = base_long & (rsi_val > 55)
        exit_setup = known & ((rsi_val < 42) | (close < ema_slow))

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_long, position=0.5)
        self.set_positions(strong_long, position=1)
