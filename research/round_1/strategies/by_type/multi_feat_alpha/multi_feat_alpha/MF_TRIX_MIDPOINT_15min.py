class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        trix = self.feat.trix(close, timeperiod=14)
        midpoint = self.feat.midpoint(close, timeperiod=14)

        long_setup = (trix > 0) & (close > midpoint)
        short_setup = (trix < 0) & (close < midpoint)
        exit_setup = self.op.crossed(close, midpoint) | self.op.crossed_above_value(trix, 0) | self.op.crossed_below_value(trix, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
