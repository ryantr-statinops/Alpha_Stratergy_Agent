class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        rsi = self.feat.rsi(close, timeperiod=10)
        sma10 = self.feat.sma(close, timeperiod=10)

        long_entry = (rsi > 50) & (close > sma10)
        short_entry = (rsi < 50) & (close < sma10)
        hold_long = self.op.hold_for(long_entry, 2)
        hold_short = self.op.hold_for(short_entry, 2)
        exit_setup = self.op.crossed(close, sma10) | self.op.crossed_below_value(rsi, 50) | self.op.crossed_above_value(rsi, 50)

        long_signal = hold_long & (~exit_setup)
        short_signal = hold_short & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
