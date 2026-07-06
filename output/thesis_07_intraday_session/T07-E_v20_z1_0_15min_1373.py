"""
name:    T07-E_v20_z1.0
summary: Session VWAP Bounce
idea:    Price deviates ±z% from VWAP then bounces back with return_roll confirmation; exit on VWAP cross.
"""
class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:15"]
    position_close_ranges = ["04:20-04:30", "07:30-07:45"]


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        vwap_val = self.feat.rolling_vwap(high, low, close, volume, window=20)
        vol_sma = self.feat.sma(volume, timeperiod=14)
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=5)

        upper_band = vwap_val * (1 + 1.0 / 100)
        lower_band = vwap_val * (1 - 1.0 / 100)

        long_setup = (close < lower_band) & (return_roll > 0) & (volume > vol_sma * 0.7)
        short_setup = (close > upper_band) & (return_roll < 0) & (volume > vol_sma * 0.7)
        exit_setup = self.op.crossed_above(close, vwap_val) | self.op.crossed_below(close, vwap_val)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

