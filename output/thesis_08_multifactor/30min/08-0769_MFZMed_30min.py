
"""
name:    MFZMed_30min
summary: Z-Score: ZScore(1.2) — 30min
thesis:  multifactor | 30min
idea:    Multi-factor z-score
"""
class CustomStrategy(SimpleAlgorithm):

    z_window = 40
    z_threshold = 1.2
    rsi_window = 14
    adx_window = 14

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        high = self.data.pv_high
        low = self.data.pv_low

        price_z = self.feat.rolling_zscore(close, window=self.z_window)
        vol_z = self.feat.rolling_zscore(volume, window=self.z_window)
        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        adx = self.feat.adx(high, low, close, timeperiod=self.adx_window)

        momentum = self.feat.roc(close, timeperiod=self.rsi_window)
        mom_z = self.feat.rolling_zscore(momentum, window=self.z_window)

        composite = price_z + mom_z + vol_z
        trend_ok = adx > 20
        rsi_ok = (rsi > 30) & (rsi < 70)

        long_setup = (composite > self.z_threshold) & trend_ok & rsi_ok
        short_setup = (composite < -self.z_threshold) & trend_ok & rsi_ok
        exit_setup = (abs(composite) < 0.5) | (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
