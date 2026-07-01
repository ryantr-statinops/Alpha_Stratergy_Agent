
"""
name:    BODonFast_5min
summary: Donchian: Donchian(8) — 5min
thesis:  breakout | 5min
idea:    Donchian channel breakout
"""
class CustomStrategy(SimpleAlgorithm):

    d_window = 8

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        hh = self.feat.rolling_max(high, window=self.d_window)
        ll = self.feat.rolling_min(low, window=self.d_window)

        long_setup = close > hh
        short_setup = close < ll
        exit_setup = self.op.crossed_below(close, hh) | self.op.crossed_above(close, ll)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
