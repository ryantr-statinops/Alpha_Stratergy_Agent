"""
name:    VnLargeCsEvAdjustedCashYield
summary: Allocate across large caps by operating cash flow yield on
         enterprise value net of liquid assets, cross-sectionally market-neutral.
idea:    A high equity cash yield can simply reflect leverage. Enterprise value
         (market cap plus debt minus liquid assets) penalizes cash flow that
         must first serve debt holders, isolating a firm's cash value to all
         capital providers. Large caps with high cash yield on this net
         enterprise basis are the long candidates.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
        close = self.data.pv_close_panel
        common_shares = self.data.fun_bs_common_shares_quarterly_panel
        short_term_loans = self.data.fun_bs_short_term_loans_quarterly_panel
        long_term_loans = self.data.fun_bs_long_term_loans_quarterly_panel
        cash = self.data.fun_bs_cash_and_cash_equivalents_quarterly_panel
        short_term_investments = self.data.fun_bs_short_term_investments_quarterly_panel

        market_cap = close * common_shares
        debt = short_term_loans + long_term_loans
        liquid_assets = cash + short_term_investments
        enterprise_value = market_cap + debt - liquid_assets

        ev_cash_yield = self.feat.safe_divide_panel(operating_cash_flow, enterprise_value)

        eligible = (
            (operating_cash_flow > 0)
            & (common_shares > 0)
            & (enterprise_value > 0)
        )

        yield_score = self.op.zscore_cs_panel(ev_cash_yield, mask=eligible)

        weights = self.op.portfolio_weights_panel(yield_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
