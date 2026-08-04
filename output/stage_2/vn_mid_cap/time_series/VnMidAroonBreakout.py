"""
name:    VnMidAroonBreakout
summary: Long mid caps when Aroon-up confirms a fresh breakout.
idea:    Mid-cap trend waves are steep and persistent; a high Aroon-up reading
         near the 14-day high flags a fresh directional push above the slow
         average. Exit when price loses the average or Aroon-up decays.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        aroon_down, aroon_up = self.feat.aroon(high, low, timeperiod=14)
        ema_slow = self.feat.ema(close, timeperiod=30)

        known = (
            self.op.notna(aroon_up)
            & self.op.notna(aroon_down)
            & self.op.notna(ema_slow)
            & (close > 0)
        )

        weak_long = known & (aroon_up > 70) & (close > ema_slow)
        strong_long = weak_long & (aroon_up > 85)
        exit_setup = known & ((close < ema_slow) | (aroon_up < 50))

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)