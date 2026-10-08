class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        open_ = self.data.pv_open
        sarext = self.feat.sarext(high, low, close, startvalue=0, offsetonreverse=0)
        bop = self.feat.bop(open_, high, low, close)

        long_setup = (sarext < close) & (bop > 0)
        short_setup = (sarext > close) & (bop < 0)
        exit_setup = self.op.crossed(sarext, close) | self.op.crossed_above_value(bop, 0) | self.op.crossed_below_value(bop, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
