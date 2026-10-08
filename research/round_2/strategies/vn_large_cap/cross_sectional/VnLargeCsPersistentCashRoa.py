"""
name:    VnLargeCsPersistentCashRoa
summary: Allocate across large caps by persistent positive cash ROA,
         cross-sectionally z-scored and market-neutral.
idea:    Cash-based profitability strips out accruals that can reverse, but a
         large cap should only be rewarded when positive cash profitability
         persists rather than coming from a one-year working-capital release.
         An EMA of annual operating cash flow over total assets captures the
         persistent level; the cross-section then goes long cash-profitable
         names and short the rest on the same quality dimension.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel

        cash_roa = self.feat.safe_divide_panel(operating_cash_flow, total_assets)
        persistent_cash_roa = self.feat.ema_panel(cash_roa)

        eligible = (operating_cash_flow > 0) & (total_assets > 0)

        quality_score = self.op.zscore_cs_panel(persistent_cash_roa, mask=eligible)

        weights = self.op.portfolio_weights_panel(quality_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
