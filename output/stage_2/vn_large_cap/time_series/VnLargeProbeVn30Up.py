"""
name:    VnLargeProbeVn30Up
summary: Purely diagnostic probe. Goes long whenever the VN30 index 20-day
         return is positive, flat otherwise. If pv_vn30_close is a constant,
         pct_change == 0 so the condition 0 > 0 is never true and metrics stay
         ~0. Confirms (with ProbeVn30Down) whether the index field varies.
idea:    Diagnostic only. Inverse of ProbeVn30Down.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        vn30_close = self.data.pv_vn30_close
        vn30_return = self.op.fillna(self.op.pct_change(vn30_close, periods=20), value=0)
        long_setup = vn30_return > 0
        self.set_positions(long_setup, position=1)