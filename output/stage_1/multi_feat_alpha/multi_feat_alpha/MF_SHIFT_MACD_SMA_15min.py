class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        macd, macd_signal, macd_hist = self.feat.macd(close, fastperiod=5, slowperiod=13, signalperiod=5)
        sma10 = self.feat.sma(close, timeperiod=10)
        macd_prev = self.op.shift(macd, 1)

        long_setup = (macd > 0) & (macd_prev > 0) & (close > sma10)
        short_setup = (macd < 0) & (macd_prev < 0) & (close < sma10)
        exit_setup = self.op.crossed(close, sma10) | self.op.crossed_above_value(macd, 0) | self.op.crossed_below_value(macd, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
