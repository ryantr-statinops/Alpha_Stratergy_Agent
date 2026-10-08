class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        rolling_mad = self.feat.rolling_mad(close, timeperiod=10)
        mad_mean = self.feat.rolling_mean(rolling_mad, window=30)

        long_setup = rolling_mad > mad_mean
        short_setup = rolling_mad < mad_mean
        exit_setup = self.op.crossed(rolling_mad, mad_mean)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
