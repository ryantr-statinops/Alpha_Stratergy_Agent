class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        linearreg_intercept = self.feat.linearreg_intercept(close, timeperiod=10)
        momentum = self.feat.momentum(close, timeperiod=5)

        long_setup = (close > linearreg_intercept) & (momentum > 0)
        short_setup = (close < linearreg_intercept) & (momentum < 0)
        exit_setup = self.op.crossed(close, linearreg_intercept)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
