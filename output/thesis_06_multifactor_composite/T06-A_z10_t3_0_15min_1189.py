"""
name:    T06-A_z10_t3.0
summary: 3-Factor Z-Score Composite
idea:    Composite z-score of price, momentum, and volume; strong/weak position sizing based on conviction levels.
"""
class CustomStrategy(SimpleAlgorithm):
    z_window = 10
    z_threshold = 3.0
    thesis_group = "06"

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        high = self.data.pv_high
        low = self.data.pv_low

        price_z = self.feat.rolling_zscore(close, window=self.z_window)
        vol_z = self.feat.volume_z(volume, timeperiod=self.z_window)
        momentum = self.feat.roc(close, timeperiod=10)
        mom_z = self.feat.rolling_zscore(momentum, window=self.z_window)

        composite = price_z + mom_z + vol_z
        rsi = self.feat.rsi(close, timeperiod=10)
        rsi_ok = self.op.between(rsi, 30, 70)

        adx_val = self.feat.adx(high, low, close, timeperiod=10)
        return_roll = self.feat.returns(close, periods=5)

        core_long = (composite > self.z_threshold)
        core_short = (composite < -self.z_threshold)

        strong_long = core_long & rsi_ok & (adx_val > 22) & (vol_z > 0) & (return_roll > 0)
        weak_long = core_long & rsi_ok & (adx_val > 18) & (return_roll > 0)
        strong_short = core_short & rsi_ok & (adx_val > 22) & (vol_z < 0) & (return_roll < 0)
        weak_short = core_short & rsi_ok & (adx_val > 18) & (return_roll < 0)

        exit_setup = (self.op.abs(composite) < 0.5) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-1)

