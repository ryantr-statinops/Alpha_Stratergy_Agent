class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        fut_matched_value = self.data.fut_matched_value_vn30f1m_1d
        value_accel = self.feat.roc(fut_matched_value, timeperiod=5)
        adx = self.feat.adx(high, low, close, timeperiod=14)

        long_setup = (value_accel > 0) & (adx > 22)
        short_setup = (value_accel < 0) & (adx > 22)
        exit_setup = (value_accel < 0) | (adx < 18)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
