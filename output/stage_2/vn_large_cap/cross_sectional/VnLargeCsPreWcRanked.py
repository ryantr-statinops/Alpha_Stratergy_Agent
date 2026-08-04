"""
name:    VnLargeCsPreWcRanked
summary: Allocate across large caps by rank of pre-working-capital cash strength,
         cross-sectionally rank-demeaned and market-neutral.
idea:    Ranks absorb the unstable magnitude of accounting ratios, so the base
         pre-working-capital cash strength is converted directly to its
         cross-sectional percentile instead of being z-scored. This makes the
         book robust to scale drift and extreme readings while retaining the
         order of cash strength across large caps.
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

        strength_score = self.op.rank_cs_panel(pre_wc_cash_strength, mask=eligible)

        weights = self.op.portfolio_weights_panel(strength_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)