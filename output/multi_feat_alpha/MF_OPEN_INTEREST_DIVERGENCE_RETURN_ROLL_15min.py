class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        fut_oi = self.data.fut_open_interest_vn30f1m_1d
        return_1 = self.op.pct_change(close, periods=1)
        return_roll = self.feat.rolling_mean(return_1, window=5)
        oi_change = self.op.pct_change(fut_oi, periods=1)

        long_setup = (return_roll < 0) & (oi_change > 0)
        short_setup = (return_roll > 0) & (oi_change < 0)
        exit_setup = (return_roll > 0) | (return_roll < 0) | (oi_change < 0.01)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
