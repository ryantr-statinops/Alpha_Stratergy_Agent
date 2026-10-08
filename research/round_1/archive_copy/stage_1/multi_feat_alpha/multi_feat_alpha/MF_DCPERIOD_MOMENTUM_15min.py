class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        dcperiod = self.feat.dcperiod(close)
        momentum = self.feat.momentum(close, timeperiod=5)
        sma10 = self.feat.sma(close, timeperiod=10)

        long_setup = (dcperiod < 10) & (momentum > 0) & (close > sma10)
        short_setup = (dcperiod < 10) & (momentum < 0) & (close < sma10)
        exit_setup = self.op.crossed(close, sma10)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
