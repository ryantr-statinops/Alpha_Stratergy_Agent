"""
name:    VnLargeObvTrendConfirm
summary: Long large caps where OBV confirms the price uptrend.
idea:    On-Balance Volume rising above its EMA confirms that price gains
         are backed by genuine accumulation. This filters bull traps where
         price rises on thin volume. Exit when OBV loses its trend.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        ema_slow = self.feat.ema(close, timeperiod=30)
        obv_val = self.feat.obv(close, volume)
        obv_ema = self.feat.ema(obv_val, timeperiod=20)
        obv_rising = self.op.fillna(self.op.pct_change(obv_val, periods=5), 0)

        known = (
            self.op.notna(ema_slow)
            & self.op.notna(obv_val)
            & self.op.notna(obv_ema)
            & (close > 0)
        )

        base_long = known & (obv_val > obv_ema) & (close > ema_slow)
        strong_long = base_long & (obv_rising > 0)
        exit_setup = known & ((obv_val < obv_ema) | (close < ema_slow))

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_long, position=0.5)
        self.set_positions(strong_long, position=1)
