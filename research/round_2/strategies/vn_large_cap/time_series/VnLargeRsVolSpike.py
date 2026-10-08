"""
name:    VnLargeRsVolSpike
summary: RelativeStrengthTrend baseline plus a per-stock volatility guard that
         flattens all positions when the stock's normalized ATR z-score spikes
         above 1.0 (crash = volatility expansion). Trend and momentum blocks
         untouched so re-entry after the crash stays fast.
idea:    The 2022 crash is a regime of exploding volatility. A normalized-ATR
         z-score spikes exactly in those regimes; flattening then protects the
         compounding base and un-inflates full-sample volatility. The unchanged
         momentum/trend blocks re-enter promptly once volatility normalizes.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)

        stock_return = self.op.fillna(self.op.pct_change(close, periods=20), value=0)

        natr = self.feat.natr(high, low, close, timeperiod=14)
        natr_z = self.feat.rolling_zscore(natr, window=20)
        vol_guard = natr_z > 1.0

        base_entry = (
            (stock_return > 0)
            & (close > ema_slow)
            & (~vol_guard)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (stock_return < 0) | (close < ema_slow) | vol_guard

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)