
"""
name:    TrendQMild_5min
summary: Quantile Trend: Q70%/Q30% + ADX — 5min
thesis:  trend | 5min
idea:    Quantile trend channel
"""
class CustomStrategy(SimpleAlgorithm):

    q_window = 14
    adx_window = 7

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        upper = self.feat.rolling_quantile(close, self.q_window, 0.75)
        lower = self.feat.rolling_quantile(close, self.q_window, 0.25)
        adx = self.feat.adx(high, low, close, timeperiod=self.adx_window)

        long_setup = (close > upper) & (adx > 20)
        short_setup = (close < lower) & (adx > 20)
        exit_setup = self.op.crossed_below(close, upper) | self.op.crossed_above(close, lower)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
