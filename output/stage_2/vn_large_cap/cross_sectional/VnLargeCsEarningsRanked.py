"""
name:    VnLargeCsEarningsRanked
summary: Allocate across large caps by rank of earnings-to-price yield,
         cross-sectionally rank-demeaned and market-neutral.
idea:    Ranking the earnings yield cross-sectionally makes the value signal
         invariant to the scale of EPS across large caps, so the book reflects
         relative cheapness rather than absolute yield magnitude. This reduces
         the influence of large-cap EPS outliers and keeps the value leg stable
         across regimes.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        eps = self.data.fun_is_eps_basis_quarterly_panel
        close = self.data.pv_close_panel

        earnings_yield = self.feat.safe_divide_panel(eps, close)

        eligible = (eps > 0) & (close > 0)

        value_score = self.op.rank_cs_panel(earnings_yield, mask=eligible)

        weights = self.op.portfolio_weights_panel(value_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)