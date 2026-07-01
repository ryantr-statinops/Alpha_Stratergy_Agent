
"""
name:    VFVolGentle_60min
summary: Vol Surge: VolSurge(1.2x) — 60min
thesis:  volume_flow | 60min
idea:    Matched volume surge
"""
class CustomStrategy(SimpleAlgorithm):

    vol_window = 34
    surge_mult = 1.2

    def __algorithm__(self):
        close = self.data.pv_close
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d

        vol_sma = self.feat.sma(matched_vol, timeperiod=self.vol_window)
        vol_q80 = self.feat.rolling_quantile(matched_vol, self.vol_window, 0.80)
        close_sma = self.feat.sma(close, timeperiod=self.vol_window)

        surge = (matched_vol > vol_sma * self.surge_mult) & (matched_vol > vol_q80)

        long_setup = surge & (close > close_sma)
        short_setup = surge & (close < close_sma)
        exit_setup = (matched_vol < vol_sma) | self.op.crossed_below(close, close_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
