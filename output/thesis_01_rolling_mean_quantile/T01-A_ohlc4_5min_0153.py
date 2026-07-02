"""
name:    T01-A_ohlc4
summary: Price vs Rolling Mean
idea:    Compare price to rolling mean at multiple price sources (close, typical, weighted, median, OHLC4, high, low, volume, VWAP); long above, short below mean.
"""
class CustomStrategy(SimpleAlgorithm):
    mean_window = 200


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        open_price = self.data.pv_open

        ohlc4 = self.feat.ohlc4(open_price, high, low, close)

        mean = self.feat.rolling_mean(ohlc4, window=self.mean_window)

        long_setup = ohlc4 > mean
        short_setup = ohlc4 < mean
        exit_setup = self.op.crossed_below(ohlc4, mean) | self.op.crossed_above(ohlc4, mean)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

