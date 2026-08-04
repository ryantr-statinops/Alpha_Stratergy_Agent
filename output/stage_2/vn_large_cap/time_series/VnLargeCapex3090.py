"""
name:    VnLargeCapex3090
summary: Long large caps whose capex is fully funded by operating cash flow, with
         price above the 30/90 EMA trend.
idea:    The 30/90 stable-hold family is the slowest timing tested for the capex-
         discipline gate. This variant maximally suppresses trend churn so the
         position is governed almost entirely by the internal-funding quality
         gate; the 90 EMA only filters the clearest broad downtrends, which
         targets the deepest part of the 2022 drawdown. Exit remains negative
         cash generation, capex outrunning cash flow, or the 90 EMA break.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=30)
        ema_slow = self.feat.ema(close, timeperiod=90)

        fundamentals_known = self.op.notna(operating_cash_flow) & self.op.notna(capex)

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (capex < operating_cash_flow)
            & (close > ema_slow)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (operating_cash_flow < 0) | (capex > operating_cash_flow) | (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
