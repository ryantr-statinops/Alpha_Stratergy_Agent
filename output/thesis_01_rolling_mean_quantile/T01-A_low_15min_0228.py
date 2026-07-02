"""
name:    T01-A_low
summary: Price vs Rolling Mean
idea:    Compare price to rolling mean at multiple price sources (close, typical, weighted, median, OHLC4, high, low, volume, VWAP); long above, short below mean.
"""
class CustomStrategy(SimpleAlgorithm):
    mean_window = 10


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        open_price = self.data.pv_open

        low_px = self.data.pv_low

        mean = self.feat.rolling_mean(low_px, window=self.mean_window)

        long_setup = low_px > mean
        short_setup = low_px < mean
        exit_setup = self.op.crossed_below(low_px, mean) | self.op.crossed_above(low_px, mean)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

