"""
name:    OpenInterestQ80
summary: Trade when open interest breaks quantile 0.8
idea:    Open interest quantile breakout for institutional flow detection
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        oi = self.data.fut_open_interest_vn30f1m_1d

        oi_q80 = self.feat.rolling_quantile(oi, 20, 0.8)
        close_mean = self.feat.rolling_mean(close, window=20)

        long_setup = (oi > oi_q80) & (close > close_mean)
        short_setup = (oi > oi_q80) & (close < close_mean)
        exit_setup = oi < self.feat.rolling_quantile(oi, 20, 0.5)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
