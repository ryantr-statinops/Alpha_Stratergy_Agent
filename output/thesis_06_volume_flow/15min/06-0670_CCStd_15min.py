
"""
name:    CCStd_15min
summary: Cascade Catcher: Standard cascade: OI-1%/vol-2x/price-0.5% — 15min
thesis:  volume_flow | 15min
idea:    Margin call cascade — OI drop + volume spike + price fall
"""
class CustomStrategy(SimpleAlgorithm):

    oi_window = 34
    vol_window = 20
    oi_drop_threshold = 0.01
    vol_spike_mult = 2.0
    price_fall_threshold = 0.005

    return_window = 5
    return_threshold = 0.0002
    position_close_after_n_candles = 24
    chandelier_window = 5
    chandelier_mult = 2.0
    range_window = 5
    cooldown_period = 2
    position_close_ranges = ['04:30-06:00']
    adx_window = 10
    adx_entry_threshold = 22
    adx_exit_threshold = 15

    def __algorithm__(self):
        close = self.data.pv_close
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d
        oi = self.data.fut_open_interest_vn30f1m_1d
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

        oi_sma = self.feat.sma(oi, timeperiod=self.oi_window)
        vol_sma = self.feat.sma(matched_vol, timeperiod=self.vol_window)

        oi_change = self.op.fillna(self.op.pct_change(oi, periods=1), value=0)
        oi_drop = oi_change < -self.oi_drop_threshold
        vol_spike = matched_vol > vol_sma * self.vol_spike_mult
        price_fall = self.op.pct_change(close, periods=1) < -self.price_fall_threshold

        cascade = oi_drop & vol_spike & price_fall

        vol_collapse = matched_vol < vol_sma * 0.5
        price_stable = self.op.abs(self.op.pct_change(close, periods=1)) < self.price_fall_threshold * 0.2
        exhaustion = oi_drop & vol_collapse & price_stable

        long_setup = ((exhaustion) & (return_roll > 0)) & (adx > self.adx_entry_threshold)
        short_setup = ((cascade) & (return_roll < 0)) & (adx > self.adx_entry_threshold)

        exit_setup = ((self.op.crossed_below(close, oi_sma) | self.op.crossed_above(close, oi_sma)) | self.op.crossed_below(abs(return_roll), self.return_threshold)) | self.op.crossed_below(adx, self.adx_exit_threshold) | trailing_long_exit | trailing_short_exit
        recent_exit = self.feat.rolling_max(exit_setup, window=self.cooldown_period)
        long_setup = long_setup & (recent_exit < 1)
        short_setup = short_setup & (recent_exit < 1)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
