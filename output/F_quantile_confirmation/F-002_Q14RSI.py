"""
name:    Q14RSI
summary: Short when close < Q20(14) and RSI < 50
idea:    Quantile breakdown with RSI momentum confirmation
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        upper = self.feat.rolling_quantile(close, 14, 0.8)
        lower = self.feat.rolling_quantile(close, 14, 0.2)
        rsi = self.feat.rsi(close, timeperiod=14)
        

        long_setup = (close > upper) & (rsi > 50)
        short_setup = (close < lower) & (rsi < 50)
        exit_long = self.op.crossed_below(close, upper) | rsi < 40
        exit_short = self.op.crossed_above(close, lower) | rsi > 60
        exit_setup = exit_long | exit_short

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
