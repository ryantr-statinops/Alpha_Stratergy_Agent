"""
name:    VnLargeCashInterestCoverage
summary: Long large caps whose annual operating cash flow covers interest paid by
         more than three times, in a 12/36 EMA uptrend.
idea:    Interest coverage from operating cash flow, not net profit, is the truest
         measure of debt service capacity for a large cap. A CFO-to-interest-paid
         ratio above three flags a low credit risk business, and the 12/36 EMA
         trend picks the timing; exit when coverage collapses toward one or the
         trend breaks.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        interest_paid = self.data.fun_cf_interest_paid_annual

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)

        coverage = operating_cash_flow / interest_paid
        coverage_known = (
            self.op.notna(operating_cash_flow)
            & self.op.notna(interest_paid)
            & (interest_paid > 0)
            & self.op.notna(coverage)
        )

        base_entry = coverage_known & (coverage > 3.0) & (close > ema_slow)
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = coverage_known & (coverage < 1.0) | (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
