"""
name:    T08-B_l14_v20
summary: Volume Climax Absorption
idea:    Volume spike + tight range at key level + close in rejection half = climax absorption; trade the reversal with ADX + return_roll exit.
"""
class CustomStrategy(SimpleAlgorithm):
    level_window = 14
    vol_window = 20


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        res_level = self.feat.rolling_max(close, window=self.level_window)
        sup_level = self.feat.rolling_min(close, window=self.level_window)
        midpoint = (high + low) * 0.5
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        adx_val = self.feat.adx(high, low, close, timeperiod=21)
        natr_val = self.feat.natr(high, low, close, timeperiod=14)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=14)

        at_resistance = close >= res_level * 0.995
        at_support = close <= sup_level * 1.005
        close_lower_half = close < midpoint
        close_upper_half = close > midpoint
        vol_spike = volume > vol_sma * 1.5
        tight_range = (high - low) < natr_val * 0.8

        short_setup = at_resistance & vol_spike & tight_range & close_lower_half & (adx_val > 14) & (return_roll < 0)
        long_setup = at_support & vol_spike & tight_range & close_upper_half & (adx_val > 14) & (return_roll > 0)
        exit_setup = (adx_val < 10)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

