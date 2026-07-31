class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        volume_z_val = self.feat.volume_z(volume, timeperiod=10)
        sma = self.feat.sma(close, timeperiod=10)

        long_setup = (close > sma) & (volume_z_val > 1)
        short_setup = (close < sma) & (volume_z_val < -1)
        exit_setup = self.op.crossed(close, sma)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
