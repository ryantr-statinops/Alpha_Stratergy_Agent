class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        tema = self.feat.tema(close, timeperiod=10)
        mfi = self.feat.mfi(high, low, close, volume, timeperiod=10)

        long_setup = (close > tema) & (mfi > 50)
        short_setup = (close < tema) & (mfi < 50)
        exit_setup = self.op.crossed(close, tema)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
