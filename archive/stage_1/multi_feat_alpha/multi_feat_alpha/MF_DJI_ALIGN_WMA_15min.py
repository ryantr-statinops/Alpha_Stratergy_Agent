class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        dji_close = self.data.pv_dji_close
        wma10 = self.feat.wma(close, timeperiod=10)

        long_setup = (close > dji_close) & (close > wma10)
        short_setup = (close < dji_close) & (close < wma10)
        exit_setup = self.op.crossed(close, wma10) | self.op.crossed(close, dji_close)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
