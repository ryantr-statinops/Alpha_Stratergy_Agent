"""
name:    VnMidCsCapexCommissioning
summary: Buy mid caps whose construction-in-progress converts into productive
         fixed assets while the uptrend holds. Pair I+N: commissioning quality.
idea:    I+N pair #97 - Commissioning. CIP declining with fixed assets rising
         signals projects are completing and becoming productive (activation)
         rather than idle capital stuck in construction. The signal combines
         negative CIP change with positive fixed-asset change, scaled by the
         existing asset base to remove size effects.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        fixed_assets = self.data.fun_bs_tangible_fixed_assets_quarterly_panel
        cip = self.data.fun_bs_construction_in_progress_quarterly_panel

        cip_change = self.feat.delta_panel(cip)
        fixed_change = self.feat.delta_panel(fixed_assets)
        commissioning = self.feat.safe_divide_panel(fixed_change - cip_change, fixed_assets)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (fixed_assets > 0)
            & (cip >= 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        factor_rank = self.op.rank_cs_panel(commissioning, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = factor_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
