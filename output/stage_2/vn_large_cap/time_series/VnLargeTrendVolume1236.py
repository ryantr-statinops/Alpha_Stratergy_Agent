"""
name:    VnLargeTrendVolume1236
summary: Long large caps in a 12/36 EMA uptrend with stable volume support.
idea:    The 12/36 EMA pair catches a slower, more durable trend than the fast
         8/24 pair. Entry requires price above the 36-day EMA and a rising fast
         EMA; a position is only doubled when turnover clears its stable 20-day
         base, keeping the long in line with institutional participation.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)
        vol_base = self.feat.sma(volume, timeperiod=20)

        base_entry = (close > ema_slow) & (ema_fast > ema_slow)
        strong_entry = base_entry & (volume > vol_base)
        exit_setup = (close < ema_slow) | (ema_fast < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
