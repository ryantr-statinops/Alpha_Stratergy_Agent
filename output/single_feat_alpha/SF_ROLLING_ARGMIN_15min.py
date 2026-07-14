class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 5

    def __algorithm__(self):
        low = self.data.pv_low
        rolling_argmin = self.feat.rolling_argmin(low, timeperiod=20)

        long_setup = rolling_argmin == 0
        short_setup = rolling_argmin >= 10
        exit_setup = long_setup & short_setup

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
