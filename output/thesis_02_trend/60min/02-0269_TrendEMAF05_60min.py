
"""
name:    TrendEMAF05_60min
summary: EMA Trend: EMA(fast/2) + ADX — 60min
thesis:  trend | 60min
idea:    Half EMA + ADX
"""
class CustomStrategy(SimpleAlgorithm):

    fast_window = 4
    adx_window = 7

    return_window = 3
    return_threshold = 0.0001
    position_close_after_n_candles = 6

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        ema = self.feat.ema(close, timeperiod=self.fast_window)
        adx = self.feat.adx(high, low, close, timeperiod=self.adx_window)

        above_ema = close > ema
        below_ema = close < ema

        strong_long = above_ema & (adx > 22) & (adx < 40) & (return_roll > 0)
        weak_long = above_ema & (adx > 18) & (adx < 40) & (return_roll > 0)
        strong_short = below_ema & (adx > 22) & (adx < 40) & (return_roll < 0)
        weak_short = below_ema & (adx > 18) & (adx < 40) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(close, ema) | self.op.crossed_above(close, ema)) | self.op.crossed_below(abs(return_roll), self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-1)
