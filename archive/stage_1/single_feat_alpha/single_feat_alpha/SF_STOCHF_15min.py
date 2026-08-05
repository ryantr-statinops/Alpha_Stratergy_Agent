class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        high = self.data.pv_high
        low = self.data.pv_low
        close = self.data.pv_close
        fastk, fastd = self.feat.stochf(high, low, close, fastk_period=10, fastd_period=3, fastd_matype=0)

        long_setup = fastk > 50
        short_setup = fastk < 50
        exit_setup = self.op.crossed_above_value(fastk, 50) | self.op.crossed_below_value(fastk, 50)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
