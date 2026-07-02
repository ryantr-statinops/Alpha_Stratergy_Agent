
"""
name:    TrendMACDAggr_5min
summary: MACD: MACD + ADX(30) — 5min
thesis:  trend | 5min
idea:    MACD + ADX trend strength
"""
class CustomStrategy(SimpleAlgorithm):

    adx_window = 5

    return_window = 2
    return_threshold = 0.0001
    position_close_after_n_candles = 72

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        macd_line, signal_line, _hist = self.feat.macd(
            close, fastperiod=12, slowperiod=26, signalperiod=9
        )
        adx = self.feat.adx(high, low, close, timeperiod=self.adx_window)

        trend_long = macd_line > signal_line
        trend_short = macd_line < signal_line

        strong_long = trend_long & (adx > 25) & (return_roll > 0)
        weak_long = trend_long & (adx > 18) & (return_roll > 0)
        strong_short = trend_short & (adx > 25) & (return_roll < 0)
        weak_short = trend_short & (adx > 18) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(macd_line, signal_line) | self.op.crossed_above(macd_line, signal_line)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-1)
