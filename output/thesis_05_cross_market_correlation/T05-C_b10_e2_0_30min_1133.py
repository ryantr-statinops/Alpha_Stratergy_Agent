"""
name:    T05-C_b10_e2.0
summary: Futures-Cash Basis Extreme
idea:    Trade basis extreme z-score deviations; entry when basis diverges from its mean under low volume.
"""
class CustomStrategy(SimpleAlgorithm):
    basis_window = 10


    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        high = self.data.pv_high
        low = self.data.pv_low

        basis = close - vn30_close
        basis_z = self.feat.rolling_zscore(basis, window=self.basis_window)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d
        vol_sma = self.feat.sma(matched_vol, timeperiod=self.basis_window)

        long_setup = (basis_z < -2.0) & (matched_vol < vol_sma) & (adx_val > 18)
        short_setup = (basis_z > 2.0) & (matched_vol < vol_sma) & (adx_val > 18)
        exit_setup = self.op.between(basis_z, -1, 1) | (adx_val < 12)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

