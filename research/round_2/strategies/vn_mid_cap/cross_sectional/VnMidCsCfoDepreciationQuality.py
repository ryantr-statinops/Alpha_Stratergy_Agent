"""
name:    VnMidCsCfoDepreciationQuality
summary: Buy mid caps with low depreciation relative to operating cash flow
         while the uptrend holds. Depreciation-burden vote plus trend vote.
         Covers pair I+M: fixed-asset burden vs cash generation.
idea:    I+M pair #96 - Depreciation in CFO. Low
         depreciation/operating_cash_flow means cash earnings are not eaten
         by replacement capex needs; CFO quality is high. Precedent:
         VnSmallCs CFO-quality direction.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        depreciation = self.data.fun_cf_depreciation_and_amortisation_quarterly_panel
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_quarterly_panel

        dep_burden = self.feat.safe_divide_panel(depreciation, operating_cash_flow)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (depreciation >= 0)
            & (operating_cash_flow > 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        quality_rank = self.op.rank_cs_panel(-dep_burden, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = quality_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
