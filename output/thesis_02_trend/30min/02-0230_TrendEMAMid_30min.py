
"""
name:    TrendEMAMid_30min
summary: EMA Trend: EMA(40) + ADX — 30min
thesis:  trend | 30min
idea:    EMA trend with ADX strength
"""
class CustomStrategy(SimpleAlgorithm):

    fast_window = 40
    adx_window = 14

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        ema = self.feat.ema(close, timeperiod=self.fast_window)
        adx = self.feat.adx(high, low, close, timeperiod=self.adx_window)

        long_setup = (close > ema) & (adx > 20) & (adx < 40)
        short_setup = (close < ema) & (adx > 20) & (adx < 40)
        exit_setup = self.op.crossed_below(close, ema) | self.op.crossed_above(close, ema)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
