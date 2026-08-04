"""
name:    VnLargeTrixMomentum
summary: Long large caps when TRIX crosses above zero with rising momentum.
idea:    TRIX is a triple-smoothed EMA that filters out noise非常适合
         large caps where whipsaw is costly. A TRIX crossing above zero
         with rising slope confirms sustained upward momentum.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close

        ema_slow = self.feat.ema(close, timeperiod=30)
        trix_val = self.feat.trix(close, timeperiod=14)
        trix_rising = self.op.fillna(self.op.pct_change(trix_val, periods=3), 0)

        known = (
            self.op.notna(ema_slow)
            & self.op.notna(trix_val)
            & (close > 0)
        )

        base_long = known & (trix_val > 0) & (trix_rising > 0) & (close > ema_slow)
        exit_setup = known & ((trix_val < 0) | (close < ema_slow))

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_long, position=1)
