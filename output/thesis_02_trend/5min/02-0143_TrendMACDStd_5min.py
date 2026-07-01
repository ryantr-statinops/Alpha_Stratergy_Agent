
"""
name:    TrendMACDStd_5min
summary: MACD: MACD + ADX(20) — 5min
thesis:  trend | 5min
idea:    MACD + ADX trend strength
"""
class CustomStrategy(SimpleAlgorithm):

    adx_window = 7
    adx_threshold = 20

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        macd_line, signal_line, _hist = self.feat.macd(
            close, fastperiod=12, slowperiod=26, signalperiod=9
        )
        adx = self.feat.adx(high, low, close, timeperiod=self.adx_window)

        long_setup = (macd_line > signal_line) & (adx > self.adx_threshold)
        short_setup = (macd_line < signal_line) & (adx > self.adx_threshold)
        exit_setup = self.op.crossed_below(macd_line, signal_line) | self.op.crossed_above(macd_line, signal_line)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
