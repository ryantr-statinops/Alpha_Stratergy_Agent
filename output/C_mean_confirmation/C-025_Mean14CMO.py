"""
name:    Mean14CMO
summary: Long when close > mean(14) and CMO positive, short when opposite
idea:    Chande Momentum Oscillator as confirmation filter with mean trend
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close

        mean = self.feat.rolling_mean(close, window=14)
        cmo = self.feat.cmo(close, timeperiod=14)

        long_setup = (close > mean) & (cmo > 0)
        short_setup = (close < mean) & (cmo < 0)
        exit_long = self.op.crossed_below(close, mean) | (cmo < -10)
        exit_short = self.op.crossed_above(close, mean) | (cmo > 10)
        exit_setup = exit_long | exit_short

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
