class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        rolling_median = self.feat.rolling_median(close, window=20)
        linearreg = self.feat.linearreg(close, timeperiod=14)

        long_setup = (close > rolling_median) & (linearreg > close)
        short_setup = (close < rolling_median) & (linearreg < close)
        exit_setup = self.op.crossed(close, rolling_median) | self.op.crossed(linearreg, close)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
