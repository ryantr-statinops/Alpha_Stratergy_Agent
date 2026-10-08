"""
name:    VnLargeProbeVn30Down
summary: Purely diagnostic probe. Goes long whenever the VN30 index 20-day
         return is negative, flat otherwise. Used to confirm whether the
         pv_vn30_close field actually varies over time on the platform. If the
         field is constant, position is always 0 and metrics collapse to ~0.
idea:    Diagnostic only. A constant index series makes pct_change == 0, so the
         long condition vn30_return < 0 is never true and the strategy stays
         flat. A nonzero, meaningful Equity curve proves the field varies.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        vn30_close = self.data.pv_vn30_close
        vn30_return = self.op.fillna(self.op.pct_change(vn30_close, periods=20), value=0)
        long_setup = vn30_return < 0
        self.set_positions(long_setup, position=1)