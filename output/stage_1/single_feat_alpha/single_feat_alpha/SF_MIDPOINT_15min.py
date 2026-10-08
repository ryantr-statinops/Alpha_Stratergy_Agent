class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        midpoint = self.feat.midpoint(close, timeperiod=10)

        long_setup = close > midpoint
        short_setup = close < midpoint
        exit_setup = self.op.crossed(close, midpoint)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
