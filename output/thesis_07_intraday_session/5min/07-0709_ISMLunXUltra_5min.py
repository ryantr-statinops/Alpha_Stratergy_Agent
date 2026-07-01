
"""
name:    ISMLunXUltra_5min
summary: Lunch Rev: LunchRev(3) — 5min
thesis:  intraday_session | 5min
idea:    Lunch mean reversion
"""
class CustomStrategy(SimpleAlgorithm):

    rsi_window = 3

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        open_price = self.data.pv_open

        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        mid_price = (high + low) / 2
        extreme_band = (high - low) * 0.8

        long_setup = (rsi < 30) & (close < (mid_price - extreme_band))
        short_setup = (rsi > 70) & (close > (mid_price + extreme_band))
        exit_setup = self.op.crossed_above(rsi, 50) | self.op.crossed_below(rsi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
