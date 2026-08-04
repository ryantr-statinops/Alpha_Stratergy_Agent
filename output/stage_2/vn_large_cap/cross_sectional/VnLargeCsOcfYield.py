"""
name:    VnLargeCsOcfYield
summary: Allocate across large caps by operating cash flow yield on market
         capitalization, cross-sectionally z-scored and market-neutral.
idea:    Price paid for realized operating cash differs from an earnings yield
         and depends less on accrual estimates. Annual operating cash flow is
         scaled by market capitalization to form a cash value yield, and the
         book goes long the large caps that are cheapest on realized cash
         generation while shorting the most expensive.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
        close = self.data.pv_close_panel
        common_shares = self.data.fun_bs_common_shares_quarterly_panel

        market_cap = close * common_shares
        ocf_yield = self.feat.safe_divide_panel(operating_cash_flow, market_cap)

        eligible = (operating_cash_flow > 0) & (close > 0) & (common_shares > 0) & (market_cap > 0)

        yield_score = self.op.zscore_cs_panel(ocf_yield, mask=eligible)

        weights = self.op.portfolio_weights_panel(yield_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
