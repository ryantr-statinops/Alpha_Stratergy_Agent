class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        high = self.data.pv_high
        low = self.data.pv_low
        close = self.data.pv_close
        adx_val = self.feat.adx(high, low, close, timeperiod=10)
        plus_di = self.feat.plus_di(high, low, close, timeperiod=10)
        minus_di = self.feat.minus_di(high, low, close, timeperiod=10)

        long_setup = (plus_di > minus_di) & (adx_val > 20)
        short_setup = (minus_di > plus_di) & (adx_val > 20)
        exit_setup = self.op.crossed(plus_di, minus_di)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
