"""
name:    T03-B_b26_m30
summary: DCPeriod Adaptive Sizing
idea:    Use Dominant Cycle Period to scale position sizes dynamically; larger cycles get larger positions.
"""
class CustomStrategy(SimpleAlgorithm):
    base_window = 26


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        cycle_period = self.feat.dcperiod(close)
        trend = self.feat.ht_trendline(close)
        adx_val = self.feat.adx(high, low, close, timeperiod=self.base_window)

        roc_val = self.feat.roc(close, timeperiod=5)

        long_setup = (close > trend) & (roc_val > 0) & (adx_val > 22)
        short_setup = (close < trend) & (roc_val < 0) & (adx_val > 22)
        exit_setup = self.op.crossed_below(close, trend) | self.op.crossed_above(close, trend) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

