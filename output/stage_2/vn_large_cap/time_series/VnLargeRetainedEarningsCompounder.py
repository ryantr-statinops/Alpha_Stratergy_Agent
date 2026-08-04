"""
name:    VnLargeRetainedEarningsCompounder
summary: Long large caps growing retained earnings with positive profit, held
         above a slow 30/90 EMA trend for low turnover.
idea:    Compounding at large caps shows up as a growing stock of undistributed
         earnings backed by positive net profit. This is a slow, persistent
         quality state; the 30/90 EMA hold keeps turnover low and only exits when
         retained earnings stop growing, profit turns negative, or the long-term
         trend breaks.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual
        retained_earnings = self.data.fun_bs_undistributed_earnings_annual

        ema_fast = self.feat.ema(close, timeperiod=30)
        ema_slow = self.feat.ema(close, timeperiod=90)

        retained_growth = self.op.pct_change(retained_earnings, periods=1)

        fundamentals_known = (
            self.op.notna(net_profit)
            & self.op.notna(retained_earnings)
            & self.op.notna(retained_growth)
        )

        base_entry = (
            fundamentals_known
            & (net_profit > 0)
            & (retained_earnings > 0)
            & (retained_growth > 0)
            & (close > ema_slow)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (net_profit < 0) | (fundamentals_known & (retained_growth < 0)) | (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
