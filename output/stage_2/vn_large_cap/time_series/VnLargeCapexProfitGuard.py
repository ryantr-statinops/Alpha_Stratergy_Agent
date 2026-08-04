"""
name:    VnLargeCapexProfitGuard
summary: Long large caps whose capex is fully funded by operating cash flow, with
         positive profit and price above the 12/36 EMA trend.
idea:    Adding a profit guard (positive quarterly profit, and exit when it turns
         negative) to the capex-discipline gate filters large caps that fund
         investment internally yet are already losing money. In a 2022-style
         downturn, unprofitable but cash-funded names can still fall hard, so the
         profit condition is the extra defensive screen; exit adds it to the
         baseline negative-cash, capex-outrun, and trend-break rules.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)

        fundamentals_known = self.op.notna(operating_cash_flow) & self.op.notna(capex) & self.op.notna(net_profit)

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (capex < operating_cash_flow)
            & (net_profit > 0)
            & (close > ema_slow)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (
            (operating_cash_flow < 0)
            | (capex > operating_cash_flow)
            | (net_profit < 0)
            | (close < ema_slow)
        )

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
