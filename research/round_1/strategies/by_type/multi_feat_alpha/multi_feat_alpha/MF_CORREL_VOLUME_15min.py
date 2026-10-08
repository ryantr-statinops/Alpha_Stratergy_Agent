class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        correl = self.feat.correl(close, volume, timeperiod=10)
        sma10 = self.feat.sma(close, timeperiod=10)

        long_setup = (correl > 0) & (close > sma10)
        short_setup = (correl < 0) & (close < sma10)
        exit_setup = self.op.crossed(close, sma10) | self.op.crossed_above_value(correl, 0) | self.op.crossed_below_value(correl, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
