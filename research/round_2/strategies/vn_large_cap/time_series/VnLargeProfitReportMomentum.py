"""
name:    VnLargeProfitReportMomentum
summary: Hold profitable large caps in an 8/24 EMA trend and use positive
         quarterly profit reports to increase exposure.
idea:    Positive quarterly profit is the persistent eligibility state and the
         8/24 trend controls holding. A positive report step is only a
         strong-position overlay, avoiding the sparse one-day event behavior of
         the original implementation.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)

        profit_growth = self.op.pct_change(net_profit, periods=1)
        fundamentals_known = (
            self.op.notna(net_profit)
            & (net_profit > 0)
            & self.op.notna(profit_growth)
        )

        base_entry = fundamentals_known & (ema_fast > ema_slow) & (close > ema_slow)
        strong_entry = base_entry & (profit_growth > 0)
        exit_setup = (net_profit < 0) | (ema_fast < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
