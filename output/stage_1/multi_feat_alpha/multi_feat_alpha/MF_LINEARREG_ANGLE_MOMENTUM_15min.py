class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        linearreg_angle = self.feat.linearreg_angle(close, timeperiod=10)
        momentum = self.feat.momentum(close, timeperiod=5)
        sma10 = self.feat.sma(close, timeperiod=10)

        long_setup = (linearreg_angle > 0) & (momentum > 0) & (close > sma10)
        short_setup = (linearreg_angle < 0) & (momentum < 0) & (close < sma10)
        exit_setup = self.op.crossed(close, sma10) | self.op.crossed_above_value(linearreg_angle, 0) | self.op.crossed_below_value(linearreg_angle, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
