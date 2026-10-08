class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        percentile_rank = self.feat.rolling_percentile_rank(close, window=20)
        adx = self.feat.adx(high, low, close, timeperiod=10)
        return_1 = self.op.pct_change(close, periods=1)
        return_roll = self.feat.rolling_mean(return_1, window=10)

        long_setup = (percentile_rank > 0.6) & (adx > 22) & (return_roll > 0)
        short_setup = (percentile_rank < 0.4) & (adx > 22) & (return_roll < 0)
        exit_setup = (adx < 18)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
