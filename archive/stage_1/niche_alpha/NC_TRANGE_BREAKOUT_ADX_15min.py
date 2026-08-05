class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        trange = self.feat.trange(high, low, close)
        trange_sma = self.feat.sma(trange, timeperiod=10)
        adx = self.feat.adx(high, low, close, timeperiod=10)
        rsi = self.feat.rsi(close, timeperiod=14)

        long_setup = (trange > trange_sma) & (rsi < 40) & (adx > 18)
        short_setup = (trange > trange_sma) & (rsi > 60) & (adx > 18)
        exit_setup = (adx < 15)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
