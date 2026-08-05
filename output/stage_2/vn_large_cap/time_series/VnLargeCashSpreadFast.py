"""
name:    VnLargeCashSpreadFast
summary: Long large caps with positive cash-earnings spread using fast 8/24
         EMA timing for quicker entry.
idea:    Variant of CashEarningsSpreadTrend with faster trend timing. The
         8/24 EMA may capture uptrends earlier and reduce lag that causes
         the strategy to miss rallies in the Test period.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)

        fundamentals_known = (
            self.op.notna(operating_cash_flow)
            & self.op.notna(net_profit)
            & (net_profit > 0)
        )

        cash_quality = operating_cash_flow / net_profit

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (cash_quality > 0.5)
            & (close > ema_slow)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (
            (operating_cash_flow < 0)
            | (net_profit < 0)
            | (close < ema_slow)
        )

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
