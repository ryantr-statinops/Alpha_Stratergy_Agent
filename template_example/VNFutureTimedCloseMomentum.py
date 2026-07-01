"""
name:    VNFutureTimedCloseMomentum
summary: Force futures positions flat at selected late-session close times
         and after a fixed candle age.
idea:    The strategy can enter from normal trend conditions, but
         close-time gates and an 11-candle holding limit keep exposure
         from running into the end window.
"""


class CustomStrategy(SimpleAlgorithm):
    # Force positions flat at these exact late-session timestamps.
    position_close_times = [
        "07:20", "07:25", "07:30", "07:35", "07:40", "07:45", "07:50"
    ]

    # Force close after 11 candles so the strategy does not hold beyond the
    # intended intraday window.
    position_close_after_n_candles = 11

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

        # Use the latest return as a small directional confirmation filter.
        # Positive return supports long setups, negative return supports short setups.
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)

        # Strong setups require trend alignment, enough ADX strength, and volume confirmation.
        strong_long = (macd > macd_signal) & (adx > 22) & (return_1 > 0) & (volume > volume_base)
        strong_short = (macd < macd_signal) & (adx > 22) & (return_1 < 0) & (volume > volume_base)

        # Weak setups only require trend alignment and a supportive one-bar return.
        # These get smaller size because the move is less confirmed.
        weak_long = (macd > macd_signal) & (adx > 18) & (return_1 > 0)
        weak_short = (macd < macd_signal) & (adx > 18) & (return_1 < 0)

        # Exit when trend strength fades or the latest candle is too close to flat.
        # That keeps the strategy from staying engaged when momentum is not clear.
        exit_setup = (adx < 14) | ((return_1 > -0.0005) & (return_1 < 0.0005))

        # Apply exits first so entry rules can override them when their conditions hold.
        # Then layer weak positions before strong ones so the stronger signal can replace them.
        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-0.75)