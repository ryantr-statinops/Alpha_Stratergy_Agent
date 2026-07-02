"""
name:    T01-D_q0.85_0.15
summary: Quantile Breakout Channel
idea:    Trade breakouts beyond rolling quantile bands at multiple quantile thresholds; exit when price reverts to the band edge.
"""
class CustomStrategy(SimpleAlgorithm):
    q_window = 100
    thesis_group = "01"

    def __algorithm__(self):
        close = self.data.pv_close

        upper = self.feat.rolling_quantile(close, window=self.q_window, q=0.85)
        lower = self.feat.rolling_quantile(close, window=self.q_window, q=0.15)

        long_setup = close > upper
        short_setup = close < lower
        exit_setup = self.op.crossed_below(close, upper) | self.op.crossed_above(close, lower)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

