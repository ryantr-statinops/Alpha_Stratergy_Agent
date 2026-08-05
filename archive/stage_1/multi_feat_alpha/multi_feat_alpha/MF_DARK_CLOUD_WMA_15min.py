class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        open_ = self.data.pv_open
        dark_cloud = self.feat.dark_cloud_cover(open_, high, low, close)
        wma = self.feat.wma(close, timeperiod=10)

        long_setup = (close > wma)
        short_setup = (dark_cloud < 0) & (close < wma)
        exit_setup = self.op.crossed(close, wma)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
