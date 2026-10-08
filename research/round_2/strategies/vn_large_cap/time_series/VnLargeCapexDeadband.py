"""
name:    VnLargeCapexDeadband
summary: Long large caps whose capex is fully funded by operating cash flow, with
         price above a dead-band on the 36 EMA of the 12/36 trend.
idea:    A dead-band (full-size requires price 2% above the 36 EMA) stops a
         one-day close hovering on the line from re-entering or scaling out of
         the capex-discipline hold. This noise filter reduces churn around the
         2022 declines while preserving the internal-funding gate; exit stays on
         negative cash generation, capex outrunning cash flow, or the trend break.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)

        fundamentals_known = self.op.notna(operating_cash_flow) & self.op.notna(capex)

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (capex < operating_cash_flow)
            & (close > ema_slow)
        )
        strong_entry = base_entry & (ema_fast > ema_slow) & (close > ema_slow * 1.02)
        exit_setup = (operating_cash_flow < 0) | (capex > operating_cash_flow) | (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
