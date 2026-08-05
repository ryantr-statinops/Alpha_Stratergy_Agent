class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        volume_z = self.feat.volume_z(volume, timeperiod=20)
        trendmode = self.feat.trendmode(close)
        sma = self.feat.sma(close, timeperiod=10)

        long_setup = (volume_z > 1) & (trendmode > 0) & (close > sma)
        short_setup = (volume_z > 1) & (trendmode > 0) & (close < sma)
        exit_setup = self.op.crossed_below_value(volume_z, 0.5) | self.op.crossed_below_value(trendmode, 1) | self.op.crossed(close, sma)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
