class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        fastk, fastd = self.feat.stochrsi(close, timeperiod=14, fastk_period=5, fastd_period=3)
        adxr = self.feat.adxr(high, low, close, timeperiod=14)

        long_setup = (fastk > 50) & (adxr > 22)
        short_setup = (fastk < 50) & (adxr > 22)
        exit_setup = self.op.crossed_above_value(fastk, 50) | self.op.crossed_below_value(fastk, 50) | (adxr < 18)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
