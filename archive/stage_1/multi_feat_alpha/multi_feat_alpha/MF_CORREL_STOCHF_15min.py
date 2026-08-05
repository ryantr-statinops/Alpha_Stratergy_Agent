class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        correl = self.feat.correl(close, volume, timeperiod=20)
        fastk, fastd = self.feat.stochf(high, low, close, fastk_period=5, fastd_period=3)

        long_setup = (correl > 0) & (fastk > 50)
        short_setup = (correl < 0) & (fastk < 50)
        exit_setup = self.op.crossed_below_value(correl, 0) | self.op.crossed_above_value(fastk, 50) | self.op.crossed_below_value(fastk, 50)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
