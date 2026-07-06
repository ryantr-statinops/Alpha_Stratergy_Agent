"""
name:    T08-B_v20
summary: Volume Absorption
idea:    Detect liquidity absorption via matched volume spike + narrow range at key levels; trade post-absorption breakout.
"""
class CustomStrategy(SimpleAlgorithm):
    vol_window = 20
    return_window = 14


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d

        vol_ma = self.feat.sma(matched_vol, timeperiod=self.vol_window)
        vol_ratio = matched_vol / vol_ma
        range_pct = (high - low) / close
        range_ma = self.feat.sma(range_pct, timeperiod=20)
        adx_val = self.feat.adx(high, low, close, timeperiod=21)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        absorption = (vol_ratio > 1.5) & (range_pct < range_ma * 0.7)
        res_level = self.feat.rolling_max(close, window=20)
        sup_level = self.feat.rolling_min(close, window=20)

        at_resistance = close >= res_level * 0.995
        at_support = close <= sup_level * 1.005

        long_setup = at_support & absorption & (adx_val > 14) & (return_roll > 0)
        short_setup = at_resistance & absorption & (adx_val > 14) & (return_roll < 0)
        exit_setup = (vol_ratio < 1.0) | (adx_val < 10) | (return_roll == 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

