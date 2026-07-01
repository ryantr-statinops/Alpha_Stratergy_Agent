"""
name:    OpenInterestMean14
summary: Trade when open interest and price align with trend
idea:    Open interest confirmation for trend strength
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        oi = self.data.fut_open_interest_vn30f1m_1d

        oi_mean = self.feat.rolling_mean(oi, window=14)
        close_mean = self.feat.rolling_mean(close, window=14)

        long_setup = (oi > oi_mean) & (close > close_mean)
        short_setup = (oi < oi_mean) & (close < close_mean)
        exit_setup = (oi < oi_mean * 0.95) | (close < close_mean * 0.98)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
