class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        open_ = self.data.pv_open
        piercing = self.feat.piercing_pattern(open_, high, low, close)
        midpoint = self.feat.midpoint(close, timeperiod=14)

        long_setup = (piercing > 0) & (close > midpoint)
        short_setup = (close < midpoint)
        exit_setup = self.op.crossed(close, midpoint)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
