
"""
name:    BORngStd_60min
summary: Range Exp: Range(1.5x) — 60min
thesis:  breakout | 60min
idea:    Range expansion breakout
"""
class CustomStrategy(SimpleAlgorithm):

    range_window = 8
    vol_window = 14
    range_mult = 1.5

    return_window = 3
    return_threshold = 0.0001
    position_close_after_n_candles = 6
    chandelier_window = 3
    chandelier_mult = 3.0
    range_window = 3
    cooldown_period = 1
    position_close_ranges = ['04:30-06:00']
    adx_window = 7
    adx_entry_threshold = 16
    adx_exit_threshold = 10

    def __algorithm__(self):
        close = self.data.pv_close
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

        daily_range = high - low
        avg_range = self.feat.sma(daily_range, timeperiod=self.range_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        range_expansion = daily_range > avg_range * self.range_mult
        vol_confirmation = volume > vol_sma

        long_setup = ((range_expansion & vol_confirmation & (close > (high + low) / 2)) & (return_roll > 0)) & (adx > self.adx_entry_threshold)
        short_setup = ((range_expansion & vol_confirmation & (close < (high + low) / 2)) & (return_roll < 0)) & (adx > self.adx_entry_threshold)
        exit_setup = (((daily_range < avg_range) | (volume < vol_sma)) | self.op.crossed_below(abs(return_roll), self.return_threshold)) | self.op.crossed_below(adx, self.adx_exit_threshold) | trailing_long_exit | trailing_short_exit
        recent_exit = self.feat.rolling_max(exit_setup, window=self.cooldown_period)
        long_setup = long_setup & (recent_exit < 1)
        short_setup = short_setup & (recent_exit < 1)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=vol_scale)
        self.set_positions(short_setup, position=-vol_scale)
