
"""
name:    TrendMACMA6x13_15min
summary: MA Cross: MA(6)/MA(13) cross — 15min
thesis:  trend | 15min
idea:    Moving average crossover
"""
class CustomStrategy(SimpleAlgorithm):

    fast_window = 6
    slow_window = 13

    return_window = 5
    return_threshold = 0.0002
    position_close_after_n_candles = 24
    adx_window = 10

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=10)

        fast_ma = self.feat.sma(close, timeperiod=self.fast_window)
        slow_ma = self.feat.sma(close, timeperiod=self.slow_window)

        long_setup = ((self.op.crossed_above(fast_ma, slow_ma)) & (return_roll > 0)) & (adx > 22)
        short_setup = ((self.op.crossed_below(fast_ma, slow_ma)) & (return_roll < 0)) & (adx > 22)
        exit_setup = ((self.op.crossed_below(fast_ma, slow_ma) | self.op.crossed_above(fast_ma, slow_ma)) | (abs(return_roll) < self.return_threshold)) | (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
