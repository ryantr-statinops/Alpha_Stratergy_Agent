"""
name:    VnMidCsValueMomentumComposite
summary: Buy mid caps that are cheap on quarterly earnings yield, financially
         strong, liquid, and above their price trend. Momentum-squared is the
         core; value and quality are discipline layers. Market-neutral book.
idea:    The momentum term (close/ema) squared is the dominant driver and is a
         stable factor on VN. Earnings yield keeps the screen from chasing
         overvalued trends, while an equity/assets floor and a top-60% liquidity
         rank hold a clean, tradable cross-section. Magnitude weighting
         (demean_l1) lets the strongest composite names drive the book instead
         of flattening dispersion the way rank weighting does. All fields are
         quarterly; no cash-flow fields, so coverage stays broad. Tests whether
         the small-cap passing structure generalizes to the mid-cap universe.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel

        earnings_yield = self.feat.safe_divide_panel(eps, close)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        trend_ratio = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        base_eligible = (
            (eps > 0) & (close > 0) & (volume > 0) & (equity > 0)
            & (total_assets > 0) & (capital_strength > 0.15)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        signal = earnings_yield * trend_ratio * trend_ratio

        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
