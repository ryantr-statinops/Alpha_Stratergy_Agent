"""
name:    SMA-single
summary: long short exit
idea:    solo SMA 9 
"""

class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):

        close = self.data.pv_close
        sma = self.feat.sma(close, timeperiod=9)

        long_setup = close > sma
        short_setup = close < sma

        exit_setup = self.op.crossed(close,sma)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)

