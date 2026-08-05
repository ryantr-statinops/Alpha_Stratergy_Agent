class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 8

    def __algorithm__(self):
        close = self.data.pv_close
        rocr = self.feat.rocr(close, timeperiod=5)
        ema10 = self.feat.ema(close, timeperiod=10)

        long_setup = (rocr > 1) & (close > ema10)
        short_setup = (rocr < 1) & (close < ema10)
        exit_setup = self.op.crossed(close, ema10)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
