"""
name:    QuantileChannel100_75
summary: Short when close < quantile(100, 0.25)
idea:    Long-term quantile channel with wider bands
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close

        upper = self.feat.rolling_quantile(close, 100, 0.75)
        lower = self.feat.rolling_quantile(close, 100, 0.25)

        long_setup = close > upper
        short_setup = close < lower
        exit_setup = self.op.crossed_below(close, upper) | self.op.crossed_above(close, lower)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
