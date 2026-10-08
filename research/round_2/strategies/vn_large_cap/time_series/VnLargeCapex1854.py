"""
name:    VnLargeCapex1854
summary: Long large caps whose capex is fully funded by operating cash flow, with
         price above the 18/54 EMA trend.
idea:    Moving the capex-discipline timing to the 18/54 stable-hold family keeps
         the internal-funding quality gate and drops trade frequency further. The
         slower 54 EMA smooths the 2022 regime so the position holds only while
         the broad downtrend is clearly absent; exit stays on negative cash
         generation, capex outrunning cash flow, or the 54 EMA break.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=18)
        ema_slow = self.feat.ema(close, timeperiod=54)

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
