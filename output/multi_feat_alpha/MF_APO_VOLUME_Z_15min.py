class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        apo = self.feat.apo(close, fastperiod=12, slowperiod=26, matype=0)
        volume_z = self.feat.volume_z(volume, timeperiod=20)

        long_setup = (apo > 0) & (volume_z > 0)
        short_setup = (apo < 0) & (volume_z > 0)
        exit_setup = self.op.crossed(apo, 0) | (volume_z < -1)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
