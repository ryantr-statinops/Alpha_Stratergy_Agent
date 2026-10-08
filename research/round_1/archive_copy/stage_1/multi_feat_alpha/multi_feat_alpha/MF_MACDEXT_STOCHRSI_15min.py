class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        macd_line, signal_line, histogram = self.feat.macdext(close, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)
        fastk, fastd = self.feat.stochrsi(close, timeperiod=14, fastk_period=5, fastd_period=3)

        long_setup = (histogram > 0) & (fastk > 50)
        short_setup = (histogram < 0) & (fastk < 50)
        exit_setup = self.op.crossed_above_value(histogram, 0) | self.op.crossed_below_value(histogram, 0) | self.op.crossed_above_value(fastk, 50) | self.op.crossed_below_value(fastk, 50)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
