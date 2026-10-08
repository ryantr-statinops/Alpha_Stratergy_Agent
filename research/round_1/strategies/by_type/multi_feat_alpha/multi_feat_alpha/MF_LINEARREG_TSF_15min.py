class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        linearreg = self.feat.linearreg(close, timeperiod=20)
        tsf = self.feat.tsf(close, timeperiod=20)

        long_setup = (close > linearreg) & (tsf > close)
        short_setup = (close < linearreg) & (tsf < close)
        exit_setup = self.op.crossed(close, linearreg) | self.op.crossed(tsf, close)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
