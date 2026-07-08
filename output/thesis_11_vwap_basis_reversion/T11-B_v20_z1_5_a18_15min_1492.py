"""
name:    T11-B_v20_z1.5_a18
summary: VWAP Basis with ADX Filter
idea:    Same dual z-score logic + ADX trending filter: only enter when ADX < threshold to avoid mean-reverting against strong trends.
"""
class CustomStrategy(SimpleAlgorithm):
    z_entry = 1.5
    z_exit = 1.0


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close

        vwap_val = self.feat.rolling_vwap(high, low, close, volume, window=20)
        vwap_dist = close - vwap_val
        vwap_dist_z = self.feat.rolling_zscore(vwap_dist, window=20)

        basis = close - vn30_close
        basis_z = self.feat.rolling_zscore(basis, window=20)

        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        trend_ok = adx_val < 18

        long_setup = (vwap_dist_z < -self.z_entry) & (basis_z < -self.z_entry) & trend_ok
        short_setup = (vwap_dist_z > self.z_entry) & (basis_z > self.z_entry) & trend_ok
        exit_setup = (
            (self.op.abs_op(vwap_dist_z) < self.z_exit) |
            (self.op.abs_op(basis_z) < self.z_exit) |
            (adx_val > 15)
        )

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

