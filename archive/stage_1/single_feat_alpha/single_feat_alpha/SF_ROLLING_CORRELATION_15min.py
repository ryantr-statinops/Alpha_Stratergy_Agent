class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        rolling_corr = self.feat.rolling_correlation(close, volume, timeperiod=10)

        long_setup = rolling_corr > 0.5
        short_setup = rolling_corr < -0.5
        exit_setup = (rolling_corr > -0.3) & (rolling_corr < 0.3)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
