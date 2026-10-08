"""
name:    VnLargeTrendVolume824
summary: Long large caps in an 8/24 EMA uptrend with volume confirmation.
idea:    An 8-day EMA above the 24-day EMA marks a persistent short-term trend
         in a large cap. Holding only while price is above the slow EMA and
         scaling up when volume confirms participation captures the retail
         herding tendency without chasing speculative moves.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)
        vol_base = self.feat.sma(volume, timeperiod=10)

        base_entry = (close > ema_slow) & (ema_fast > ema_slow)
        strong_entry = base_entry & (volume > vol_base)
        exit_setup = (close < ema_slow) | (ema_fast < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
