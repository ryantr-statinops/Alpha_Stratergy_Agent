class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        rolling_argmax = self.feat.rolling_argmax(close, window=20)
        kama = self.feat.kama(close, timeperiod=10)

        long_setup = (rolling_argmax == 0) & (close > kama)
        short_setup = (rolling_argmax == 0) & (close < kama)
        exit_setup = self.op.crossed_above_value(rolling_argmax, 1) | self.op.crossed(close, kama)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
