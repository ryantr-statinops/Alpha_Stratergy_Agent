class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        plus_di = self.feat.plus_di(high, low, close, timeperiod=14)
        minus_di = self.feat.minus_di(high, low, close, timeperiod=14)
        adx = self.feat.adx(high, low, close, timeperiod=14)

        long_setup = (plus_di > minus_di) & (adx > 20)
        short_setup = (minus_di > plus_di) & (adx > 20)
        exit_setup = self.op.crossed(plus_di, minus_di) | self.op.crossed_below_value(adx, 20)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
