
"""
name:    ISMLunUltra_15min
summary: Lunch Rev: LunchRev(3) — 15min
thesis:  intraday_session | 15min
idea:    Lunch mean reversion
"""
class CustomStrategy(SimpleAlgorithm):

    rsi_window = 3

    return_window = 5
    return_threshold = 0.0002
    position_close_after_n_candles = 24
    position_open_ranges = ['02:00-04:30', '06:00-07:45']
    position_close_ranges = ['04:20-04:30', '07:30-07:45']
    adx_window = 10

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        open_price = self.data.pv_open
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=10)

        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        mid_price = (high + low) / 2
        extreme_band = (high - low) * 0.8

        long_setup = (((rsi < 30) & (close < (mid_price - extreme_band))) & (return_roll > 0)) & (adx > 22)
        short_setup = (((rsi > 70) & (close > (mid_price + extreme_band))) & (return_roll < 0)) & (adx > 22)
        exit_setup = ((self.op.crossed_above(rsi, 50) | self.op.crossed_below(rsi, 50)) | (abs(return_roll) < self.return_threshold)) | (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
