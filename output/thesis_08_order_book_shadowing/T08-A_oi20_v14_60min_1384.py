"""
name:    T08-A_oi20_v14
summary: OI Wall Detection
idea:    Spot resistance/support walls via OI divergence: OI drops at key levels = spoof orders unwinding → breakout imminent.
"""
class CustomStrategy(SimpleAlgorithm):
    oi_window = 20
    vol_window = 14
    return_window = 14


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        oi = self.data.fut_open_interest_vn30f1m_1d

        oi_z = self.feat.rolling_zscore(oi, window=self.oi_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        res_level = self.feat.rolling_max(close, window=self.oi_window)
        sup_level = self.feat.rolling_min(close, window=self.oi_window)
        adx_val = self.feat.adx(high, low, close, timeperiod=21)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        at_resistance = close >= res_level * 0.995
        at_support = close <= sup_level * 1.005
        oi_collapse = oi_z < -1.0

        long_setup = at_support & oi_collapse & (volume > vol_sma) & (adx_val > 14)
        short_setup = at_resistance & oi_collapse & (volume > vol_sma) & (adx_val > 14)
        exit_setup = (oi_z > 0) | (adx_val < 10)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

