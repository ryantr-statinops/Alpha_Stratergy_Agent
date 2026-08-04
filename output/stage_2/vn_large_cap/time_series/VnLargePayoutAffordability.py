"""
name:    VnLargePayoutAffordability
summary: Long large caps whose operating cash flow exceeds dividends paid, with
         price above the 8/24 EMA trend.
idea:    Dividends paid entirely from operating cash flow, without resorting to
         debt, signal that the payout is affordable and sustainable. Holding only
         names where annual CFO covers annual dividends, in an 8/24 EMA uptrend,
         keeps both a cash-backed payout and a healthy trend; exit when the cash
         no longer covers the dividend or the trend breaks.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        dividends_paid = self.data.fun_cf_dividends_paid_annual

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)

        fundamentals_known = self.op.notna(operating_cash_flow) & self.op.notna(dividends_paid)

        base_entry = (
            fundamentals_known
            & (dividends_paid > 0)
            & (operating_cash_flow > dividends_paid)
            & (close > ema_slow)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (operating_cash_flow < dividends_paid) | (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
