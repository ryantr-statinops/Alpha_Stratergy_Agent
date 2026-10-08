"""
name:    VnLargeCsEarningsYield
summary: Allocate across large caps by positive earnings-to-price yield,
         cross-sectionally z-scored and market-neutral.
idea:    Earnings yield is the strongest single value measure in Vietnamese
         factor evidence, so it is kept here as a clean, transparent value
         benchmark leg. The cross-section goes long the cheapest large caps on
         trailing EPS-to-price and short the richest, making this the reference
         control against which every residual value signal must be measured.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        eps = self.data.fun_is_eps_basis_quarterly_panel
        close = self.data.pv_close_panel

        earnings_yield = self.feat.safe_divide_panel(eps, close)

        eligible = (eps > 0) & (close > 0)

        value_score = self.op.zscore_cs_panel(earnings_yield, mask=eligible)

        weights = self.op.portfolio_weights_panel(value_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
