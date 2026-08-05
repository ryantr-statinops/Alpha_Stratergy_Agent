"""
name:    VnSmallCsAssetGrowthNeutral
summary: Allocate across small caps by asset growth made neutral to persistent
         cash profitability: unexplained asset growth (rank of asset growth
         minus rank of cash ROA) is penalized. Market-neutral cross-sectional
         book.
idea:    High asset growth predicts lower returns, but growth accompanied by
         persistent cash productivity should not be punished like empire
         building. Neutralizing raw asset growth against trailing cash ROA
         isolates the unexplained expansion component. Low unexplained growth
         is preferred, capturing the investment dimension without confounding
         with cash profitability.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        total_assets = self.data.fun_bs_total_assets_annual_panel
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel

        asset_growth = self.feat.safe_divide_panel(self.feat.delta_panel(total_assets), total_assets)
        cash_roa = self.feat.safe_divide_panel(operating_cash_flow, total_assets)
        persistent_cash_roa = self.feat.ema_panel(cash_roa)

        input_sum = total_assets + operating_cash_flow
        eligible = (input_sum == input_sum) & (total_assets > 0) & (operating_cash_flow > 0)

        growth_rank = self.op.rank_cs_panel(asset_growth, mask=eligible)
        cash_roa_rank = self.op.rank_cs_panel(persistent_cash_roa, mask=eligible)
        neutral_growth = growth_rank - cash_roa_rank
        growth_score = self.op.zscore_cs_panel(0 - neutral_growth, mask=eligible)

        weights = self.op.portfolio_weights_panel(growth_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)