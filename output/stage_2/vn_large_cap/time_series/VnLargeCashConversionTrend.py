"""
name:    VnLargeCashConversionTrend
summary: Long large caps whose annual profit is well backed by cash, in a
         12/36 EMA uptrend.
idea:    Cash conversion (annual CFO over net profit) measures earnings quality:
         profit that lands in the bank is more durable than profit held in
         accruals. Requiring a healthy conversion ratio and an intact 12/36
         trend keeps the position in genuinely cash-generative large caps.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)

        conversion = operating_cash_flow / net_profit
        fundamentals_known = (
            self.op.notna(operating_cash_flow)
            & self.op.notna(net_profit)
            & (net_profit > 0)
            & self.op.notna(conversion)
        )

        base_entry = fundamentals_known & (conversion > 0.5) & (close > ema_slow)
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (net_profit < 0) | (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
