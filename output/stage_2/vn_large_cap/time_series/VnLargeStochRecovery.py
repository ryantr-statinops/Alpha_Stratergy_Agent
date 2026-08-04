"""
name:    VnLargeStochRecovery
summary: Long large caps with Stochastic K/D crossover from oversold in uptrend.
idea:    Stochastic K crossing above D in the oversold zone (< 30) within
         a confirmed uptrend captures the momentum recovery after a
         short-term pullback. Large caps bounce reliably from these levels.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        ema_slow = self.feat.ema(close, timeperiod=30)
        slow_k, slow_d = self.feat.stoch(high, low, close, fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

        known = (
            self.op.notna(ema_slow)
            & self.op.notna(slow_k)
            & self.op.notna(slow_d)
            & (close > 0)
        )

        base_long = known & (slow_k > slow_d) & (slow_k < 30) & (close > ema_slow)
        strong_long = base_long & (slow_k < 20)
        exit_setup = known & ((slow_k > 80) | (close < ema_slow))

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_long, position=0.5)
        self.set_positions(strong_long, position=1)
