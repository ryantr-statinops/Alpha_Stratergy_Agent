"""
name:    VnLargeCsCashFlowYield
summary: Allocate across large caps by cash-flow-to-price value, cross-sectionally
         z-scored and market-neutral.
idea:    Operating cash flow is the hardest number to dress up, so a
         cash-flow-to-price yield isolates large caps whose value rests on real
         cash generation rather than accrual-based profit. The yield is z-scored
         across the eligible large-cap cross-section and converted to a
         rank-demeaned, L1-normalized long/short portfolio.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel

        cash_flow_yield = self.feat.safe_divide_panel(operating_cash_flow, close)

        eligible = (operating_cash_flow > 0) & (close > 0)

        value_score = self.op.zscore_cs_panel(cash_flow_yield, mask=eligible)

        signal = value_score

        weights = self.op.portfolio_weights_panel(signal, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
