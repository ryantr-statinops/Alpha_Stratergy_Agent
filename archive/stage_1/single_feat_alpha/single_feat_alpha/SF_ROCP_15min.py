class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        rocp = self.feat.rocp(close, timeperiod=5)

        long_setup = rocp > 0
        short_setup = rocp < 0
        exit_setup = self.op.crossed_above_value(rocp, 0) | self.op.crossed_below_value(rocp, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
