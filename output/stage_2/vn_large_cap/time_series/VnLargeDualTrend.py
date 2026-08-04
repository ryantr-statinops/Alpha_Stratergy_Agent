"""
name:    VnLargeDualTrend
summary: Long large caps confirmed by two stacked EMA regimes.
idea:    Requiring both the fast 8/24 and slow 12/36 EMA pairs to be aligned
         filters out single-indicator whipsaws. The dual confirmation keeps the
         book long only when the short and medium trends agree, and the slow
         pair governs the exit so the position is not shaken out early.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_mid = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=24)
        ema_base = self.feat.ema(close, timeperiod=36)

        base_entry = (ema_fast > ema_slow) & (ema_mid > ema_base)
        strong_entry = base_entry & (close > ema_base)
        exit_setup = (ema_fast < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
