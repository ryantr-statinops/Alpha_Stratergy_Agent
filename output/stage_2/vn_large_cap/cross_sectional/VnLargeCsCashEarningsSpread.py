"""
name:    VnLargeCsCashEarningsSpread
summary: Allocate across large caps by the cash-minus-accounting earnings spread
         scaled by assets, cross-sectionally z-scored and market-neutral.
idea:    Cash earnings are more durable than accrual earnings; a wide positive
         spread between operating cash flow and net profit shows that reported
         profit has actually been converted into cash. Scaling both by assets
         makes the spread comparable across large caps of different sizes, and
         the market-neutral book goes long the highest-conversion names.
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

        spread_score = self.op.zscore_cs_panel(cash_earnings_spread, mask=eligible)

        weights = self.op.portfolio_weights_panel(spread_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
