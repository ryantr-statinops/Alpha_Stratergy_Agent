"""
name:    VNFutureShortMomentumTrend
summary: Trade futures on short-only momentum confirmation with trend
         strength and a rolling price filter.
idea:    The strategy stays short only when trend, momentum, and recent
         price behavior all point in the same direction. It exits when the
         move loses strength or momentum turns flat.
"""


class CustomStrategy(SimpleAlgorithm):
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

        # Use a rolling return mean as a smoother short-term momentum filter.
        # This reduces sensitivity to a single noisy candle.
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=14)

        # Short only when the trend is bearish, strength is acceptable, volume is supportive,
        # and recent rolling momentum is still negative.
        short_setup = (macd < macd_signal) & (adx > 18) & (volume > volume_base) & (return_roll < 0)

        # Exit when trend strength fades or the rolling momentum turns flat/positive.
        exit_setup = (adx < 14) | (return_roll > 0)

        # Apply exit first so the short signal can override it when conditions are valid.
        self.set_positions(exit_setup, position=0)
        self.set_positions(short_setup, position=-1)