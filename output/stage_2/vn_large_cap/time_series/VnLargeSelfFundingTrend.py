"""
name:    VnLargeSelfFundingTrend
summary: Long large caps with positive annual operating cash flow while the
         financing line runs negative, holding price above the 10/30 EMA trend.
idea:    A self-funding large cap generates cash internally and repays or avoids
         new external financing. Combining positive CFO with a net financing
         outflow isolates businesses that do not depend on new debt or equity to
         keep running, and the 10/30 EMA trend determines timing while cash
         generation stays intact.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        financing_flow = self.data.fun_cf_net_cash_inflows_outflows_from_financing_activities_annual

        ema_fast = self.feat.ema(close, timeperiod=10)
        ema_slow = self.feat.ema(close, timeperiod=30)

        fundamentals_known = self.op.notna(operating_cash_flow) & self.op.notna(financing_flow)

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (financing_flow < 0)
            & (close > ema_slow)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (operating_cash_flow < 0) | (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
