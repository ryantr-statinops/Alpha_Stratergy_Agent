"""
name:    T11-D_v20_z2.0_ae25_ax18_m3.5
summary: VWAP Basis Regime Switching
idea:    Dual-mode: mean-revert in ranging (ADX<exit) via dual z-score; trend-follow in trending (ADX>entry) via VWAP+basis+momentum alignment; regime crossover exits for clean transitions.
"""
class CustomStrategy(SimpleAlgorithm):
    z_entry = 2.0
    z_exit = 1.0
    atr_stop_mult = 3.5


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
        ranging = adx_val < 18
        trending = adx_val > 25

        atr = self.feat.atr(high, low, close, timeperiod=14)
        ma20 = self.feat.sma(close, timeperiod=20)
        trend_up = close > ma20 + self.atr_stop_mult * atr
        trend_down = close < ma20 - self.atr_stop_mult * atr

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=5)

        range_to_trend = self.op.crossed_above(adx_val, 25)
        trend_to_range = self.op.crossed_below(adx_val, 18)

        mr_long = ranging & (vwap_dist_z < -self.z_entry) & (basis_z < -self.z_entry) & (~trend_down)
        mr_short = ranging & (vwap_dist_z > self.z_entry) & (basis_z > self.z_entry) & (~trend_up)

        tf_long = trending & (close > vwap_val) & (basis > 0) & (return_roll > 0) & trend_up
        tf_short = trending & (close < vwap_val) & (basis < 0) & (return_roll < 0) & trend_down

        long_setup = mr_long | tf_long
        short_setup = mr_short | tf_short

        exit_reversion = (self.op.abs(vwap_dist_z) < self.z_exit) | (self.op.abs(basis_z) < self.z_exit)
        exit_regime = range_to_trend | trend_to_range
        exit_setup = (exit_reversion | exit_regime) & (~trend_up) & (~trend_down)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)

