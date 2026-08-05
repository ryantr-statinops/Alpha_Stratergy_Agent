"""
name:    VnLargeCashSpreadCapex
summary: Long large caps with positive cash-earnings spread AND capex
         discipline, using 12/36 EMA trend.
idea:    Combining two independent cash-quality signals: (1) CFO materially
         backs reported earnings, and (2) capital expenditure is fully funded
         by operating cash flow. Each signal captures a different dimension of
         cash quality — the spread measures earnings authenticity, while capex
         discipline measures investment restraint. Together they create a
         stricter quality gate while maintaining the proven trend timing.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)

        fundamentals_known = (
            self.op.notna(operating_cash_flow)
            & self.op.notna(net_profit)
            & self.op.notna(capex)
            & (net_profit > 0)
        )

        cash_quality = operating_cash_flow / net_profit

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (cash_quality > 0.3)
            & (capex < operating_cash_flow)
            & (close > ema_slow)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (
            (operating_cash_flow < 0)
            | (net_profit < 0)
            | (capex > operating_cash_flow)
            | (close < ema_slow)
        )

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
