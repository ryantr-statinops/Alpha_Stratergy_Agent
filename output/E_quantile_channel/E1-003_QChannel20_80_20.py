"""
name:    QChannel20_80_20
summary: Quantile breakout: long above Q80, short below Q20 (window=20)
idea:    Medium-term quantile breakout
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close

        upper = self.feat.rolling_quantile(close, 20, 0.8)
        lower = self.feat.rolling_quantile(close, 20, 0.2)

        long_setup = close > upper
        short_setup = close < lower
        exit_setup = self.op.crossed_below(close, upper) | self.op.crossed_above(close, lower)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
