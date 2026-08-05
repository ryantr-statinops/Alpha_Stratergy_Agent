"""
name:    VnLargeRsVnIndexTrendGuard
summary: RelativeStrengthTrend baseline plus a regime guard that flattens all
         positions while the VN30 index trades below its own 20-day EMA. The
         12/36 EMA trend and residual-momentum blocks are unchanged so recovery
         re-entry stays fast.
idea:    Relative strength isolates firm momentum, but in a broad bear regime
         (index below its trend) beta drags every long. An index regime guard
         flattens only in that window to protect capital and un-inflate
         full-sample volatility, while the untouched residual/trend blocks
         re-enter on the rebound.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)
        vn30_ema = self.feat.ema(vn30_close, timeperiod=20)

        stock_return = self.op.fillna(self.op.pct_change(close, periods=20), value=0)
        vn30_return = self.op.fillna(self.op.pct_change(vn30_close, periods=20), value=0)
        relative_strength = stock_return - vn30_return

        index_guard = vn30_close < vn30_ema

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