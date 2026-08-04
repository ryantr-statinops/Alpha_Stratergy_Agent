"""
name:    VnLargeCsEarningsWinsorized
summary: Allocate across large caps by winsorized earnings-to-price yield,
         cross-sectionally rank-demeaned and market-neutral.
idea:    A raw earnings yield z-score can be dominated by a few cheap large caps
         with extreme EP outliers. Winsorizing the yield to the 2–98 percentiles
         before z-scoring keeps the value ordering while dampening the tail that
         a handful of names drives, stabilizing the value leg out of sample.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        eps = self.data.fun_is_eps_basis_quarterly_panel
        close = self.data.pv_close_panel

        earnings_yield = self.feat.safe_divide_panel(eps, close)

        eligible = (eps > 0) & (close > 0)

        clean = self.op.winsorize_cs_panel(earnings_yield, mask=eligible, lower=0.02, upper=0.98)
        value_score = self.op.zscore_cs_panel(clean, mask=eligible)

        weights = self.op.portfolio_weights_panel(value_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)