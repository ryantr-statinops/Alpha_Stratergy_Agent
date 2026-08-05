class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        percentile_rank = self.feat.rolling_percentile_rank(close, window=10)

        long_setup = percentile_rank < 0.2
        short_setup = percentile_rank > 0.8
        exit_setup = (percentile_rank > 0.4) & (percentile_rank < 0.6)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
