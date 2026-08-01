"""
name:    VnSmallEpsGrowthMomentum
summary: Long small caps whose quarterly EPS is improving while the stock
         trades above its short-term trend and volume confirms participation.
idea:    Small caps are often mispriced when the market has not yet priced in
         a turn in earnings. A positive quarter-on-quarter step in EPS combined
         with price above the 20-day average and above-average volume captures
         the early re-rating. Position scales up when the trend is intact.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        eps = self.data.fun_is_eps_basis_quarterly
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly

        sma20 = self.feat.sma(close, timeperiod=20)
        ema_slow = self.feat.ema(close, timeperiod=54)
        volume_base = self.feat.sma(volume, timeperiod=20)

        eps_growth = self.op.pct_change(eps, periods=1)
        profit_growth = self.op.pct_change(net_profit, periods=1)

        fundamentals_known = (
            self.op.notna(eps)
            & (eps > 0)
            & self.op.notna(eps_growth)
            & self.op.notna(net_profit)
            & self.op.notna(profit_growth)
        )

        weak_long = (
            fundamentals_known
            & (close > sma20)
            & (eps_growth > -0.05)
            & (profit_growth > -0.05)
        )

        strong_long = (
            weak_long
            & (eps_growth > 0)
            & (profit_growth > 0)
            & (close > ema_slow)
            & (volume > volume_base)
        )

        exit_setup = (close < sma20) | (eps_growth < -0.20)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
