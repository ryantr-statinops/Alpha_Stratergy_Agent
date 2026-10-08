"""
name:    VnLargeMfiDivergence
summary: Long large caps with healthy MFI confirming price momentum.
idea:    Money Flow Index between 50-80 with rising slope confirms that
         price gains are backed by real money flow. Combined with an EMA
         uptrend, this captures the sweet spot where momentum is strong
         but not yet overbought.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        ema_slow = self.feat.ema(close, timeperiod=30)
        mfi_val = self.feat.mfi(high, low, close, volume, timeperiod=14)
        mfi_rising = self.op.fillna(self.op.pct_change(mfi_val, periods=3), 0)

        known = (
            self.op.notna(ema_slow)
            & self.op.notna(mfi_val)
            & (close > 0)
        )

        base_long = known & (mfi_val > 50) & (mfi_val < 80) & (close > ema_slow)
        strong_long = base_long & (mfi_rising > 0)
        exit_setup = known & ((mfi_val < 40) | (close < ema_slow))

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_long, position=0.5)
        self.set_positions(strong_long, position=1)
