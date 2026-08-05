"""
name:    VnLargeCashEarningsSpreadTrend
summary: Long large caps where operating cash flow exceeds half of net profit,
         indicating earnings backed by real cash, in an uptrend.
idea:    Accrual-heavy earnings can mask deteriorating business quality. When
         CFO materially exceeds PAT, profits are backed by actual cash
         collection. Requiring the cash-earnings spread to be positive filters
         for companies where reported profits translate into cash. The 12/36
         EMA trend adds timing discipline.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)

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
