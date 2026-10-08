"""
name:    VnLargeCsCompositeMagnitude
summary: Allocate across large caps by magnitude-weighted blend of cash strength
         and earnings yield, cross-sectionally market-neutral.
idea:    This composite keeps the two stable legs (pre-working-capital cash
         strength and earnings yield) but applies magnitude-sensitive demeaning
         so the book scales with the strength of each signal rather than ranks.
         Each leg is winsorized and z-scored before the equal sum, preventing
         extreme readings from dominating the blend.
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

        quality_clean = self.op.winsorize_cs_panel(cash_strength, mask=eligible, lower=0.02, upper=0.98)
        quality_score = self.op.zscore_cs_panel(quality_clean, mask=eligible)
        value_clean = self.op.winsorize_cs_panel(earnings_yield, mask=eligible, lower=0.02, upper=0.98)
        value_score = self.op.zscore_cs_panel(value_clean, mask=eligible)
        signal = quality_score + value_score

        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)