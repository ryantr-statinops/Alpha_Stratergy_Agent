"""
name:    VnMidMacdTrend
summary: Long mid caps on MACD 8/21/5 expansion above the 30-day average.
idea:    MACD momentum captures the strong directional waves of mid caps while
         the slow average keeps the trade on the right side of the trend.
         Exit when the MACD line crosses back below its signal line or price
         breaks the slow average.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close

        macd_line, signal_line, _hist = self.feat.macd(
            close,
            fastperiod=8,
            slowperiod=21,
            signalperiod=5,
        )
        ema_slow = self.feat.ema(close, timeperiod=30)

        known = (
            self.op.notna(macd_line)
            & self.op.notna(signal_line)
            & self.op.notna(ema_slow)
            & (close > 0)
        )

        weak_long = known & (macd_line > signal_line) & (close > ema_slow)
        exit_setup = known & ((macd_line < signal_line) | (close < ema_slow))

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=1)