"""
name:    VnLargeRsVnIndexFlatten
summary: RelativeStrengthTrend baseline plus a market-wide crash guard that
         flattens all positions whenever VN30 has turned down over the last 20
         sessions. The 12/36 EMA trend and residual-momentum blocks are
         untouched so re-entry after a crash stays fast.
idea:    Firm-specific relative strength is edge, but a broad 2022-style index
         downturn drags every long position and the full-sample Sharpe. A
         dedicated index guard flattens during VN30 downtrends, protecting the
         compounding base, then the unchanged trend/residual blocks re-enter
         quickly on the recovery.
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

        index_guard = vn30_return < 0

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