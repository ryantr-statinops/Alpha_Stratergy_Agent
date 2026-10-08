"""
name:    VnLargeAgreement1854
summary: Long large caps with positive cash flow and profit confirmed by 18/54
         and 30/90 EMA trend agreement.
idea:    Pushing both trend horizons to the stable-hold family (18/54 and 30/90)
         makes the quality gate dominant over the price timing, which should
         defend the 2022 regime where fast EMAs whipsawed. Positive annual CFO
         and positive quarterly profit define the hold set; exit only on the
         faster 18/54 stack breaking down.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly

        ema_fast_short = self.feat.ema(close, timeperiod=18)
        ema_slow_short = self.feat.ema(close, timeperiod=54)
        ema_fast_long = self.feat.ema(close, timeperiod=30)
        ema_slow_long = self.feat.ema(close, timeperiod=90)

        fundamentals_known = self.op.notna(operating_cash_flow) & self.op.notna(net_profit)

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (net_profit > 0)
            & (ema_fast_short > ema_slow_short)
            & (ema_fast_long > ema_slow_long)
        )
        strong_entry = base_entry & (close > ema_slow_long)
        exit_setup = (ema_fast_short < ema_slow_short)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
