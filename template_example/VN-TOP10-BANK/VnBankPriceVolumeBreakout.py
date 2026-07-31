"""
name:    VnBankPriceVolumeBreakout
summary: Enter long when price breaks above trend with volume
         confirmation.
idea:    A breakout is more reliable when price is above its slower trend
         and volume expands. The strategy stays flat when the move loses
         momentum.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # Pull only price and volume series into short names.
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        # Use a trend pair and a participation filter.
        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=40)
        volume_base = self.feat.sma(volume, timeperiod=20)
        atr = self.feat.atr(high, low, close, timeperiod=14)

        # Use a short momentum filter to confirm the breakout is happening now.
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)

        # Long only when trend, momentum, volume, and range all support the move.
        long_setup = (
            (close > ema_slow)
            & (ema_fast > ema_slow)
            & (return_1 > 0)
            & (volume > volume_base)
            & (atr > 0)
        )

        # Exit when the fast trend loses the slow trend or momentum turns negative.
        exit_setup = (ema_fast < ema_slow) | (return_1 < 0)

        # Apply exits first so the long signal can override when conditions hold.
        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)