"""
name:    T07-B_r7_v14
summary: Lunch Revert
idea:    Pre-lunch mean reversion: RSI > 70 (short) or RSI < 30 (long) before lunch close.
"""
class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["03:30-04:15"]
    position_close_ranges = ["04:20-04:30"]


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        rsi_val = self.feat.rsi(close, timeperiod=7)
        vol_sma = self.feat.sma(volume, timeperiod=14)
        adx_val = self.feat.adx(high, low, close, timeperiod=10)

        long_setup = (rsi_val < 30) & (volume > vol_sma * 0.7) & (adx_val < 20)
        short_setup = (rsi_val > 70) & (volume > vol_sma * 0.7) & (adx_val < 20)
        exit_setup = self.op.crossed_above(rsi_val, 50) | self.op.crossed_below(rsi_val, 50) | (adx_val > 25)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

