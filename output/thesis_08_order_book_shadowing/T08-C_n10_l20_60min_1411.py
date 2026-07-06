"""
name:    T08-C_n10_l20
summary: Range Compression Absorption
idea:    Narrow range (NATR < SMA × 0.8) at key level = absorption complete, trade the impending breakout direction via return_roll.
"""
class CustomStrategy(SimpleAlgorithm):
    natr_window = 10
    level_window = 20


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        res_level = self.feat.rolling_max(close, window=self.level_window)
        sup_level = self.feat.rolling_min(close, window=self.level_window)
        natr_val = self.feat.natr(high, low, close, timeperiod=self.natr_window)
        natr_sma = self.feat.sma(natr_val, timeperiod=self.natr_window)
        vol_sma = self.feat.sma(volume, timeperiod=34)
        adx_val = self.feat.adx(high, low, close, timeperiod=21)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=14)

        at_resistance = close >= res_level * 0.995
        at_support = close <= sup_level * 1.005
        tight_range = natr_val < natr_sma * 0.8

        short_setup = at_resistance & tight_range & (volume > vol_sma) & (adx_val > 14) & (return_roll < 0)
        long_setup = at_support & tight_range & (volume > vol_sma) & (adx_val > 14) & (return_roll > 0)
        exit_setup = (adx_val < 10) | (return_roll < -0.001) | (return_roll > 0.001) | (natr_val > natr_sma * 2.0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

