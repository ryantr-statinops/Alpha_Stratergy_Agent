class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        donchian_upper = self.feat.donchian_upper(high, timeperiod=10)
        donchian_lower = self.feat.donchian_lower(low, timeperiod=10)
        donchian_mid = (donchian_upper + donchian_lower) / 2
        adx = self.feat.adx(high, low, close, timeperiod=10)

        long_setup = (close > donchian_mid) & (adx > 22)
        short_setup = (close < donchian_mid) & (adx > 22)
        exit_setup = self.op.crossed(close, donchian_mid) | (adx < 18)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
