
"""
name:    TrendMACMA60x100_60min
summary: MA Cross: MA(60)/MA(100) cross — 60min
thesis:  trend | 60min
idea:    Moving average crossover
"""
class CustomStrategy(SimpleAlgorithm):

    fast_window = 60
    slow_window = 100

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
