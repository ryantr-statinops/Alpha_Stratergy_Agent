class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        open_ = self.data.pv_open
        evening_star = self.feat.evening_star(open_, high, low, close)
        trima = self.feat.trima(close, timeperiod=30)

        long_setup = (close > trima)
        short_setup = (evening_star < 0) & (close < trima)
        exit_setup = self.op.crossed(close, trima)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
