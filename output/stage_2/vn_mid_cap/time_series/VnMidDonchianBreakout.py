"""
name:    VnMidDonchianBreakout
summary: Long mid caps on a 20-day Donchian breakout inside an uptrend.
idea:    Mid caps show the strongest trend persistence on the market with
         reliable breakouts above 20-day highs. Entry requires price above the
         slow average so a channel breakout is not caught in a downtrend.
         Exit on a close below the 20-day low of the channel.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        upper_channel = self.op.shift(self.feat.rolling_max(high, window=20), periods=1)
        lower_channel = self.op.shift(self.feat.rolling_min(low, window=20), periods=1)
        ema_slow = self.feat.ema(close, timeperiod=30)

        known = (
            self.op.notna(upper_channel)
            & self.op.notna(lower_channel)
            & self.op.notna(ema_slow)
            & (close > 0)
        )

        base_long = known & (close > upper_channel) & (close > ema_slow)
        exit_setup = known & (close < lower_channel)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_long, position=1)
