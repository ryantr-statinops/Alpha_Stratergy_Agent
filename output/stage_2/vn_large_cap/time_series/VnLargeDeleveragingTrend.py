"""
name:    VnLargeDeleveragingTrend
summary: Long large caps whose total loans relative to total assets are falling
         while operating cash flow stays positive, in a 12/36 EMA uptrend.
idea:    A large cap that keeps generating cash and pays down borrowings improves
         its balance-sheet resilience quarter by quarter. The loans-to-assets
         ratio is tracked as a slow fundamental event: entry requires the ratio
         to shrink with positive CFO and price above the 12/36 EMA trend, exit on
         a rising leverage ratio, negative cash flow, or a trend break.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        short_term_loans = self.data.fun_bs_short_term_loans_annual
        long_term_loans = self.data.fun_bs_long_term_loans_annual
        total_assets = self.data.fun_bs_total_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)

        total_loans = short_term_loans + long_term_loans
        leverage = total_loans / total_assets
        leverage_known = (
            self.op.notna(total_loans)
            & self.op.notna(total_assets)
            & (total_assets > 0)
            & self.op.notna(leverage)
        )
        leverage_change = self.op.pct_change(leverage, periods=1)

        deleveraging_known = leverage_known & self.op.notna(leverage_change)

        base_entry = (
            deleveraging_known
            & (operating_cash_flow > 0)
            & (leverage_change < 0)
            & (close > ema_slow)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (
            (operating_cash_flow < 0)
            | (deleveraging_known & (leverage_change > 0))
            | (close < ema_slow)
        )

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
