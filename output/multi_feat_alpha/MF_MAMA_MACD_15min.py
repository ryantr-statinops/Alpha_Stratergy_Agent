class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        mama_line, fama_line = self.feat.mama(close, fastlimit=0.5, slowlimit=0.05)
        macd_line, signal_line, histogram = self.feat.macd(close, fastperiod=12, slowperiod=26, signalperiod=9)

        long_setup = (mama_line > fama_line) & (histogram > 0)
        short_setup = (mama_line < fama_line) & (histogram < 0)
        exit_setup = self.op.crossed_above(mama_line, fama_line) | self.op.crossed_below(mama_line, fama_line) | self.op.crossed_above_value(histogram, 0) | self.op.crossed_below_value(histogram, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
