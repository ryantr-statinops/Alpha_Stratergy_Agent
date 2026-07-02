
"""
name:    ISMOpnVSlow_5min
summary: Open Drive: OpenDrive(21) — 5min
thesis:  intraday_session | 5min
idea:    Morning session momentum
"""
class CustomStrategy(SimpleAlgorithm):

    rsi_window = 21

    return_window = 3
    return_threshold = 0.0001
    position_close_after_n_candles = 72
    chandelier_window = 6
    chandelier_mult = 2.0
    range_window = 7
    cooldown_period = 3
    position_close_ranges = ['04:30-06:00']
    position_open_ranges = ['02:00-04:30', '06:00-07:45']
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
        daily_range = high - low
        avg_range = self.feat.sma(daily_range, timeperiod=self.range_window)
        hh = self.feat.rolling_max(high, window=self.chandelier_window)
        ll = self.feat.rolling_min(low, window=self.chandelier_window)
        trailing_long_exit = close < (hh - avg_range * self.chandelier_mult)
        trailing_short_exit = close > (ll + avg_range * self.chandelier_mult)
        vol_scale = self.op.clip(avg_range / daily_range, 0.3, 1.0)

        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        open_range = (close - open_price) / open_price * 100
        candle_range = high - low
        avg_range = self.feat.sma(candle_range, timeperiod=self.rsi_window)

        expanding_range = candle_range > avg_range
        bullish_drive = (open_range > 0.3) & expanding_range & (rsi > 50) & (rsi < 70)
        bearish_drive = (open_range < -0.3) & expanding_range & (rsi < 50) & (rsi > 30)

        long_setup = ((bullish_drive) & (return_roll > 0)) & (adx > self.adx_entry_threshold)
        short_setup = ((bearish_drive) & (return_roll < 0)) & (adx > self.adx_entry_threshold)
        exit_setup = ((self.op.crossed_below(rsi, 50) | self.op.crossed_above(rsi, 50)) | self.op.crossed_below(abs(return_roll), self.return_threshold)) | self.op.crossed_below(adx, self.adx_exit_threshold) | trailing_long_exit | trailing_short_exit
        recent_exit = self.feat.rolling_max(exit_setup, window=self.cooldown_period)
        long_setup = long_setup & (recent_exit < 1)
        short_setup = short_setup & (recent_exit < 1)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=vol_scale)
        self.set_positions(short_setup, position=-vol_scale)
