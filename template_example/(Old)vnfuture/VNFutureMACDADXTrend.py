"""
name:    VNFutureMACDADXTrend
summary: Trade futures direction from MACD trend confirmation with ADX and
         short-term return direction.
idea:    MACD defines the core trend signal, while ADX and the latest
         return help filter weak or indecisive crosses. This keeps the
         strategy in directional moves and steps aside when trend strength
         fades.
"""


class CustomStrategy(SimpleAlgorithm):
    # Force close after 24 candles so the strategy does not hold beyond the
    # intended intraday window.
    position_close_after_n_candles = 24

    def __algorithm__(self):
        # Assign each field to a short local name so later signal rules are readable.
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        # MACD captures trend direction, ADX measures trend strength, and the
        # latest return confirms whether price is moving with the signal.
        macd, macd_signal, _hist = self.feat.macd(
            close,
            fastperiod=12,
            slowperiod=26,
            signalperiod=9,
        )
        adx = self.feat.adx(high, low, close, timeperiod=14)
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)

        # Long when MACD is above its signal line, trend strength is strong enough,
        # and the latest return is positive.
        long_setup = (macd > macd_signal) & (adx > 18) & (return_1 > 0)

        # Short uses the same structure in the opposite direction.
        short_setup = (macd < macd_signal) & (adx > 18) & (return_1 < 0)

        # Exit when ADX drops below the trend-strength threshold.
        exit_setup = adx < 14

        # Apply exits first so entry rules can override when their conditions are met.
        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-0.5)