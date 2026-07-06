"""
name:    T08-D_l14_vw20_m1.0
summary: VWAP Divergence at Key Level
idea:    Price at key level AND beyond VWAP band = divergence from fair value; trade mean reversion with between-exit on VWAP cross.
"""
class CustomStrategy(SimpleAlgorithm):
    level_window = 14
    vwap_window = 20
    vwap_mult = 1.0


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        res_level = self.feat.rolling_max(close, window=self.level_window)
        sup_level = self.feat.rolling_min(close, window=self.level_window)
        vwap_val = self.feat.rolling_vwap(high, low, close, volume, window=self.vwap_window)
        vol_sma = self.feat.sma(volume, timeperiod=26)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=8)

        at_resistance = close >= res_level * 0.995
        at_support = close <= sup_level * 1.005
        over_extended_short = at_resistance & (close > vwap_val * (1 + self.vwap_mult / 100))
        over_extended_long = at_support & (close < vwap_val * (1 - self.vwap_mult / 100))

        short_setup = over_extended_short & (volume > vol_sma) & (adx_val > 15) & (return_roll < 0)
        long_setup = over_extended_long & (volume > vol_sma) & (adx_val > 15) & (return_roll > 0)
        exit_setup = (self.op.between(close, vwap_val * 0.999, vwap_val * 1.001)) | (adx_val < 12)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

