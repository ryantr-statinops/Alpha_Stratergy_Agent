"""
name:    T07-C_r3_v20_m2.0
summary: Close Squeeze
idea:    Afternoon breakout: ROC > 0 + volume × mult spike + ADX > entry; exit before ATC.
"""
class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["13:00-14:15"]
    position_close_ranges = ["14:30-14:45"]


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        roc_val = self.feat.roc(close, timeperiod=3)
        vol_sma = self.feat.sma(volume, timeperiod=20)
        adx_val = self.feat.adx(high, low, close, timeperiod=7)

        long_setup = (roc_val > 0) & (volume > vol_sma * 2.0) & (adx_val > 22)
        short_setup = (roc_val < 0) & (volume > vol_sma * 2.0) & (adx_val > 22)
        exit_setup = (roc_val < 0) | (roc_val > 0) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

