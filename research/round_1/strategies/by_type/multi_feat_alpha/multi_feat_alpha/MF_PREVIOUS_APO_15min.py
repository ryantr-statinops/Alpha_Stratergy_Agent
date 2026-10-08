class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        apo = self.feat.apo(close, fastperiod=5, slowperiod=13, matype=0)
        prev_apo = self.op.previous(apo)
        sma10 = self.feat.sma(close, timeperiod=10)

        long_setup = (apo > prev_apo) & (apo > 0) & (close > sma10)
        short_setup = (apo < prev_apo) & (apo < 0) & (close < sma10)
        exit_setup = self.op.crossed_above_value(apo, 0) | self.op.crossed_below_value(apo, 0) | self.op.crossed(close, sma10)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
