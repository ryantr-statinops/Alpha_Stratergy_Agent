"""
name:    T08-C_a14_e2.0
summary: Agreed Volume Footprint
idea:    Follow institutional positioning via agreed volume z-score spike; direction confirmation via ROC and volume.
"""
class CustomStrategy(SimpleAlgorithm):
    agree_window = 14
    vol_window = 26
    return_window = 8


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        agreed_vol = self.data.fut_agreed_volume_vn30f1m_1d

        agree_z = self.feat.rolling_zscore(agreed_vol, window=self.agree_window)
        vol_ma = self.feat.sma(volume, timeperiod=self.vol_window)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        roc_val = self.feat.roc(close, timeperiod=8)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        institutional_activity = agree_z > 2.0

        long_setup = institutional_activity & (roc_val > 0) & (volume > vol_ma) & (adx_val > 15) & (return_roll > 0)
        short_setup = institutional_activity & (roc_val < 0) & (volume > vol_ma) & (adx_val > 15) & (return_roll < 0)
        exit_setup = (agree_z < 0.5) | (adx_val < 12)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

