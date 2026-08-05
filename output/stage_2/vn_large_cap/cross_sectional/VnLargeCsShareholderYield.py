"""
name:    VnLargeCsShareholderYield
summary: Allocate across large caps by shareholder yield: net payout yield plus
         net debt paydown, combined by equal rank. Market-neutral
         cross-sectional book.
idea:    A mature firm returns cash to capital providers through dividends,
         buybacks and net debt reduction. Combining net payout (dividends plus
         repurchases minus issuance) with net debt repayment captures total
         cash distribution to all capital providers. In the panel convention
         dividends, repurchases and repayments are nonpositive outflows and
         issuance and borrowings are positive inflows. Equal-rank combination
         avoids fitting weights between the two legs.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        dividends = self.data.fun_cf_dividends_paid_annual_panel
        repurchases = self.data.fun_cf_payments_for_share_returns_and_repurchases_annual_panel
        issuance = self.data.fun_cf_proceeds_from_issue_of_shares_annual_panel
        borrowings = self.data.fun_cf_proceeds_from_borrowings_annual_panel
        repayments = self.data.fun_cf_repayment_of_borrowings_annual_panel
        common_shares = self.data.fun_bs_common_shares_annual_panel
        close = self.data.pv_close_panel

        market_value = close * common_shares
        gross_payout = (0 - dividends) + (0 - repurchases) - issuance
        net_debt_paydown = (0 - repayments) - borrowings

        payout_yield = self.feat.safe_divide_panel(gross_payout, market_value)
        paydown_yield = self.feat.safe_divide_panel(net_debt_paydown, market_value)

        input_sum = dividends + repurchases + issuance + borrowings + repayments + common_shares + close
        eligible = (input_sum == input_sum) & (common_shares > 0) & (close > 0) & (market_value > 0)

        payout_rank = self.op.rank_cs_panel(payout_yield, mask=eligible)
        paydown_rank = self.op.rank_cs_panel(paydown_yield, mask=eligible)
        shareholder_yield = payout_rank + paydown_rank
        yield_score = self.op.zscore_cs_panel(shareholder_yield, mask=eligible)

        weights = self.op.portfolio_weights_panel(yield_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)