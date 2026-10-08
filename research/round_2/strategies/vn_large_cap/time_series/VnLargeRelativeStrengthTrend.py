"""
name:    VnLargeRelativeStrengthTrend
summary: Long large caps whose 20-day return exceeds the VN30 benchmark
         return, in an uptrend.
idea:    Relative strength against the index removes the common market
         component and isolates firm-specific momentum. A stock consistently
         outperforming VN30 signals benchmark-residual momentum that is less
         exposed to broad market beta. Combining this with an absolute uptrend
         ensures both firm-specific and price-momentum alignment.
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

        base_entry = (
            (relative_strength > 0)
            & (close > ema_slow)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (relative_strength < 0) | (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)