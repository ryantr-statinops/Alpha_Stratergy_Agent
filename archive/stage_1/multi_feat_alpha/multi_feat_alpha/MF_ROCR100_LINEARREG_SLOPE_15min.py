class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        rocr100 = self.feat.rocr100(close, timeperiod=10)
        linearreg_slope = self.feat.linearreg_slope(close, timeperiod=14)

        long_setup = (rocr100 > 100) & (linearreg_slope > 0)
        short_setup = (rocr100 < 100) & (linearreg_slope < 0)
        exit_setup = self.op.crossed_above_value(rocr100, 100) | self.op.crossed_below_value(rocr100, 100) | self.op.crossed_above_value(linearreg_slope, 0) | self.op.crossed_below_value(linearreg_slope, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
