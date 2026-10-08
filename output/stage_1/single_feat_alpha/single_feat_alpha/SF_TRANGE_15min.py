class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        high = self.data.pv_high
        low = self.data.pv_low
        close = self.data.pv_close
        trange = self.feat.trange(high, low, close)
        trange_mean = self.feat.rolling_mean(trange, window=20)

        long_setup = trange > trange_mean
        short_setup = trange > trange_mean
        exit_setup = trange < trange_mean

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
