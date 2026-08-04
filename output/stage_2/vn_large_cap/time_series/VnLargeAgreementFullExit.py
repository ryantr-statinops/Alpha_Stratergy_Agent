"""
name:    VnLargeAgreementFullExit
summary: Long large caps with positive cash flow and profit in 8/24 + 12/36
         trend agreement, exiting on the fast break or the long regime break.
idea:    The baseline agreement exited only on the 8/24 break, which can leave
         exposure on while the slower 12/36 regime has already rolled over into
         a 2022-style decline. This variant adds an explicit second exit leg:
         leave when price closes back under the 36 EMA, coupling the fast break
         with the long-horizon regime failure.
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

        fundamentals_known = self.op.notna(operating_cash_flow) & self.op.notna(net_profit)

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (net_profit > 0)
            & (ema_fast_short > ema_slow_short)
            & (ema_fast_long > ema_slow_long)
        )
        strong_entry = base_entry & (close > ema_slow_long)
        exit_setup = (ema_fast_short < ema_slow_short) | (close < ema_slow_long)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
