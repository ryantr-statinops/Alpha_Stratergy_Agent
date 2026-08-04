"""
name:    VnLargeCsResidualTangibleBook
summary: Allocate across large caps by tangible book value to market
         capitalization orthogonalized against earnings yield, market-neutral.
idea:    The prior level-only version overfit (Train Sharpe 1.33 collapsed to 0.42
         OOS) because raw tangible-book-to-price is dominated by generic cheapness.
         Orthogonalizing against the earnings-yield rank keeps only the tangible
         asset backing that is not already captured by EP, so the signal is far
         less concentrated in value and more stable out of sample.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        owners_equity = self.data.fun_bs_owners_equity_quarterly_panel
        goodwill = self.data.fun_bs_good_will_quarterly_panel
        intangible_assets = self.data.fun_bs_intangible_fixed_assets_quarterly_panel
        close = self.data.pv_close_panel
        common_shares = self.data.fun_bs_common_shares_quarterly_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel

        market_cap = close * common_shares
        tangible_book = owners_equity - goodwill - intangible_assets
        tangible_book_yield = self.feat.safe_divide_panel(tangible_book, market_cap)
        earnings_yield = self.feat.safe_divide_panel(eps, close)

        eligible = (
            (tangible_book > 0)
            & (common_shares > 0)
            & (market_cap > 0)
            & (eps > 0)
            & (close > 0)
        )

        tangible_rank = self.op.rank_cs_panel(tangible_book_yield, mask=eligible)
        earnings_rank = self.op.rank_cs_panel(earnings_yield, mask=eligible)
        signal = tangible_rank - earnings_rank

        weights = self.op.portfolio_weights_panel(signal, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)