
"""
name:    MFMomStd_60min
summary: Momentum MF: MFMom(7) — 60min
thesis:  multifactor | 60min
idea:    Multi-layer momentum
"""
class CustomStrategy(SimpleAlgorithm):

    rsi_window = 7
    roc_window = 8
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
        volume = self.data.pv_volume
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        daily_range = high - low
        avg_range = self.feat.sma(daily_range, timeperiod=self.range_window)
        hh = self.feat.rolling_max(high, window=self.chandelier_window)
        ll = self.feat.rolling_min(low, window=self.chandelier_window)
        trailing_long_exit = close < (hh - avg_range * self.chandelier_mult)
        trailing_short_exit = close > (ll + avg_range * self.chandelier_mult)

        roc = self.feat.roc(close, timeperiod=self.roc_window)
        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        adx = self.feat.adx(high, low, close, timeperiod=self.adx_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.rsi_window)

        morning_momentum = (roc > 0) & (rsi > 50) & (rsi < 65)
        volume_confirm = volume > vol_sma

        core_long = morning_momentum
        core_short = (roc < 0) & (rsi < 50) & (rsi > 35)

        strong_long = core_long & volume_confirm & (adx > 22) & (return_roll > 0)
        weak_long = core_long & (adx > 18) & (return_roll > 0)
        strong_short = core_short & volume_confirm & (adx > 22) & (return_roll < 0)
        weak_short = core_short & (adx > 18) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(rsi, 50) | self.op.crossed_above(rsi, 50)) | self.op.crossed_below(abs(return_roll), self.return_threshold) | trailing_long_exit | trailing_short_exit
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
