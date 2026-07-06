"""
name:    T08-E_c14_e4.0
summary: Composite Shadow
idea:    Multi-proxy composite (OI, matched, agreed, ratio, basis) for high-conviction institutional flow detection.
"""
class CustomStrategy(SimpleAlgorithm):
    composite_window = 14
    vol_window = 20


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        oi = self.data.fut_open_interest_vn30f1m_1d
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d
        matched_val = self.data.fut_matched_value_vn30f1m_1d
        agreed_vol = self.data.fut_agreed_volume_vn30f1m_1d
        vn30_close = self.data.pv_vn30_close

        oi_z = self.feat.rolling_zscore(oi, window=self.composite_window)
        matched_z = self.feat.rolling_zscore(matched_vol, window=self.composite_window)
        agree_z = self.feat.rolling_zscore(agreed_vol, window=self.composite_window)
        lot_ratio = matched_val / matched_vol
        ratio_z = self.feat.rolling_zscore(lot_ratio, window=self.composite_window)
        premium = close / vn30_close
        premium_z = self.feat.rolling_zscore(premium, window=self.composite_window)

        shadow_composite = (-oi_z) + matched_z + agree_z + ratio_z + premium_z

        vol_ma = self.feat.sma(volume, timeperiod=self.vol_window)
        adx_val = self.feat.adx(high, low, close, timeperiod=10)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=3)

        long_setup = (shadow_composite > 4.0) & (volume > vol_ma) & (adx_val > 22) & (return_roll > 0)
        short_setup = (shadow_composite < -4.0) & (volume > vol_ma) & (adx_val > 22) & (return_roll < 0)
        exit_setup = (self.op.abs(shadow_composite) < 0.5) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

