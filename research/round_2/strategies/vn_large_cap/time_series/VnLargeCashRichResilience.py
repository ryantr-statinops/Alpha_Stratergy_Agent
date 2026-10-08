"""
name:    VnLargeCashRichResilience
summary: Long large caps whose cash and equivalents exceed 10% of total assets
         while price trades above the 8/24 EMA trend.
idea:    Large caps with a fortress balance sheet carry enough cash relative to
         total assets to absorb shocks and self-finance downturns. This filters
         names by balance-sheet resilience, then only buys the ones whose price
         is in an 8/24 EMA uptrend, exiting when the cash buffer thins out or the
         trend breaks.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        cash_and_equivalents = self.data.fun_bs_cash_and_cash_equivalents_annual
        total_assets = self.data.fun_bs_total_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)

        cash_ratio = cash_and_equivalents / total_assets
        ratio_known = (
            self.op.notna(cash_and_equivalents)
            & self.op.notna(total_assets)
            & (total_assets > 0)
            & self.op.notna(cash_ratio)
        )

        base_entry = ratio_known & (cash_ratio > 0.10) & (close > ema_slow)
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = ratio_known & (cash_ratio < 0.05) | (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
