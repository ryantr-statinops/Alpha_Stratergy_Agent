"""
name:    Q20Volume
summary: Long when close > Q80(20) and volume above average
idea:    Quantile breakout with volume confirmation
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        upper = self.feat.rolling_quantile(close, 20, 0.8)
        lower = self.feat.rolling_quantile(close, 20, 0.2)
        volume_sma = self.feat.sma(volume, timeperiod=20)
        

        long_setup = (close > upper) & (volume > volume_sma)
        short_setup = (close < lower) & (volume > volume_sma)
        exit_long = self.op.crossed_below(close, upper) | volume < volume_sma
        exit_short = self.op.crossed_above(close, lower) | volume < volume_sma
        exit_setup = exit_long | exit_short

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
