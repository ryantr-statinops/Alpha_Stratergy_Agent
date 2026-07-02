"""
name:    T01-A_median
summary: Price vs Rolling Mean
idea:    Compare price to rolling mean at multiple price sources (close, typical, weighted, median, OHLC4, high, low, volume, VWAP); long above, short below mean.
"""
class CustomStrategy(SimpleAlgorithm):
    mean_window = 14
    thesis_group = "01"

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        open_price = self.data.pv_open

        median = self.feat.medprice(high, low)

        mean = self.feat.rolling_mean(median, window=self.mean_window)

        long_setup = median > mean
        short_setup = median < mean
        exit_setup = self.op.crossed_below(median, mean) | self.op.crossed_above(median, mean)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

