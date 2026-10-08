"""
name:    VnMidTrendQuality
summary: Long mid caps that combine a confirmed uptrend with improving
         return on equity and a solid capital base.
idea:    Mid caps tend to reward quality during the middle of a trend cycle.
         Requiring price above the slow average, an improving ROE step and an
         equity-to-assets floor filters out momentum-only names that are
         structurally weak. Position strengthens as the trend matures.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close

        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly
        eps = self.data.fun_is_eps_basis_quarterly
        equity = self.data.fun_bs_owners_equity_quarterly
        total_assets = self.data.fun_bs_total_assets_quarterly

        ema_fast = self.feat.ema(close, timeperiod=18)
        ema_slow = self.feat.ema(close, timeperiod=54)

        roe = net_profit / equity
        capital_ratio = equity / total_assets

        profit_growth = self.op.pct_change(net_profit, periods=1)
        eps_growth = self.op.pct_change(eps, periods=1)

        fundamentals_known = (
            self.op.notna(net_profit)
            & self.op.notna(equity)
            & (equity > 0)
            & self.op.notna(total_assets)
            & (total_assets > 0)
            & self.op.notna(roe)
            & self.op.notna(capital_ratio)
            & self.op.notna(profit_growth)
            & self.op.notna(eps_growth)
        )

        weak_long = (
            fundamentals_known
            & (close > ema_slow)
            & (roe > 0.02)
            & (capital_ratio > 0.10)
            & (profit_growth > -0.10)
            & (eps_growth > -0.10)
        )

        strong_long = (
            weak_long
            & (ema_fast > ema_slow)
            & (roe > 0.04)
            & (profit_growth > 0)
            & (eps_growth > 0)
        )

        exit_setup = (close < ema_slow) | (capital_ratio < 0.06)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
