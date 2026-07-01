"""
name:    Mean50ROC
summary: Long when close > mean(50) and ROC positive
idea:    Momentum filter with ROC on long-term mean
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        mean = self.feat.rolling_mean(close, window=50)
        roc = self.feat.roc(close, timeperiod=10)
        

        long_setup = (close > mean) & (roc > 0)
        short_setup = (close < mean) & (roc < 0)
        exit_long = self.op.crossed_below(close, mean) | roc < -2
        exit_short = self.op.crossed_above(close, mean) | roc > 2
        exit_setup = exit_long | exit_short

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
