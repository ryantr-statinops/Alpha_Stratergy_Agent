class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        var = self.feat.var(close, timeperiod=10, nbdev=1)
        var_sma = self.feat.sma(var, timeperiod=10)
        willr = self.feat.willr(high, low, close, timeperiod=10)

        long_setup = (var < var_sma) & (willr > -50)
        short_setup = (var < var_sma) & (willr < -50)
        exit_setup = self.op.crossed_above_value(var, var_sma) | self.op.crossed_above_value(willr, -50) | self.op.crossed_below_value(willr, -50)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
