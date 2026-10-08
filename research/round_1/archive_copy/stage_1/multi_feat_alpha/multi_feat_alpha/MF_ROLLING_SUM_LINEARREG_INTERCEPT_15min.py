class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        rolling_sum = self.feat.rolling_sum(close, window=5)
        linearreg_intercept = self.feat.linearreg_intercept(close, timeperiod=20)

        long_setup = (rolling_sum > 0) & (close > linearreg_intercept)
        short_setup = (rolling_sum < 0) & (close < linearreg_intercept)
        exit_setup = self.op.crossed_above_value(rolling_sum, 0) | self.op.crossed_below_value(rolling_sum, 0) | self.op.crossed(close, linearreg_intercept)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
