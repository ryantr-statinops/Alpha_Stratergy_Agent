"""
name:    VnLargeCsStableCashProfitability
summary: Allocate across large caps by stable, positively smoothed cash
         profitability, cross-sectionally z-scored and market-neutral.
idea:    Cash-flow volatility is associated with return risk and uncertainty;
         institutional ownership in large caps makes stability worth pricing
         over a single quarter of growth. Without a verified rolling standard
         deviation primitive, the EMA of annual operating cash flow over assets
         stands in for the persistent, stable level of cash profitability, so
         the book favors names whose cash ROA is durably high rather than
         volatile.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel

        cash_roa = self.feat.safe_divide_panel(operating_cash_flow, total_assets)
        stable_cash_roa = self.feat.ema_panel(cash_roa)

        eligible = (operating_cash_flow > 0) & (total_assets > 0)

        quality_score = self.op.zscore_cs_panel(stable_cash_roa, mask=eligible)

        weights = self.op.portfolio_weights_panel(quality_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
