"""
name:    VnLargeAgreementConversion
summary: Long large caps with positive cash flow and profit, cash conversion
         above 0.5, in 8/24 + 12/36 EMA trend agreement.
idea:    Adding a cash-conversion floor (annual CFO at least half of net profit)
         raises the earnings-quality bar inside the trend-agreement hold. Cash
         profits that are actually collected are less likely to be revised away
         in a downturn, so the 2022 defense comes from holding only the most
         cash-backed large caps while both trend horizons agree.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly

        ema_fast_short = self.feat.ema(close, timeperiod=8)
        ema_slow_short = self.feat.ema(close, timeperiod=24)
        ema_fast_long = self.feat.ema(close, timeperiod=12)
        ema_slow_long = self.feat.ema(close, timeperiod=36)

        conversion = operating_cash_flow / net_profit
        fundamentals_known = (
            self.op.notna(operating_cash_flow)
            & self.op.notna(net_profit)
            & (net_profit > 0)
            & self.op.notna(conversion)
        )

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (conversion > 0.5)
            & (ema_fast_short > ema_slow_short)
            & (ema_fast_long > ema_slow_long)
        )
        strong_entry = base_entry & (close > ema_slow_long)
        exit_setup = (ema_fast_short < ema_slow_short)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
