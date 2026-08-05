class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        open_ = self.data.pv_open
        volume = self.data.pv_volume
        engulfing = self.feat.engulfing_pattern(open_, high, low, close)
        mfi = self.feat.mfi(high, low, close, volume, timeperiod=10)

        long_setup = (engulfing > 0) & (mfi > 50)
        short_setup = (engulfing < 0) & (mfi < 50)
        exit_setup = self.op.crossed_above_value(mfi, 50) | self.op.crossed_below_value(mfi, 50) | self.op.crossed(engulfing, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
