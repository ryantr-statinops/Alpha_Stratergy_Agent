"""
name:    VNFutureMorningOpenTimes
summary: Trade futures only during the morning session open times.
idea:    The strategy is allowed to open positions only at the listed
         morning timestamps, then manages exits normally after entry.
"""


class CustomStrategy(SimpleAlgorithm):
    # Allow new positions only at these exact morning timestamps.
    position_open_times = [
        "02:00", "02:05", "02:10", "02:15", "02:20", "02:25", "02:30", "02:35", "02:40", "02:45", "02:50", "02:55",
        "03:00", "03:05", "03:10", "03:15", "03:20", "03:25", "03:30", "03:35", "03:40", "03:45", "03:50", "03:55"
    ]

    def __algorithm__(self):
        # Pull the core futures series into short names so the signal logic stays readable.
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        # MACD gives direction, ADX checks trend strength, and volume confirms participation.
        macd, macd_signal, _hist = self.feat.macd(
            close,
            fastperiod=12,
            slowperiod=26,
            signalperiod=9,
        )
        adx = self.feat.adx(high, low, close, timeperiod=14)
        volume_base = self.feat.sma(volume, timeperiod=20)

        # Long only when trend is bullish, strength is enough, and volume is supportive.
        long_setup = (macd > macd_signal) & (adx > 18) & (volume > volume_base)

        # Exit when trend strength fades.
        exit_setup = adx < 14

        # Apply exit first so the entry signal can override when it is valid.
        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)