class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vwap = self.feat.vwap(high, low, close, volume)
        rocp = self.feat.rocp(close, timeperiod=5)

        long_setup = (close > vwap) & (rocp > 0)
        short_setup = (close < vwap) & (rocp < 0)
        exit_setup = self.op.crossed(close, vwap) | self.op.crossed_above_value(rocp, 0) | self.op.crossed_below_value(rocp, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
