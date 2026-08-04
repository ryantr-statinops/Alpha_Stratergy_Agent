"""
name:    VnMidBreakoutVolume
summary: Long mid caps on a 20-day high breakout confirmed by volume.
idea:    Mid-cap breakouts above the 20-day high succeed about 65% of the time
         when volume exceeds twice the 20-day volume average. Volume is a
         confirmation, not a stand-alone signal. Exit when price loses the
         slow average.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        volume = self.data.pv_volume

        upper_high = self.op.shift(self.feat.rolling_max(high, window=20), periods=1)
        vol_sma = self.feat.sma(volume, timeperiod=20)
        ema_slow = self.feat.ema(close, timeperiod=30)

        known = (
            self.op.notna(upper_high)
            & self.op.notna(vol_sma)
            & self.op.notna(ema_slow)
            & (close > 0)
            & (volume > 0)
            & (vol_sma > 0)
        )

        base_long = known & (close > upper_high) & (close > ema_slow)
        strong_long = base_long & (volume > vol_sma * 2.0)
        exit_setup = known & (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_long, position=0.5)
        self.set_positions(strong_long, position=1)