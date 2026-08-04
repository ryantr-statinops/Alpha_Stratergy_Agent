"""
name:    VnLargeAgreementHysteresis
summary: Long large caps with positive cash flow and profit in 8/24 + 12/36
         trend agreement, requiring price above a dead-band on the 36 EMA.
idea:    A dead-band (price must clear 2% above the 36 EMA before full size)
         stops a one-day close hovering on the line from flipping the position.
         This noise filter preserves the cash-flow quality gate while reducing
         the churn that hurt the 2022 drawdown; exit couples the fast break
         with price falling under the slow regime.
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
        strong_entry = base_entry & (close > ema_slow_long * 1.02)
        exit_setup = (ema_fast_short < ema_slow_short) | (close < ema_slow_long)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
