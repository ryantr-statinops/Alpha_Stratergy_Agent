"""
name:    VnMidCsShortTermRefinance
summary: Allocate across mid caps by short-term refinancing pressure:
         firms whose short-term loans exceed liquid assets rank worst.
         Market-neutral cross-sectional book.
idea:    A wall of short-term debt creates convex downside even before total
         leverage looks extreme. mid caps with short-term loans far above
         cash and short-term investments are structurally exposed to rollover
         stress; ranking them last harvests a fragility premium that broad
         factor portfolios ignore. The book prefers balance sheets that can
         absorb a shock.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        short_loans = self.data.fun_bs_short_term_loans_quarterly_panel
        cash = self.data.fun_bs_cash_and_cash_equivalents_quarterly_panel
        st_invest = self.data.fun_bs_short_term_investments_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel

        liquid = cash + st_invest
        liquid_buffer = liquid - short_loans
        buffer_ratio = self.feat.safe_divide_panel(liquid_buffer, total_assets)

        input_sum = cash + st_invest + short_loans + total_assets
        eligible = (input_sum == input_sum) & (total_assets > 0)

        buffer_score = self.op.zscore_cs_panel(buffer_ratio, mask=eligible)

        weights = self.op.portfolio_weights_panel(buffer_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)