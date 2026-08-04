"""
name:    VnLargeCsResidualFcfYield
summary: Allocate across large caps by free cash flow yield on market
         capitalization, cross-sectionally z-scored and market-neutral.
idea:    Subtracting reinvestment from operating cash flow measures cash left
         after capex. In the panel convention fixed-asset purchases are a
         nonpositive outflow, so FCF is operating cash flow plus that outflow.
         The FCF yield on market capitalization is used at its level form here
         (capex-intensity residualization is a documented leg), preferring
         large caps whose cash generation still exceeds reinvestment when valued
         against the market.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual_panel
        close = self.data.pv_close_panel
        common_shares = self.data.fun_bs_common_shares_quarterly_panel

        market_cap = close * common_shares
        free_cash_flow = operating_cash_flow + capex
        fcf_yield = self.feat.safe_divide_panel(free_cash_flow, market_cap)

        eligible = (free_cash_flow > 0) & (capex <= 0) & (close > 0) & (common_shares > 0) & (market_cap > 0)

        yield_score = self.op.zscore_cs_panel(fcf_yield, mask=eligible)

        weights = self.op.portfolio_weights_panel(yield_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)