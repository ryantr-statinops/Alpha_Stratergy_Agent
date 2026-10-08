class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        ema = self.feat.ema(close, timeperiod=10)
        rsi = self.feat.rsi(close, timeperiod=10)

        long_setup = (close > ema) & (rsi > 50)
        short_setup = (close < ema) & (rsi < 50)
        exit_setup = self.op.crossed(close, ema) | self.op.crossed_above_value(rsi, 50) | self.op.crossed_below_value(rsi, 50)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
