
"""
name:    VFOBVFast_30min
summary: OBV Flow: OBV(13) — 30min
thesis:  volume_flow | 30min
idea:    OBV cumulative flow
"""
class CustomStrategy(SimpleAlgorithm):

    obv_window = 13

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
        volume = self.data.pv_volume
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

        obv = self.feat.obv(close, volume)
        obv_sma = self.feat.sma(obv, timeperiod=self.obv_window)
        close_sma = self.feat.sma(close, timeperiod=self.obv_window)

        long_setup = (((obv > obv_sma) & (close > close_sma)) & (return_roll > 0)) & (adx > self.adx_entry_threshold)
        short_setup = (((obv < obv_sma) & (close < close_sma)) & (return_roll < 0)) & (adx > self.adx_entry_threshold)
        exit_setup = ((self.op.crossed_below(obv, obv_sma) | self.op.crossed_above(obv, obv_sma)) | self.op.crossed_below(abs(return_roll), self.return_threshold)) | self.op.crossed_below(adx, self.adx_exit_threshold) | trailing_long_exit | trailing_short_exit
        recent_exit = self.feat.rolling_max(exit_setup, window=self.cooldown_period)
        long_setup = long_setup & (recent_exit < 1)
        short_setup = short_setup & (recent_exit < 1)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=vol_scale)
        self.set_positions(short_setup, position=-vol_scale)
