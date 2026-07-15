class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        fastk, fastd = self.feat.stochrsi(close, timeperiod=10, fastk_period=5, fastd_period=3)
        sma = self.feat.sma(close, timeperiod=20)

        long_setup = (fastk > 50) & (close > sma)
        short_setup = (fastk < 50) & (close < sma)
        exit_setup = self.op.crossed(close, sma)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
