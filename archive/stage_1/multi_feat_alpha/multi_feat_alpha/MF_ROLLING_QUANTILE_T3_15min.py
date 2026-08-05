class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        rolling_quantile = self.feat.rolling_quantile(close, window=20, q=0.9)
        t3 = self.feat.t3(close, timeperiod=5, vfactor=0)

        long_setup = (close > rolling_quantile) & (close > t3)
        short_setup = (close < rolling_quantile) & (close < t3)
        exit_setup = self.op.crossed(close, rolling_quantile) | self.op.crossed(close, t3)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
