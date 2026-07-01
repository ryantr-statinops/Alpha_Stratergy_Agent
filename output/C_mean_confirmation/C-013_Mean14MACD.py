"""
name:    Mean14MACD
summary: Long when close > mean(14) and MACD bullish
idea:    MACD trend confirmation with mean filter
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        mean = self.feat.rolling_mean(close, window=14)
        macd, macd_signal, _hist = self.feat.macd(close, fastperiod=12, slowperiod=26, signalperiod=9)
        

        long_setup = (close > mean) & (macd > macd_signal)
        short_setup = (close < mean) & (macd < macd_signal)
        exit_long = self.op.crossed_below(close, mean) | macd < macd_signal
        exit_short = self.op.crossed_above(close, mean) | macd > macd_signal
        exit_setup = exit_long | exit_short

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
