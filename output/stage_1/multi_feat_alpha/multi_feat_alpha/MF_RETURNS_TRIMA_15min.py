class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        returns = self.feat.returns(close, timeperiod=5)
        trima = self.feat.trima(close, timeperiod=30)

        long_setup = (returns > 0) & (close > trima)
        short_setup = (returns < 0) & (close < trima)
        exit_setup = self.op.crossed(close, trima)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
