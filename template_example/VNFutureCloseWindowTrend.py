"""
name:    VNFutureCloseWindowTrend
summary: Trade futures with fixed close windows at 07:20-07:50.
idea:    The strategy can manage entries normally, but any open position
         is forced flat inside the configured close ranges.
"""


class CustomStrategy(SimpleAlgorithm):
    # Force close positions inside these time windows.
    position_close_ranges = [
        "07:20-07:50",
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