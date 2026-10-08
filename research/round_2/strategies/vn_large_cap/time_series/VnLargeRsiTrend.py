"""
name:    VnLargeRsiTrend
summary: Long large caps with RSI7 recovery over a rising 7/21 EMA trend.
idea:    The stock-template recovery profile uses RSI above 48 with a fast 7/21
         trend, while RSI below 42 marks failed momentum. Volume above SMA10
         confirms full exposure without becoming a daily exit condition.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        ema_fast = self.feat.ema(close, timeperiod=7)
        ema_slow = self.feat.ema(close, timeperiod=21)
        rsi = self.feat.rsi(close, timeperiod=7)
        volume_base = self.feat.sma(volume, timeperiod=10)

        base_entry = (rsi > 48) & (ema_fast > ema_slow)
        strong_entry = base_entry & (rsi < 70) & (close > ema_slow) & (volume > volume_base)
        exit_setup = (rsi < 42) | (ema_fast < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
