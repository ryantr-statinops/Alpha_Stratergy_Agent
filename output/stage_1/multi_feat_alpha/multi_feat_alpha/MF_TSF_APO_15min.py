class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        tsf = self.feat.tsf(close, timeperiod=14)
        apo = self.feat.apo(close, fastperiod=12, slowperiod=26, matype=0)

        long_setup = (tsf > close) & (apo > 0)
        short_setup = (tsf < close) & (apo < 0)
        exit_setup = self.op.crossed(tsf, close) | self.op.crossed_above_value(apo, 0) | self.op.crossed_below_value(apo, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
