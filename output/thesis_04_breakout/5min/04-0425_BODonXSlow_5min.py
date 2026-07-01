
"""
name:    BODonXSlow_5min
summary: Donchian: Donchian(28) — 5min
thesis:  breakout | 5min
idea:    Donchian channel breakout
"""
class CustomStrategy(SimpleAlgorithm):

    d_window = 28

    return_window = 3
    return_threshold = 0.0001
    position_close_after_n_candles = 72

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        hh = self.feat.rolling_max(high, window=self.d_window)
        ll = self.feat.rolling_min(low, window=self.d_window)

        long_setup = (close > hh) & (return_roll > 0)
        short_setup = (close < ll) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(close, hh) | self.op.crossed_above(close, ll)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
