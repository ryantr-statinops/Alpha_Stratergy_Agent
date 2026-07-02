
"""
name:    TrendEMAFast_60min
summary: EMA Trend: EMA(8) + ADX — 60min
thesis:  trend | 60min
idea:    EMA trend with ADX strength
"""
class CustomStrategy(SimpleAlgorithm):

    fast_window = 8
    adx_window = 7

    return_window = 3
    return_threshold = 0.0001
    position_close_after_n_candles = 6
    chandelier_window = 3
    chandelier_mult = 3.0
    range_window = 3
    cooldown_period = 1
    position_close_ranges = ['04:30-06:00']

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        daily_range = high - low
        avg_range = self.feat.sma(daily_range, timeperiod=self.range_window)
        hh = self.feat.rolling_max(high, window=self.chandelier_window)
        ll = self.feat.rolling_min(low, window=self.chandelier_window)
        trailing_long_exit = close < (hh - avg_range * self.chandelier_mult)
        trailing_short_exit = close > (ll + avg_range * self.chandelier_mult)

        ema = self.feat.ema(close, timeperiod=self.fast_window)
        adx = self.feat.adx(high, low, close, timeperiod=self.adx_window)

        above_ema = close > ema
        below_ema = close < ema

        strong_long = above_ema & (adx > 22) & (adx < 40) & (return_roll > 0)
        weak_long = above_ema & (adx > 18) & (adx < 40) & (return_roll > 0)
        strong_short = below_ema & (adx > 22) & (adx < 40) & (return_roll < 0)
        weak_short = below_ema & (adx > 18) & (adx < 40) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(close, ema) | self.op.crossed_above(close, ema)) | self.op.crossed_below(abs(return_roll), self.return_threshold) | trailing_long_exit | trailing_short_exit
        recent_exit = self.feat.rolling_max(exit_setup, window=self.cooldown_period)
        strong_long = strong_long & (recent_exit < 1)
        weak_long = weak_long & (recent_exit < 1)
        strong_short = strong_short & (recent_exit < 1)
        weak_short = weak_short & (recent_exit < 1)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-1)
