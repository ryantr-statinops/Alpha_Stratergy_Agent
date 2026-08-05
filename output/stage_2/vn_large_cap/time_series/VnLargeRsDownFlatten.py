"""
name:    VnLargeRsDownFlatten
summary: RelativeStrengthTrend baseline plus a per-stock crash guard that
         flattens all positions whenever the stock's own 20-day return drops
         below -10%. The 12/36 EMA trend and price-momentum blocks are
         untouched so re-entry after a crash stays fast.
idea:    Firm price momentum is the edge block; a broad 2022-style crash shows up
         as sharp per-stock drawdowns before the slow trend rolls over. A 20-day
         downside guard flattens fast on that crash, protecting the compounding
         base, while the unchanged momentum/trend blocks re-enter on recovery.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)

        stock_return = self.op.fillna(self.op.pct_change(close, periods=20), value=0)
        crash_guard = stock_return < -0.10

        base_entry = (
            (stock_return > 0)
            & (close > ema_slow)
            & (~crash_guard)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (stock_return < 0) | (close < ema_slow) | crash_guard

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)