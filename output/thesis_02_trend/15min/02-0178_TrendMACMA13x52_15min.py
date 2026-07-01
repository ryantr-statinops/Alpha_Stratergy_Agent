
"""
name:    TrendMACMA13x52_15min
summary: MA Cross: MA(13)/MA(52) cross — 15min
thesis:  trend | 15min
idea:    Moving average crossover
"""
class CustomStrategy(SimpleAlgorithm):

    fast_window = 13
    slow_window = 52

    def __algorithm__(self):
        close = self.data.pv_close

        fast_ma = self.feat.sma(close, timeperiod=self.fast_window)
        slow_ma = self.feat.sma(close, timeperiod=self.slow_window)

        long_setup = self.op.crossed_above(fast_ma, slow_ma)
        short_setup = self.op.crossed_below(fast_ma, slow_ma)
        exit_setup = self.op.crossed_below(fast_ma, slow_ma) | self.op.crossed_above(fast_ma, slow_ma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
