class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        rocr = self.feat.rocr(close, timeperiod=5)

        long_setup = rocr > 1
        short_setup = rocr < 1
        exit_setup = self.op.crossed_above_value(rocr, 1) | self.op.crossed_below_value(rocr, 1)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
