
"""
name:    ISMOpnUltra_5min
summary: Open Drive: OpenDrive(3) — 5min
thesis:  intraday_session | 5min
idea:    Morning session momentum
"""
class CustomStrategy(SimpleAlgorithm):

    rsi_window = 3

    return_window = 3
    return_threshold = 0.0001
    position_close_after_n_candles = 72
    position_open_ranges = ['02:00-04:30', '06:00-07:45']
    position_close_ranges = ['04:20-04:30', '07:30-07:45']
    adx_window = 7
    adx_entry_threshold = 22
    adx_exit_threshold = 15

    def __algorithm__(self):
        close = self.data.pv_close
        open_price = self.data.pv_open
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=7)

        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        open_range = (close - open_price) / open_price * 100
        candle_range = high - low
        avg_range = self.feat.sma(candle_range, timeperiod=self.rsi_window)

        expanding_range = candle_range > avg_range
        bullish_drive = (open_range > 0.3) & expanding_range & (rsi > 50) & (rsi < 70)
        bearish_drive = (open_range < -0.3) & expanding_range & (rsi < 50) & (rsi > 30)

        long_setup = ((bullish_drive) & (return_roll > 0)) & (adx > self.adx_entry_threshold)
        short_setup = ((bearish_drive) & (return_roll < 0)) & (adx > self.adx_entry_threshold)
        exit_setup = ((self.op.crossed_below(rsi, 50) | self.op.crossed_above(rsi, 50)) | self.op.crossed_below(abs(return_roll), self.return_threshold)) | self.op.crossed_below(adx, self.adx_exit_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
