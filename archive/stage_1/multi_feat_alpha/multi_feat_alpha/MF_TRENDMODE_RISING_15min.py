class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        trendmode = self.feat.trendmode(close)

        long_setup = (trendmode > 0) & self.op.rising(close, 3)
        short_setup = (trendmode > 0) & self.op.falling(close, 3)
        exit_setup = self.op.crossed_below_value(trendmode, 1)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
