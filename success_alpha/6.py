"""
name:    SMA-single
summary: long short exit
idea:    solo SMA 9 
"""

class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close
        ema = self.feat.ema(close, timeperiod=9)

        long_signal = close > ema
        short_signal = close < ema
        exit_setup = self.op.crossed(close,ema)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=0.5)
        self.set_positions(short_signal, position=-0.5)

