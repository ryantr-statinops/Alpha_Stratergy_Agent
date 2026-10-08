class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        rocp = self.feat.rocp(close, timeperiod=10)
        diff_rocp = self.op.diff(rocp, 2)
        sma10 = self.feat.sma(close, timeperiod=10)

        long_setup = (diff_rocp > 0) & (rocp > 0) & (close > sma10)
        short_setup = (diff_rocp < 0) & (rocp < 0) & (close < sma10)
        exit_setup = self.op.crossed_above_value(rocp, 0) | self.op.crossed_below_value(rocp, 0) | self.op.crossed(close, sma10)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
