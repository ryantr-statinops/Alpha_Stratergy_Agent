
"""
name:    TrendQStd_30min
summary: Quantile Trend: Q75%/Q25% + ADX — 30min
thesis:  trend | 30min
idea:    Quantile trend channel
"""
class CustomStrategy(SimpleAlgorithm):

    q_window = 20
    adx_window = 9
    q_high = 0.75
    q_low = 0.25

    return_window = 5
    return_threshold = 0.0006
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        upper = self.feat.rolling_quantile(close, self.q_window, self.q_high)
        lower = self.feat.rolling_quantile(close, self.q_window, self.q_low)
        adx = self.feat.adx(high, low, close, timeperiod=self.adx_window)

        breakout_high = close > upper
        breakout_low = close < lower

        strong_long = breakout_high & (adx > 25) & (return_roll > 0)
        weak_long = breakout_high & (adx > 18) & (return_roll > 0)
        strong_short = breakout_low & (adx > 25) & (return_roll < 0)
        weak_short = breakout_low & (adx > 18) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(close, upper) | self.op.crossed_above(close, lower)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-1)
