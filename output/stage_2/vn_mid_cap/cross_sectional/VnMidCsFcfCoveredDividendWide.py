"""
name:    VnMidCsFcfCoveredDividendWide
summary: Allocate across mid caps by dividend yield gated by positive free cash
         flow, a coverage-widened variant. Market-neutral cross-sectional book.
idea:    A standalone dividend yield is often a value trap. This ablation widens
         coverage relative to the strict FCF-covers-dividend gate: a yield is
         eligible when trailing free cash flow (operating cash flow minus capex)
         is positive, instead of requiring it to exceed the full dividend. The
         looser band keeps more payers in the cross-section, which reduces
         report-date sparsity in the Test window.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        dividends = self.data.fun_cf_dividends_paid_annual_panel
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual_panel
        common_shares = self.data.fun_bs_common_shares_annual_panel
        close = self.data.pv_close_panel

        dividend_paid = 0 - dividends
        free_cash_flow = operating_cash_flow + capex
        market_value = close * common_shares
        dividend_yield = self.feat.safe_divide_panel(dividend_paid, market_value)

        input_sum = dividends + operating_cash_flow + capex + common_shares + close
        eligible = (input_sum == input_sum) & (dividends < 0) & (capex <= 0) & (common_shares > 0) & (close > 0) & (market_value > 0) & (free_cash_flow > 0)

        yield_score = self.op.zscore_cs_panel(dividend_yield, mask=eligible)

        weights = self.op.portfolio_weights_panel(yield_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)