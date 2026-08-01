"""
name:    VnSmallCsEpsRank
summary: Allocate across small caps by the speed of quarterly EPS
         improvement relative to the rest of the universe.
idea:    Earnings acceleration is most informative in the small-cap segment
         where analyst coverage is thin. Ranking the cross-section by the
         quarter-on-quarter change in EPS and going long the relative
         improvers produces a market-neutral book that captures this
         mispricing without taking a directional bet.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel

        eps_change = self.feat.delta_panel(eps)
        eps_growth = self.feat.safe_divide_panel(eps_change, eps)

        eligible = self.op.notna(eps) & (eps > 0) & self.op.notna(close)

        signal = eps_growth

        weights = self.op.portfolio_weights_panel(signal, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
