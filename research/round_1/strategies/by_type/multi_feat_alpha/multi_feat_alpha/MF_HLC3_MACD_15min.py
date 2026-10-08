class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        hlc3 = self.feat.hlc3(high, low, close)
        macd_line, signal_line, histogram = self.feat.macd(close, fastperiod=12, slowperiod=26, signalperiod=9)

        long_setup = (close > hlc3) & (histogram > 0)
        short_setup = (close < hlc3) & (histogram < 0)
        exit_setup = self.op.crossed(close, hlc3) | self.op.crossed_above_value(histogram, 0) | self.op.crossed_below_value(histogram, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
