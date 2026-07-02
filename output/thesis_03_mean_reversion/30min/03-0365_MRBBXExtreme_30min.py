
"""
name:    MRBBXExtreme_30min
summary: BBands Rev: BBands(4STD) — 30min
thesis:  mean_reversion | 30min
idea:    Bollinger Band reversion
"""
class CustomStrategy(SimpleAlgorithm):

    bbands_window = 26
    nbdev = 4

    return_window = 5
    return_threshold = 0.0002
    position_close_after_n_candles = 12
    chandelier_window = 4
    chandelier_mult = 2.5
    range_window = 5
    cooldown_period = 2
    position_close_ranges = ['04:30-06:00']
    adx_window = 10
    adx_entry_threshold = 18
    adx_exit_threshold = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=10)
        daily_range = high - low
        avg_range = self.feat.sma(daily_range, timeperiod=self.range_window)
        hh = self.feat.rolling_max(high, window=self.chandelier_window)
        ll = self.feat.rolling_min(low, window=self.chandelier_window)
        trailing_long_exit = close < (hh - avg_range * self.chandelier_mult)
        trailing_short_exit = close > (ll + avg_range * self.chandelier_mult)
        vol_scale = self.op.clip(avg_range / daily_range, 0.3, 1.0)

        upper, mid_band, lower = self.feat.bbands(
            close, timeperiod=self.bbands_window, nbdevup=self.nbdev, nbdevdn=self.nbdev
        )

        long_setup = ((close < lower) & (return_roll > 0)) & (adx > self.adx_entry_threshold)
        short_setup = ((close > upper) & (return_roll < 0)) & (adx > self.adx_entry_threshold)
        exit_setup = ((self.op.crossed_above(close, mid_band) | self.op.crossed_below(close, mid_band)) | self.op.crossed_below(abs(return_roll), self.return_threshold)) | self.op.crossed_below(adx, self.adx_exit_threshold) | trailing_long_exit | trailing_short_exit
        recent_exit = self.feat.rolling_max(exit_setup, window=self.cooldown_period)
        long_setup = long_setup & (recent_exit < 1)
        short_setup = short_setup & (recent_exit < 1)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=vol_scale)
        self.set_positions(short_setup, position=-vol_scale)
