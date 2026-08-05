"""
name:    VnLargeCashSpreadLooseSlow
summary: Long large caps with looser cash-earnings spread (0.3) and slow
         14/42 EMA for lower turnover.
idea:    Combines the looser cash-quality threshold (0.3) that improved Test
         returns with the slower 14/42 EMA profile to reduce turnover. The
         slower timing may filter out short-term noise that erodes the loose
         threshold's wider coverage.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual

        ema_fast = self.feat.ema(close, timeperiod=14)
        ema_slow = self.feat.ema(close, timeperiod=42)

        fundamentals_known = (
            self.op.notna(operating_cash_flow)
            & self.op.notna(net_profit)
            & (net_profit > 0)
        )

        cash_quality = operating_cash_flow / net_profit

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (cash_quality > 0.3)
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
