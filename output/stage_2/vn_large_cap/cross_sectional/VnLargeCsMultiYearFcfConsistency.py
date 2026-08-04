"""
name:    VnLargeCsMultiYearFcfConsistency
summary: Allocate across large caps by consistently positive free cash flow
         scaled by assets, cross-sectionally z-scored and market-neutral.
idea:    Distributable cash that recurs matters more than a single high free cash
         flow yield driven by capex timing. In the panel convention fixed-asset
         purchases are reported as a nonpositive outflow, so free cash flow is
         operating cash flow plus that outflow. An EMA of FCF over assets
         reflects multi-year consistency, and names with positive smoothed FCF
         are favored in the long side.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel

        free_cash_flow = operating_cash_flow + capex
        fcf_roa = self.feat.safe_divide_panel(free_cash_flow, total_assets)
        consistent_fcf = self.feat.ema_panel(fcf_roa)

        eligible = (operating_cash_flow > 0) & (capex <= 0) & (total_assets > 0) & (free_cash_flow > 0)

        consistency_score = self.op.zscore_cs_panel(consistent_fcf, mask=eligible)

        weights = self.op.portfolio_weights_panel(consistency_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)