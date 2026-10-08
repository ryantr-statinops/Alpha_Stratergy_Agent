class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        open_ = self.data.pv_open
        three_white = self.feat.three_white_soldiers(open_, high, low, close)
        adx = self.feat.adx(high, low, close, timeperiod=14)
        sma10 = self.feat.sma(close, timeperiod=10)

        long_setup = (three_white > 0) & (adx > 20)
        short_setup = (adx > 20) & (close < sma10)
        exit_setup = self.op.crossed_below_value(adx, 20) | self.op.crossed(close, sma10)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
