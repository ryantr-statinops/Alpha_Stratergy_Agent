class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        open_ = self.data.pv_open
        hammer = self.feat.hammer(open_, high, low, close)
        rsi = self.feat.rsi(close, timeperiod=10)
        sma10 = self.feat.sma(close, timeperiod=10)

        long_setup = (hammer > 0) & (rsi > 50)
        short_setup = (rsi < 50) & (close < sma10)
        exit_setup = self.op.crossed(close, sma10) | self.op.crossed_above_value(rsi, 50) | self.op.crossed_below_value(rsi, 50)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
