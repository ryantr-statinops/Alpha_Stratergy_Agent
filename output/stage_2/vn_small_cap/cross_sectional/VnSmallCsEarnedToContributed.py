"""
name:    VnSmallCsEarnedToContributed
summary: Allocate across small caps by earned-to-contributed capital: retained
         undistributed earnings relative to paid-in capital and capital surplus.
         Market-neutral cross-sectional book.
idea:    Retained earnings relative to contributed capital reflect the corporate
         lifecycle and the quality of accumulated profits. Firms whose equity is
         built from earned profit rather than paid-in capital show durable
         value creation. This is a very slow lifecycle state that is smallly
         orthogonal to short-horizon price and momentum factors.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        undistributed = self.data.fun_bs_undistributed_earnings_quarterly_panel
        paid_in = self.data.fun_bs_paid_in_capital_quarterly_panel
        capital_surplus = self.data.fun_bs_capital_surplus_quarterly_panel

        contributed_capital = paid_in + capital_surplus
        earned_ratio = self.feat.safe_divide_panel(undistributed, contributed_capital)

        input_sum = undistributed + paid_in + capital_surplus
        eligible = (input_sum == input_sum) & (contributed_capital > 0)

        earned_score = self.op.zscore_cs_panel(earned_ratio, mask=eligible)

        weights = self.op.portfolio_weights_panel(earned_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)