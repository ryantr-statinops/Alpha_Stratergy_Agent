"""
name:    VnLargeCsCashValueComposite
summary: Allocate across large caps by an equal blend of pre-working-capital cash
         strength (Q04) and earnings yield (V06), cross-sectionally market-neutral.
idea:    Q04 and V06 are two orthogonal and individually stable large-cap signals:
         Q04 is a cash-residual quality dimension (operating cash earnings before
         working-capital changes net of reported profitability), while V06 is a
         valuation dimension (trailing earnings yield). Blending the two z-scored
         cross-sections diversifies slow fundamental quality against cheapness,
         which should be more robust than relying on either single factor in an
         efficiently priced large-cap universe.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        pre_wc_operating = self.data.fun_cf_operating_profit_loss_before_changes_in_wc_quarterly_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        close = self.data.pv_close_panel

        pre_wc_roa = self.feat.safe_divide_panel(pre_wc_operating, total_assets)
        profit_roa = self.feat.safe_divide_panel(net_profit, total_assets)
        cash_strength = pre_wc_roa - profit_roa
        earnings_yield = self.feat.safe_divide_panel(eps, close)

        eligible = (
            (pre_wc_operating > 0)
            & (net_profit > 0)
            & (total_assets > 0)
            & (eps > 0)
            & (close > 0)
        )

        quality_score = self.op.zscore_cs_panel(cash_strength, mask=eligible)
        value_score = self.op.zscore_cs_panel(earnings_yield, mask=eligible)
        signal = quality_score + value_score

        weights = self.op.portfolio_weights_panel(signal, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)