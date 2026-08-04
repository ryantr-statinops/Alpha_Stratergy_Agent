"""
name:    VnLargeCsCashEarningsMagnitude
summary: Allocate across large caps by winsorized cash-minus-accounting earnings
         spread with magnitude-sensitive market-neutral weights.
idea:    The cash earnings spread is scaled into portfolio weights so that large
         caps whose cash conversion most exceeds reported profit get proportionally
         more exposure. Winsorizing the spread first keeps a few working-capital
         outliers from driving the book, letting the magnitude reflect the
         durable conversion advantage across the large-cap cross-section.
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

        weights = self.op.portfolio_weights_panel(spread_score, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)