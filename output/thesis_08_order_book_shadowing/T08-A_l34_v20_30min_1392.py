"""
name:    T08-A_l34_v20
summary: Key Level Wick Rejection
idea:    Detect rejection at resistance/support via candle midpoint; when close is in opposite half at key level = absorption, trade reversal.
"""
class CustomStrategy(SimpleAlgorithm):
    level_window = 34
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
        adx_val = self.feat.adx(high, low, close, timeperiod=14)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=8)

        at_resistance = close >= res_level * 0.995
        at_support = close <= sup_level * 1.005
        close_lower_half = close < midpoint
        close_upper_half = close > midpoint

        rejected_resistance = at_resistance & close_lower_half
        rejected_support = at_support & close_upper_half

        long_setup = rejected_support & (volume > vol_sma) & (adx_val > 15) & (return_roll > 0)
        short_setup = rejected_resistance & (volume > vol_sma) & (adx_val > 15) & (return_roll < 0)
        exit_setup = (adx_val < 12) | (return_roll < -0.001) | (return_roll > 0.001)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

