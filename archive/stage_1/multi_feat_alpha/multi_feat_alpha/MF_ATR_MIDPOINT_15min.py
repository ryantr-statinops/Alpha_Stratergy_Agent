class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        atr = self.feat.atr(high, low, close, timeperiod=14)
        midpoint = self.feat.midpoint(close, timeperiod=14)
        atr_ma = self.feat.rolling_mean(atr, window=20)

        long_setup = (atr > atr_ma) & (close > midpoint)
        short_setup = (atr > atr_ma) & (close < midpoint)
        exit_setup = self.op.crossed(close, midpoint) | (atr < atr_ma)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
