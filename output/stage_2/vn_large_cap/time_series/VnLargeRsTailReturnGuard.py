"""
name:    VnLargeRsTailReturnGuard
summary: RelativeStrengthTrend baseline plus a tail-risk guard that flattens all
         positions when the VN30 index is in an extreme downside drawdown (its
         20-day z-score drops below -1.5). The 12/36 EMA trend and
         residual-momentum blocks are unchanged so re-entry stays fast.
idea:    A broad-market crash, not firm momentum loss, erases yearly returns and
         inflates full-sample volatility. A tail guard activates only in extreme
         index drawdowns (like 2022), cutting compounding-base erosion with
         minimal interference in normal regimes. The untouched residual/trend
         blocks re-enter promptly once the index recovers.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)

        stock_return = self.op.fillna(self.op.pct_change(close, periods=20), value=0)
        vn30_return = self.op.fillna(self.op.pct_change(vn30_close, periods=20), value=0)
        relative_strength = stock_return - vn30_return

        vn30_zscore = self.feat.rolling_zscore(vn30_close, window=20)
        index_guard = vn30_zscore < -1.5

        base_entry = (
            (relative_strength > 0)
            & (close > ema_slow)
            & (~index_guard)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (relative_strength < 0) | (close < ema_slow) | index_guard

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)