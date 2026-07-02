
"""
name:    BORngAggr_30min
summary: Range Exp: Range(2.5x) — 30min
thesis:  breakout | 30min
idea:    Range expansion breakout
"""
class CustomStrategy(SimpleAlgorithm):

    range_window = 13
    vol_window = 20
    range_mult = 2.5

    return_window = 5
    return_threshold = 0.0002
    position_close_after_n_candles = 12
    adx_window = 10
    adx_entry_threshold = 18
    adx_exit_threshold = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=10)

        daily_range = high - low
        avg_range = self.feat.sma(daily_range, timeperiod=self.range_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        range_expansion = daily_range > avg_range * self.range_mult
        vol_confirmation = volume > vol_sma

        long_setup = ((range_expansion & vol_confirmation & (close > (high + low) / 2)) & (return_roll > 0)) & (adx > self.adx_entry_threshold)
        short_setup = ((range_expansion & vol_confirmation & (close < (high + low) / 2)) & (return_roll < 0)) & (adx > self.adx_entry_threshold)
        exit_setup = (((daily_range < avg_range) | (volume < vol_sma)) | self.op.crossed_below(abs(return_roll), self.return_threshold)) | self.op.crossed_below(adx, self.adx_exit_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
