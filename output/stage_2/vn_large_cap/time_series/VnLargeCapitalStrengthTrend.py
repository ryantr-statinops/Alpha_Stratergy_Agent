"""
name:    VnLargeCapitalStrengthTrend
summary: Long large caps with a strong equity-to-assets balance sheet in an
         8/24 EMA uptrend.
idea:    A high equity-to-assets ratio means the large cap can absorb
         downturns without distress. Requiring a strong capital base and an
         intact 8/24 EMA uptrend buys defensive quality only when the market is
         confirming it, exiting if the balance sheet or the trend deteriorates.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        equity = self.data.fun_bs_owners_equity_annual
        total_assets = self.data.fun_bs_total_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)

        capital_ratio = equity / total_assets
        fundamentals_known = (
            self.op.notna(equity)
            & self.op.notna(total_assets)
            & (total_assets > 0)
            & self.op.notna(capital_ratio)
        )

        base_entry = fundamentals_known & (capital_ratio > 0.3) & (ema_fast > ema_slow)
        strong_entry = base_entry & (close > ema_slow)
        exit_setup = (capital_ratio < 0.2) | (ema_fast < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
