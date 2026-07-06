"""
name:    T07-D_b20_m2.5_v14
summary: Pre-ATC Mean Rev
idea:    Late afternoon BBands extreme touch + volume confirm; mean revert before ATC close.
"""
class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["06:45-07:20"]
    position_close_ranges = ["07:20-07:45"]


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        upper, mid, lower = self.feat.bbands(close, timeperiod=20, nbdevup=2.5, nbdevdn=2.5)
        vol_sma = self.feat.sma(volume, timeperiod=14)
        mean_val = self.feat.sma(close, timeperiod=13)
        adx_val = self.feat.adx(high, low, close, timeperiod=10)

        long_setup = (close < lower) & (volume > vol_sma) & (adx_val < 20)
        short_setup = (close > upper) & (volume > vol_sma) & (adx_val < 20)
        exit_setup = self.op.crossed_above(close, mean_val) | self.op.crossed_below(close, mean_val) | (adx_val > 25)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

