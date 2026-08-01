"""
name:    VnLargeCsValueMomentum
summary: Allocate across large caps by a composite of cheap valuation and
         recent price strength relative to the cross-section.
idea:    Large caps tend to be priced efficiently, but a blend of earnings
         yield and short-term price momentum still separates names that are
         both reasonably valued and being re-rated. The two sub-signals are
         cross-sectionally z-scored and summed so neither dominates the book.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel

        earnings_yield = self.feat.safe_divide_panel(eps, close)
        price_momentum = self.feat.rolling_zscore_panel(close)

        eligible = self.op.notna(eps) & (close > 0)

        value_score = self.op.zscore_cs_panel(earnings_yield, mask=eligible)
        momentum_score = self.op.zscore_cs_panel(price_momentum, mask=eligible)

        signal = value_score + momentum_score

        weights = self.op.portfolio_weights_panel(signal, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
