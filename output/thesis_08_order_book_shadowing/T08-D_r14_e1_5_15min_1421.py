"""
name:    T08-D_r14_e1.5
summary: Large Lot Ratio
idea:    Detect institutional-size trades via matched value/volume ratio; combine with basis premium for direction.
"""
class CustomStrategy(SimpleAlgorithm):
    ratio_window = 14
    vol_window = 20
    return_window = 5


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d
        matched_val = self.data.fut_matched_value_vn30f1m_1d
        vn30_close = self.data.pv_vn30_close

        lot_ratio = matched_val / matched_vol
        ratio_z = self.feat.rolling_zscore(lot_ratio, window=self.ratio_window)
        vol_ma = self.feat.sma(volume, timeperiod=self.vol_window)
        adx_val = self.feat.adx(high, low, close, timeperiod=10)
        premium = close / vn30_close
        premium_z = self.feat.rolling_zscore(premium, window=self.ratio_window)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        large_lots = ratio_z > 1.5

        long_setup = large_lots & (premium_z > 0) & (volume > vol_ma) & (adx_val > 18) & (return_roll > 0)
        short_setup = large_lots & (premium_z < 0) & (volume > vol_ma) & (adx_val > 18) & (return_roll < 0)
        exit_setup = (ratio_z < 0) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

