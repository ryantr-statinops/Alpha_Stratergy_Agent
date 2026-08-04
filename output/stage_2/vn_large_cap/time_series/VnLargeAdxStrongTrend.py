"""
name:    VnLargeAdxStrongTrend
summary: Long large caps when ADX confirms directional strength in an uptrend.
idea:    ADX filters out choppy sideways markets where false breakouts are
         common in large caps. Only entering when ADX > 22 and +DI > -DI
         ensures the trade rides a genuine directional move.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        ema_slow = self.feat.ema(close, timeperiod=30)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        plus_di = self.feat.plus_di(high, low, close, timeperiod=14)
        minus_di = self.feat.minus_di(high, low, close, timeperiod=14)
        adx_rising = self.op.fillna(self.op.pct_change(adx_val, periods=3), 0)

        known = (
            self.op.notna(ema_slow)
            & self.op.notna(adx_val)
            & self.op.notna(plus_di)
            & self.op.notna(minus_di)
            & (close > 0)
        )

        base_long = known & (adx_val > 22) & (plus_di > minus_di) & (close > ema_slow)
        strong_long = base_long & (adx_rising > 0)
        exit_setup = known & (adx_val < 18)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_long, position=0.5)
        self.set_positions(strong_long, position=1)
