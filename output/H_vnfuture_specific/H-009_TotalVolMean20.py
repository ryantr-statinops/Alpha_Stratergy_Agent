"""
name:    TotalVolMean20
summary: Trade when total volume spikes confirm price direction
idea:    Total volume confirmation for VnFuture breakouts
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        total_vol = self.data.fut_total_volume_vn30f1m_1d

        tv_mean = self.feat.rolling_mean(total_vol, window=20)
        close_mean = self.feat.rolling_mean(close, window=20)

        long_setup = (total_vol > tv_mean) & (close > close_mean)
        short_setup = (total_vol > tv_mean) & (close < close_mean)
        exit_setup = total_vol < tv_mean * 0.8

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
