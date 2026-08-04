"""
name:    VnLargeCsPreWcMagnitude
summary: Allocate across large caps by winsorized pre-working-capital cash
         strength with magnitude-sensitive market-neutral weights.
idea:    Keeping magnitude in the portfolio weights (demean_l1) instead of
         collapsing to ranks preserves how strongly a large cap exceeds the
         cross-section in cash strength. Winsorizing to the 2-98 percentiles
         first prevents a few extreme accounting readings from dominating the
         book, so the exposure reflects the size of the cash-quality advantage
         rather than just its ordering.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        pre_wc_operating = self.data.fun_cf_operating_profit_loss_before_changes_in_wc_quarterly_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel

        pre_wc_roa = self.feat.safe_divide_panel(pre_wc_operating, total_assets)
        profit_roa = self.feat.safe_divide_panel(net_profit, total_assets)
        pre_wc_cash_strength = pre_wc_roa - profit_roa

        eligible = (pre_wc_operating > 0) & (net_profit > 0) & (total_assets > 0)

        clean = self.op.winsorize_cs_panel(pre_wc_cash_strength, mask=eligible, lower=0.02, upper=0.98)
        strength_score = self.op.zscore_cs_panel(clean, mask=eligible)

        weights = self.op.portfolio_weights_panel(strength_score, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)