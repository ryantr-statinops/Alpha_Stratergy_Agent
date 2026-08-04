"""
name:    VnLargeCsEarningsMagnitude
summary: Allocate across large caps by winsorized earnings-to-price yield with
         magnitude-sensitive market-neutral weights.
idea:    A magnitude-preserving portfolio rewards large caps in proportion to how
         cheap they are on trailing EPS rather than only their rank. Winsorizing
         the yield to the 2-98 percentiles before z-scoring stops extreme value
         outliers from dominating, so the book scales with relative cheapness
         while keeping the value ordering stable.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        eps = self.data.fun_is_eps_basis_quarterly_panel
        close = self.data.pv_close_panel

        earnings_yield = self.feat.safe_divide_panel(eps, close)

        eligible = (eps > 0) & (close > 0)

        clean = self.op.winsorize_cs_panel(earnings_yield, mask=eligible, lower=0.02, upper=0.98)
        value_score = self.op.zscore_cs_panel(clean, mask=eligible)

        weights = self.op.portfolio_weights_panel(value_score, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)