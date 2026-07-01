"""
name:    Mean14Q10RSI
summary: Short when close < Q20(10) < mean(14) and RSI < 50
idea:    Three-layer confirmation: quantile breakdown + mean trend + RSI momentum
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        mean = self.feat.rolling_mean(close, window=14)
        upper = self.feat.rolling_quantile(close, 10, 0.8)
        lower = self.feat.rolling_quantile(close, 10, 0.2)
        rsi = self.feat.rsi(close, timeperiod=14)
        

        long_setup = (close > upper) & (close > mean) & (rsi > 50)
        short_setup = (close < lower) & (close < mean) & (rsi < 50)
        exit_long = self.op.crossed_below(close, mean) | rsi < 40
        exit_short = self.op.crossed_above(close, mean) | rsi > 60
        exit_setup = exit_long | exit_short

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
