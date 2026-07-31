class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        upper_band, middle_band, lower_band = self.feat.bbands(close, timeperiod=10, nbdevup=2, nbdevdn=2)

        long_setup = close > middle_band
        short_setup = close < middle_band
        exit_setup = self.op.crossed(close, middle_band)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
