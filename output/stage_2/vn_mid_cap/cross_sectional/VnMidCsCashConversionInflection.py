"""
name:    VnMidCsCashConversionInflection
summary: Allocate across mid caps by the year-over-year change in cash
         earnings spread (CFO - PAT over assets), gated so PAT is not
         collapsing. Market-neutral cross-sectional book.
idea:    When a firm's earnings stop being accrual and start converting into
         operating cash, that inflection is a quality signal distinct from
         earnings growth. Because daily-aligned fundamentals are forward-filled,
         a daily delta of the spread is a report-day impulse, so the inflection
         is measured as the cash-earnings spread above its own trailing average:
         a persistent state of improving cash realization. The PAT guard uses a
         tolerance band (loss not exceeding 2% of assets) instead of a strict
         positive-profit gate, keeping coverage across the cross-section.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel

        cash_earnings_spread = self.feat.safe_divide_panel(operating_cash_flow - net_profit, total_assets)
        spread_trend = self.feat.ema_panel(cash_earnings_spread)
        spread_inflection = cash_earnings_spread - spread_trend

        input_sum = operating_cash_flow + net_profit + total_assets
        eligible = (input_sum == input_sum) & (total_assets > 0) & (net_profit > -0.02 * total_assets)

        inflection_score = self.op.zscore_cs_panel(spread_inflection, mask=eligible)

        weights = self.op.portfolio_weights_panel(inflection_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)