class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        aroondown, aroonup = self.feat.aroon(high, low, timeperiod=14)
        ultosc = self.feat.ultosc(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)

        long_setup = (aroonup > aroondown) & (ultosc > 50)
        short_setup = (aroonup < aroondown) & (ultosc < 50)
        exit_setup = self.op.crossed(aroonup, aroondown) | self.op.crossed_above_value(ultosc, 50) | self.op.crossed_below_value(ultosc, 50)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
