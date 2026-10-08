class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        t3 = self.feat.t3(close, timeperiod=10, vfactor=0)

        long_setup = close > t3
        short_setup = close < t3
        exit_setup = self.op.crossed(close, t3)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
