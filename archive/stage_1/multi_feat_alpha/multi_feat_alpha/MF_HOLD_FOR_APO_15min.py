class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        apo = self.feat.apo(close, fastperiod=5, slowperiod=13, matype=0)
        sma10 = self.feat.sma(close, timeperiod=10)
        hold_long = self.op.hold_for(apo > 0, 5)
        hold_short = self.op.hold_for(apo < 0, 5)

        long_setup = hold_long & (close > sma10)
        short_setup = hold_short & (close < sma10)
        exit_setup = self.op.crossed(close, sma10)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
