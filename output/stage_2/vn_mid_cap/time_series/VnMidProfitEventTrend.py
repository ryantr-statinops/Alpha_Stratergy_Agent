"""
name:    VnMidProfitEventTrend
summary: Long mid caps after a profitable quarter when the trend supports it.
idea:    Vietnam earnings are strongly seasonal; a profit event that beats the
         prior quarter keeps mid-cap names bid for weeks. Requiring net profit
         positive, profit growth positive and price above the 36-day average
         enters the trend leg. Exit on trend break or profit deterioration.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly

        ema_slow = self.feat.ema(close, timeperiod=36)

        profit_growth = self.op.pct_change(net_profit, periods=1)

        fundamentals_known = (
            self.op.notna(net_profit)
            & (net_profit > 0)
            & self.op.notna(profit_growth)
            & self.op.notna(ema_slow)
            & (close > 0)
        )

        weak_long = (
            fundamentals_known
            & (close > ema_slow)
            & (profit_growth > 0)
        )
        strong_long = weak_long & (profit_growth > 0.10)
        exit_setup = fundamentals_known & ((close < ema_slow) | (profit_growth < -0.05))

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
