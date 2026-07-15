class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        open_price = self.data.pv_open
        high = self.data.pv_high
        low = self.data.pv_low
        close = self.data.pv_close
        three_white_soldiers = self.feat.three_white_soldiers(open_price, high, low, close)
        sma = self.feat.sma(close, timeperiod=20)

        long_setup = (close > sma) & (three_white_soldiers >= 0)
        short_setup = (close < sma) & (three_white_soldiers <= 0)
        exit_setup = self.op.crossed(close, sma)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
