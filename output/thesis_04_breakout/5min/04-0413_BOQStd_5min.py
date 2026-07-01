
"""
name:    BOQStd_5min
summary: Quantile BO: Q80%(8) + volume — 5min
thesis:  breakout | 5min
idea:    Quantile breakout with volume
"""
class CustomStrategy(SimpleAlgorithm):

    q_window = 8
    vol_window = 14
    q_high = 0.8
    q_low = 0.2

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        upper = self.feat.rolling_quantile(close, self.q_window, self.q_high)
        lower = self.feat.rolling_quantile(close, self.q_window, self.q_low)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        long_setup = (close > upper) & (volume > vol_sma)
        short_setup = (close < lower) & (volume > vol_sma)
        exit_setup = self.op.crossed_below(close, upper) | self.op.crossed_above(close, lower)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
