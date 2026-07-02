
"""
name:    ISMGapVSlow_15min
summary: Gap Fill: GapFill(30) — 15min
thesis:  intraday_session | 15min
idea:    Intraday gap fill
"""
class CustomStrategy(SimpleAlgorithm):

    rsi_window = 30

    return_window = 5
    return_threshold = 0.0002
    position_close_after_n_candles = 24
    position_open_ranges = ['02:00-04:30', '06:00-07:45']
    position_close_ranges = ['04:20-04:30', '07:30-07:45']
    adx_window = 10
    adx_entry_threshold = 22
    adx_exit_threshold = 15

    def __algorithm__(self):
        close = self.data.pv_close
        open_price = self.data.pv_open
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=10)

        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        gap = (open_price / close - 1) * 100

        gap_up = gap > 0.3
        gap_down = gap < -0.3
        filling_down = gap_up & (close < open_price) & (rsi < 60)
        filling_up = gap_down & (close > open_price) & (rsi > 40)

        long_setup = ((filling_up) & (return_roll > 0)) & (adx > self.adx_entry_threshold)
        short_setup = ((filling_down) & (return_roll < 0)) & (adx > self.adx_entry_threshold)
        exit_setup = ((self.op.crossed_above(abs(gap), 0.1)) | self.op.crossed_below(abs(return_roll), self.return_threshold)) | self.op.crossed_below(adx, self.adx_exit_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
