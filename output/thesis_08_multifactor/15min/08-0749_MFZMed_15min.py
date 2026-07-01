
"""
name:    MFZMed_15min
summary: Z-Score: ZScore(1.2) — 15min
thesis:  multifactor | 15min
idea:    Multi-factor z-score
"""
class CustomStrategy(SimpleAlgorithm):

    z_window = 26

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        high = self.data.pv_high
        low = self.data.pv_low

        price_z = self.feat.rolling_zscore(close, window=self.z_window)
        vol_z = self.feat.rolling_zscore(volume, window=self.z_window)
        rsi = self.feat.rsi(close, timeperiod=10)
        adx = self.feat.adx(high, low, close, timeperiod=10)

        momentum = self.feat.roc(close, timeperiod=10)
        mom_z = self.feat.rolling_zscore(momentum, window=self.z_window)

        composite = price_z + mom_z + vol_z
        trend_ok = adx > 20
        rsi_ok = (rsi > 30) & (rsi < 70)

        long_setup = (composite > 1.5) & trend_ok & rsi_ok
        short_setup = (composite < -1.5) & trend_ok & rsi_ok
        exit_setup = (abs(composite) < 0.5) | (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
