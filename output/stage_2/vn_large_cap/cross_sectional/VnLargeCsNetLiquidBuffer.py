"""
name:    VnLargeCsNetLiquidBuffer
summary: Allocate across large caps by net liquid-asset buffer: cash plus
         short-term investments minus total interest-bearing debt, scaled by
         assets. Market-neutral cross-sectional book.
idea:    Liquid assets above interest-bearing debt reduce refinancing downside
         and create balance-sheet optionality. A deep net cash buffer is a
         defensive state that protects large caps through systemic shocks like
         the 2022 drawdown, and this signal uses only balance-sheet data with
         no price component.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        cash = self.data.fun_bs_cash_and_cash_equivalents_quarterly_panel
        st_invest = self.data.fun_bs_short_term_investments_quarterly_panel
        short_loans = self.data.fun_bs_short_term_loans_quarterly_panel
        long_loans = self.data.fun_bs_long_term_loans_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel

        liquid = cash + st_invest
        total_debt = short_loans + long_loans
        net_liquid_buffer = self.feat.safe_divide_panel(liquid - total_debt, total_assets)

        input_sum = cash + st_invest + short_loans + long_loans + total_assets
        eligible = (input_sum == input_sum) & (total_assets > 0)

        buffer_score = self.op.zscore_cs_panel(net_liquid_buffer, mask=eligible)

        weights = self.op.portfolio_weights_panel(buffer_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)