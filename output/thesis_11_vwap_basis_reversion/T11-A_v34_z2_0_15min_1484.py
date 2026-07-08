"""
name:    T11-A_v34_z2.0
summary: VWAP Basis Dual Z-Score
idea:    Mean-revert on dual z-score of VWAP distance and VN30 basis; long when both oversold, short when both overbought; exit on neutral reversion.
"""
class CustomStrategy(SimpleAlgorithm):
    z_entry = 2.0
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
        exit_setup = (self.op.abs(vwap_dist_z) < self.z_exit) | (self.op.abs(basis_z) < self.z_exit)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)

