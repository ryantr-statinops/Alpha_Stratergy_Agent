class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        kama = self.feat.kama(close, timeperiod=10)
        roc = self.feat.roc(close, timeperiod=10)

        long_setup = (close > kama) & (roc > 0)
        short_setup = (close < kama) & (roc < 0)
        exit_setup = self.op.crossed(close, kama) | self.op.crossed_above_value(roc, 0) | self.op.crossed_below_value(roc, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
