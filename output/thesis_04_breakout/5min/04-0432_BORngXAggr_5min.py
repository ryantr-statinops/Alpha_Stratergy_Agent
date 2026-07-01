
"""
name:    BORngXAggr_5min
summary: Range Exp: Range(3.0x) — 5min
thesis:  breakout | 5min
idea:    Range expansion breakout
"""
class CustomStrategy(SimpleAlgorithm):

    range_window = 8
    vol_window = 14

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        daily_range = high - low
        avg_range = self.feat.sma(daily_range, timeperiod=self.range_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        range_expansion = daily_range > avg_range * 1.5
        vol_confirmation = volume > vol_sma

        long_setup = range_expansion & vol_confirmation & (close > (high + low) / 2)
        short_setup = range_expansion & vol_confirmation & (close < (high + low) / 2)
        exit_setup = (daily_range < avg_range) | (volume < vol_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
