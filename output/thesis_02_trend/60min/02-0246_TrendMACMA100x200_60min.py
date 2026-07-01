
"""
name:    TrendMACMA100x200_60min
summary: MA Cross: MA(100)/MA(200) cross — 60min
thesis:  trend | 60min
idea:    Moving average crossover
"""
class CustomStrategy(SimpleAlgorithm):

    fast_window = 100
    slow_window = 200

    return_window = 14
    return_threshold = 0.0005
    position_close_after_n_candles = 6

    def __algorithm__(self):
        close = self.data.pv_close
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        fast_ma = self.feat.sma(close, timeperiod=self.fast_window)
        slow_ma = self.feat.sma(close, timeperiod=self.slow_window)

        long_setup = (self.op.crossed_above(fast_ma, slow_ma)) & (return_roll > 0)
        short_setup = (self.op.crossed_below(fast_ma, slow_ma)) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(fast_ma, slow_ma) | self.op.crossed_above(fast_ma, slow_ma)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
