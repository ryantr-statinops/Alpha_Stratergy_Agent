"""
name:    VnLargeCsAntiDilution
summary: Allocate across large caps by anti-dilution: firms that restrain share
         issuance and keep share count stable rank best. Market-neutral
         cross-sectional book.
idea:    Net equity issuance can reflect market timing and reduces per-share
         participation. In Vietnam's young market, frequent rights issues and
         share issuance dilute existing holders. Restraining issuance and
         keeping common-share count stable preserves per-share ownership, a
         financing-policy signal distinct from profitability and momentum.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        common_shares = self.data.fun_bs_common_shares_annual_panel
        issuance = self.data.fun_cf_proceeds_from_issue_of_shares_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel

        share_growth = self.feat.safe_divide_panel(self.feat.delta_panel(common_shares), common_shares)
        issuance_ratio = self.feat.safe_divide_panel(issuance, total_assets)

        input_sum = common_shares + issuance + total_assets
        eligible = (input_sum == input_sum) & (common_shares > 0) & (total_assets > 0)

        dilution_rank = self.op.rank_cs_panel(share_growth, mask=eligible)
        issuance_rank = self.op.rank_cs_panel(issuance_ratio, mask=eligible)
        anti_dilution = 0 - (dilution_rank + issuance_rank)
        dilution_score = self.op.zscore_cs_panel(anti_dilution, mask=eligible)

        weights = self.op.portfolio_weights_panel(dilution_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)