"""
name:    T07-A_f8_v20
summary: Open Drive
idea:    Morning momentum continuation: close > SMA + volume spike + return_roll > 0 in first 30 min of session.
"""
class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-02:30"]
    position_close_ranges = ["04:20-04:30"]


    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        vol_sma = self.feat.sma(volume, timeperiod=20)
        mean_val = self.feat.sma(close, timeperiod=8)
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=3)

        long_setup = (close > mean_val) & (volume > vol_sma) & (return_roll > 0)
        short_setup = (close < mean_val) & (volume > vol_sma) & (return_roll < 0)
        exit_setup = (return_roll < 0) | (return_roll > 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

