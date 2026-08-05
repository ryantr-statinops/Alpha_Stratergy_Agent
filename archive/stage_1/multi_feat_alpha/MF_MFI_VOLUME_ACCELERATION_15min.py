class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        mfi = self.feat.mfi(high, low, close, volume, timeperiod=14)
        vol_roc = self.feat.roc(volume, timeperiod=5)

        long_setup = (mfi > 50) & (vol_roc > 0)
        short_setup = (mfi < 50) & (vol_roc > 0)
        exit_setup = self.op.crossed_above_value(mfi, 50) | self.op.crossed_below_value(mfi, 50) | (vol_roc < 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
