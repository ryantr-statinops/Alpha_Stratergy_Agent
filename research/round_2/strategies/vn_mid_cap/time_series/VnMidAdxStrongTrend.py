"""
name:    VnMidAdxStrongTrend
summary: Long mid caps only when ADX confirms a directional trend.
idea:    Mid-cap moves are steep but choppy markets are dangerous. Requiring
         ADX above the entry threshold with +DI above -DI and price above the
         slow average trades only the strongest directional waves. Exit when
         trend strength fades below the exit threshold.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        plus_di = self.feat.plus_di(high, low, close, timeperiod=14)
        minus_di = self.feat.minus_di(high, low, close, timeperiod=14)
        ema_slow = self.feat.ema(close, timeperiod=30)

        known = (
            self.op.notna(adx_val)
            & self.op.notna(plus_di)
            & self.op.notna(minus_di)
            & self.op.notna(ema_slow)
            & (close > 0)
        )

        weak_long = known & (adx_val > 22) & (plus_di > minus_di) & (close > ema_slow)
        strong_long = weak_long & (adx_val > 25)
        exit_setup = known & ((adx_val < 18) | (close < ema_slow))

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)