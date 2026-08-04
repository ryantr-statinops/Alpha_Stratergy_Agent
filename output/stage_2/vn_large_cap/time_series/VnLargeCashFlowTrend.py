"""
name:    VnLargeCashFlowTrend
summary: Long large caps with positive annual operating cash flow in an 8/24
         EMA uptrend.
idea:    Large caps are priced for earnings quality, and operating cash flow is
         the hardest number to dress up. Only holding names whose annual CFO is
         positive AND whose price is in an 8/24 EMA uptrend links business
         quality to the technical regime, exiting on either a trend break or
         deteriorating cash generation.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)

        fundamentals_known = self.op.notna(operating_cash_flow)

        base_entry = fundamentals_known & (operating_cash_flow > 0) & (close > ema_slow)
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (operating_cash_flow < 0) | (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
