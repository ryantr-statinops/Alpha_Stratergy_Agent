"""
name: MACD Compression to Expansion (60-Min)

"""

class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]

    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        open_ = self.data.pv_open

        _, _, hist_core = self.feat.macd(
            close,
            fastperiod=2,
            slowperiod=7,
            signalperiod=9
        )

        histogram = self.op.fillna(hist_core, value=0)

        prev_hist = self.op.fillna(
            self.op.previous(histogram, periods=1),
            value=0
        )

        long_setup = (prev_hist <= 0) & (histogram > 0) & (close > open_)
        short_setup = (prev_hist >= 0) & (histogram < 0) & (close < open_)

        long_exit = (histogram <= 0)
        short_exit = (histogram >= 0)
        exit_setup = long_exit | short_exit

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)