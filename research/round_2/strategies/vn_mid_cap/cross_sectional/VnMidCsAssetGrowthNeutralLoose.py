"""
name:    VnMidCsAssetGrowthNeutralLoose
summary: Allocate across mid caps by asset growth made neutral to persistent
         cash profitability: unexplained asset growth (rank of asset growth
         minus rank of cash ROA) is penalized, with a loose CFO guard.
         Market-neutral cross-sectional book.
idea:    High asset growth predicts lower returns, but growth accompanied by
         persistent cash productivity should not be punished like empire
         building. Neutralizing raw asset growth against trailing cash ROA
         isolates the unexplained expansion component. The strict positive-CFO
         gate is replaced by a loose availability guard so firms with a
         temporarily negative cash flow stay eligible, keeping the
         cross-section broad per the tolerance-band convention.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        total_assets = self.data.fun_bs_total_assets_annual_panel
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel

        asset_growth = self.feat.safe_divide_panel(self.feat.delta_panel(total_assets), total_assets)
        cash_roa = self.feat.safe_divide_panel(operating_cash_flow, total_assets)
        persistent_cash_roa = self.feat.ema_panel(cash_roa)

        input_sum = total_assets + operating_cash_flow
        eligible = (input_sum == input_sum) & (total_assets > 0)

        growth_rank = self.op.rank_cs_panel(asset_growth, mask=eligible)
        cash_roa_rank = self.op.rank_cs_panel(persistent_cash_roa, mask=eligible)
        neutral_growth = growth_rank - cash_roa_rank
        growth_score = self.op.zscore_cs_panel(0 - neutral_growth, mask=eligible)

        weights = self.op.portfolio_weights_panel(growth_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)