
"""
name:    VFVolMed_30min
summary: Vol Surge: VolSurge(1.8x) — 30min
thesis:  volume_flow | 30min
idea:    Matched volume surge
"""
class CustomStrategy(SimpleAlgorithm):

    vol_window = 26
    surge_mult = 1.8

    return_window = 8
    return_threshold = 0.0003
    position_close_after_n_candles = 12
    adx_window = 14

    def __algorithm__(self):
        close = self.data.pv_close
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=14)

        vol_sma = self.feat.sma(matched_vol, timeperiod=self.vol_window)
        vol_q80 = self.feat.rolling_quantile(matched_vol, self.vol_window, 0.80)
        close_sma = self.feat.sma(close, timeperiod=self.vol_window)

        surge = (matched_vol > vol_sma * self.surge_mult) & (matched_vol > vol_q80)

        long_setup = ((surge & (close > close_sma)) & (return_roll > 0)) & (adx > 22)
        short_setup = ((surge & (close < close_sma)) & (return_roll < 0)) & (adx > 22)
        exit_setup = (((matched_vol < vol_sma) | self.op.crossed_below(close, close_sma)) | (abs(return_roll) < self.return_threshold)) | (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
