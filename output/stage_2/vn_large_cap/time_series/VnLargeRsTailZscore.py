"""
name:    VnLargeRsTailZscore
summary: RelativeStrengthTrend baseline plus a per-stock tail guard that flattens
         all positions when the stock's own 20-day z-score drops below -1.5
         (extreme drawdown). Trend and momentum blocks untouched so re-entry
         after the crash stays fast.
idea:    A broad crash produces extreme per-stock drawdowns (z-score well below
         zero) before the slow trend exits. A tail guard flatten only in those
         deep losses, cutting compounding-base erosion with minimal interference
         in normal regimes, while the unchanged momentum/trend blocks re-enter
         on recovery.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)

        stock_return = self.op.fillna(self.op.pct_change(close, periods=20), value=0)

        close_z = self.feat.rolling_zscore(close, window=20)
        tail_guard = close_z < -1.5

        base_entry = (
            (stock_return > 0)
            & (close > ema_slow)
            & (~tail_guard)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (stock_return < 0) | (close < ema_slow) | tail_guard

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)