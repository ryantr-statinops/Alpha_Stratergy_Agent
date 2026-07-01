"""
name:    MatchedVolMean14
summary: Trade when matched volume exceeds rolling mean
idea:    Volume-based signal using VnFuture matched volume
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d

        vol_mean = self.feat.rolling_mean(matched_vol, window=14)

        long_setup = (matched_vol > vol_mean)
        short_setup = (matched_vol < vol_mean * 0.8)
        exit_setup = (matched_vol < vol_mean * 0.7) | (matched_vol > vol_mean * 1.3)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
