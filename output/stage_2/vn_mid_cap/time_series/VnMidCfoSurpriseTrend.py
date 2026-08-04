"""
name:    VnMidCfoSurpriseTrend
summary: Long mid caps with positive cash-flow surprise and cash quality.
idea:    Reported profits that are not backed by operating cash flow often
         reverse in mid caps. Requiring positive CFO, accelerating CFO growth,
         a cash conversion above 0.5 and price above the slow average keeps the
         trade on genuine cash generation. Exit on trend break or CFO decay.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        cfo = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly

        ema_slow = self.feat.ema(close, timeperiod=30)

        cfo_growth = self.op.pct_change(cfo, periods=1)
        conversion = cfo / net_profit

        fundamentals_known = (
            self.op.notna(cfo)
            & (cfo > 0)
            & self.op.notna(net_profit)
            & (net_profit > 0)
            & self.op.notna(cfo_growth)
            & self.op.notna(conversion)
            & self.op.notna(ema_slow)
            & (close > 0)
        )

        weak_long = (
            fundamentals_known
            & (conversion > 0.5)
            & (close > ema_slow)
            & (cfo_growth > 0)
        )
        strong_long = weak_long & (cfo_growth > 0.10)
        exit_setup = fundamentals_known & ((close < ema_slow) | (cfo_growth < -0.05))

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
