class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        vn30_close = self.data.pv_vn30_close
        beta = self.feat.beta(close, vn30_close, timeperiod=20)
        cci = self.feat.cci(high, low, close, timeperiod=14)

        long_setup = (beta > 0.5) & (cci > 0)
        short_setup = (beta > 0.5) & (cci < 0)
        exit_setup = self.op.crossed(cci, 0) | (beta < 0.3)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
