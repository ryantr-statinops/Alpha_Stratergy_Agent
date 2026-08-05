"""
name:    VnLargeCsInternallyFundedCapex
summary: Allocate across large caps by how much capex is funded internally from
         operating cash flow rather than external borrowing or issuance, scaled
         by assets. Market-neutral cross-sectional book.
idea:    Capital expenditure covered by operating cash flow reduces dependence
         on issuance, borrowing and refinancing regimes. In the panel
         convention fixed-asset purchases and debt repayments are reported as
         nonpositive outflows and borrowings/issuance as positive inflows, so
         internal funding is operating cash flow plus capex and repayments
         minus borrowings and issuance. Large caps that self-fund investment
         show capital-allocation discipline.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual_panel
        borrowings = self.data.fun_cf_proceeds_from_borrowings_annual_panel
        repayments = self.data.fun_cf_repayment_of_borrowings_annual_panel
        issuance = self.data.fun_cf_proceeds_from_issue_of_shares_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel

        internal_funding = operating_cash_flow + capex + repayments - borrowings - issuance
        funding_score_raw = self.feat.safe_divide_panel(internal_funding, total_assets)

        input_sum = operating_cash_flow + capex + borrowings + repayments + issuance + total_assets
        eligible = (input_sum == input_sum) & (total_assets > 0) & (capex <= 0)

        funding_score = self.op.zscore_cs_panel(funding_score_raw, mask=eligible)

        weights = self.op.portfolio_weights_panel(funding_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)