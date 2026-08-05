class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        rolling_rank = self.feat.rolling_rank(close, window=20)
        macd_line, signal_line, histogram = self.feat.macdfix(close, signalperiod=9)

        long_setup = (rolling_rank > 0.8) & (histogram > 0)
        short_setup = (rolling_rank < 0.2) & (histogram < 0)
        exit_setup = self.op.crossed_below_value(rolling_rank, 0.5) | self.op.crossed_above_value(rolling_rank, 0.5) | self.op.crossed(histogram, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
