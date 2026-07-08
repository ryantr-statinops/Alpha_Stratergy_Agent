"""
name:    T11-C_v20_z2.0_m3.0
summary: VWAP Basis with ATR Stop
idea:    Same dual z-score logic + ATR trailing stop for capital-preserving exits when price breaks away from the 20-period MA.
"""
class CustomStrategy(SimpleAlgorithm):
    z_entry = 2.0
    z_exit = 1.0
    atr_stop_mult = 3.0


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

        atr = self.feat.atr(high, low, close, timeperiod=14)
        ma20 = self.feat.sma(close, timeperiod=20)
        atr_stop = (
            (close < ma20 - self.atr_stop_mult * atr) |
            (close > ma20 + self.atr_stop_mult * atr)
        )

        long_setup = (vwap_dist_z < -self.z_entry) & (basis_z < -self.z_entry)
        short_setup = (vwap_dist_z > self.z_entry) & (basis_z > self.z_entry)
        exit_setup = (
            (self.op.abs(vwap_dist_z) < self.z_exit) |
            (self.op.abs(basis_z) < self.z_exit) |
            atr_stop
        )

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

