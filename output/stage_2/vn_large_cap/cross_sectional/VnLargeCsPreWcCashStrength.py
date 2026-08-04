"""
name:    VnLargeCsPreWcCashStrength
summary: Allocate across large caps by operating cash strength before working
         capital changes, net of profitability, cross-sectionally market-neutral.
idea:    Operating profit before changes in working capital isolates a firm's
         earning power from working-capital releases or builds. The residual
         spread against asset-scaled net profit keeps cash strength that is not
         already captured by accounting profitability, so the book prefers
         large caps whose operating engine generates cash beyond reported
         earnings.
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

        strength_score = self.op.zscore_cs_panel(pre_wc_cash_strength, mask=eligible)

        weights = self.op.portfolio_weights_panel(strength_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
