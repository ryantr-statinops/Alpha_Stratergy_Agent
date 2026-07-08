"""
name:    T11-A_v34_z2.5
summary: VWAP Basis Dual Z-Score
idea:    Mean-revert on dual z-score of VWAP distance and VN30 basis; long when both oversold, short when both overbought; exit on neutral reversion.
"""
class CustomStrategy(SimpleAlgorithm):
    z_entry = 2.5
    z_exit = 1.0


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close

        vwap_val = self.feat.rolling_vwap(high, low, close, volume, window=34)
        vwap_dist = close - vwap_val
        vwap_dist_z = self.feat.rolling_zscore(vwap_dist, window=34)

        basis = close - vn30_close
        basis_z = self.feat.rolling_zscore(basis, window=34)

        long_setup = (vwap_dist_z < -self.z_entry) & (basis_z < -self.z_entry)
        short_setup = (vwap_dist_z > self.z_entry) & (basis_z > self.z_entry)
        exit_setup = (self.op.abs_op(vwap_dist_z) < self.z_exit) | (self.op.abs_op(basis_z) < self.z_exit)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

