"""
name:    VnBankPriceVolumeTrend
summary: Scale long exposure when price trend, momentum, and volume
         confirm a stronger move.
idea:    Price and volume can still capture a lot of daily stock behavior
         even without fundamentals. A faster trend trigger gives more
         trades, while half size starts the move and full size waits for
         better confirmation.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # Pull only price and volume series into short names.
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        # Use a faster trend pair so the strategy reacts more often.
        ema_fast = self.feat.ema(close, timeperiod=10)
        ema_slow = self.feat.ema(close, timeperiod=30)
        volume_base = self.feat.sma(volume, timeperiod=20)
        atr = self.feat.atr(high, low, close, timeperiod=14)

        # Short-term return and rolling return help separate weak drift from real momentum.
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_avg = self.feat.rolling_mean(return_1, window=3)

        # Weak long starts when trend is up and momentum is improving.
        weak_long = (
            (close > ema_slow)
            & (ema_fast > ema_slow)
            & (return_avg > 0)
        )

        # Strong long requires volume expansion and a clearer daily push.
        strong_long = (
            weak_long
            & (volume > volume_base)
            & (return_1 > 0)
            & (atr > 0)
        )

        # Exit when trend breaks or momentum turns down.
        exit_setup = (ema_fast < ema_slow) | (return_avg < 0)

        # Apply exits first, then half size, then full size.
        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)