"""
name:    MatchedValQ80
summary: Trade when matched value spikes above quantile 0.8
idea:    Matched value breakout for large flow detection
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        matched_val = self.data.fut_matched_value_vn30f1m_1d

        mv_mean = self.feat.rolling_mean(matched_val, window=14)
        close_mean = self.feat.rolling_mean(close, window=14)
        mv_q80 = self.feat.rolling_quantile(matched_val, 14, 0.8)

        long_setup = (matched_val > mv_q80) & (close > close_mean)
        short_setup = (matched_val > mv_q80) & (close < close_mean)
        exit_setup = matched_val < mv_mean

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
