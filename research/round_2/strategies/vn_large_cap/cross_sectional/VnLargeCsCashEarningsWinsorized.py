"""
name:    VnLargeCsCashEarningsWinsorized
summary: Allocate across large caps by winsorized cash-minus-accounting earnings
         spread, cross-sectionally rank-demeaned and market-neutral.
idea:    The cash earnings spread is noisy because a small group of large caps
         reports extreme working-capital swings. Winsorizing the spread to the
         2–98 percentiles before z-scoring keeps the durable conversion effect
         while isolating the book from working-capital outliers that reverse.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel

        cash_roa = self.feat.safe_divide_panel(operating_cash_flow, total_assets)
        profit_roa = self.feat.safe_divide_panel(net_profit, total_assets)
        cash_earnings_spread = cash_roa - profit_roa

        eligible = (operating_cash_flow > 0) & (net_profit > 0) & (total_assets > 0)

        clean = self.op.winsorize_cs_panel(cash_earnings_spread, mask=eligible, lower=0.02, upper=0.98)
        spread_score = self.op.zscore_cs_panel(clean, mask=eligible)

        weights = self.op.portfolio_weights_panel(spread_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)