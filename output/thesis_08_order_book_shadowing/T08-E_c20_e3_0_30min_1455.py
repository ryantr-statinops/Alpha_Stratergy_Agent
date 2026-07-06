"""
name:    T08-E_c20_e3.0
summary: Multi-Confirmation Composite
idea:    OHLCV-only composite of price_z + vol_z + (-range_z) + mom_z; exit when composite decays or ADX fades.
"""
class CustomStrategy(SimpleAlgorithm):
    composite_window = 20


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        price_z = self.feat.rolling_zscore(close, window=self.composite_window)
        vol_z = self.feat.volume_z(volume, timeperiod=self.composite_window)
        natr_val = self.feat.natr(high, low, close, timeperiod=14)
        range_z = self.feat.rolling_zscore(natr_val, window=self.composite_window)
        mom = self.feat.roc(close, timeperiod=8)
        mom_z = self.feat.rolling_zscore(mom, window=self.composite_window)

        composite = price_z + vol_z + (-range_z) + mom_z

        vol_sma = self.feat.sma(volume, timeperiod=26)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=8)

        long_setup = (composite > 3.0) & (volume > vol_sma) & (adx_val > 18) & (return_roll > 0)
        short_setup = (composite < -3.0) & (volume > vol_sma) & (adx_val > 18) & (return_roll < 0)
        exit_setup = (self.op.abs(composite) < 0.5) | (adx_val < 12)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

