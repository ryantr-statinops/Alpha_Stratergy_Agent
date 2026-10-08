"""
name:    VnMidObvTrendConfirm
summary: Long mid caps when on-balance volume confirms the price trend.
idea:    Price moves without volume backing often reverse in mid caps. Requiring
         OBV above its own average plus price above the slow average keeps the
         position on moves supported by accumulated flow. Exit when OBV loses
         its average or the price trend breaks.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        obv_val = self.feat.obv(close, volume)
        obv_ema = self.feat.ema(obv_val, timeperiod=20)
        ema_slow = self.feat.ema(close, timeperiod=30)

        known = (
            self.op.notna(obv_val)
            & self.op.notna(obv_ema)
            & self.op.notna(ema_slow)
            & (close > 0)
        )

        weak_long = known & (obv_val > obv_ema) & (close > ema_slow)
        strong_long = weak_long & self.op.rising(obv_val, 3)
        exit_setup = known & ((obv_val < obv_ema) | (close < ema_slow))

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)