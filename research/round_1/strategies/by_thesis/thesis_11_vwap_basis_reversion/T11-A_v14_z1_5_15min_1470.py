"""
name:    T11-A_v14_z1.5
summary: VWAP Basis Dual Z-Score
idea:    Mean-revert on dual z-score of VWAP distance and VN30 basis; long when both oversold, short when both overbought; exit on neutral reversion.
"""
class CustomStrategy(SimpleAlgorithm):
    z_entry = 1.5
    z_exit = 1.0
    atr_stop_mult = 2.5


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close

        vwap_val = self.feat.rolling_vwap(high, low, close, volume, window=14)
        vwap_dist = close - vwap_val
        vwap_dist_z = self.feat.rolling_zscore(vwap_dist, window=14)

        basis = close - vn30_close
        basis_z = self.feat.rolling_zscore(basis, window=14)

        atr = self.feat.atr(high, low, close, timeperiod=14)
        ma20 = self.feat.sma(close, timeperiod=20)
        trend_up = close > ma20 + self.atr_stop_mult * atr
        trend_down = close < ma20 - self.atr_stop_mult * atr

        mr_long = (vwap_dist_z < -self.z_entry) & (basis_z < -self.z_entry) & (~trend_down)
        mr_short = (vwap_dist_z > self.z_entry) & (basis_z > self.z_entry) & (~trend_up)
        tf_long = trend_up
        tf_short = trend_down

        long_setup = mr_long | tf_long
        short_setup = mr_short | tf_short

        exit_reversion = (self.op.abs(vwap_dist_z) < self.z_exit) | (self.op.abs(basis_z) < self.z_exit)
        exit_setup = exit_reversion & (~trend_up) & (~trend_down)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)

