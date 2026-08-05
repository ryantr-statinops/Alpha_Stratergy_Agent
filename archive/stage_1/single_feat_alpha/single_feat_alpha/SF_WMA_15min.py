class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        wma = self.feat.wma(close, timeperiod=10)

        long_setup = close > wma
        short_setup = close < wma
        exit_setup = self.op.crossed(close, wma)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
