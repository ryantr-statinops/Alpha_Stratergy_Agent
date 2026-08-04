"""
name:    VnLargeCapex1442
summary: Long large caps whose capex is fully funded by operating cash flow, with
         price above the 14/42 EMA trend.
idea:    Slowing the capex-discipline timing from 12/36 to 14/42 keeps the same
         internal-funding quality gate but trades less often. Fewer flips around
         the 2022 downtrend should cut the whipsaw that dragged the baseline's
         train-period drawdown, while still exiting on negative cash generation,
         capex outrunning cash flow, or the 42 EMA break.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=14)
        ema_slow = self.feat.ema(close, timeperiod=42)

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
