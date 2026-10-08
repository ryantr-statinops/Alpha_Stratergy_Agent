"""
name:    VnMidCsAssetLightCash
summary: Buy mid caps with high cash relative to tangible fixed assets while
         the uptrend holds. Asset-light cash vote plus trend vote. Covers
         pair G+I: cash buffer vs fixed-asset base.
idea:    G+I pair #77 - Cash vs fixed assets (asset-light). A high
         cash/tangible_fixed_assets ratio signals a flexible, asset-light
         business able to fund opportunities from its own cash. Precedent:
         VnSmallCsAssetLight direction.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        cash = self.data.fun_bs_cash_and_cash_equivalents_quarterly_panel
        fixed_assets = self.data.fun_bs_tangible_fixed_assets_quarterly_panel

        cash_cover = self.feat.safe_divide_panel(cash, fixed_assets)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (cash >= 0)
            & (fixed_assets > 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        asset_light_rank = self.op.rank_cs_panel(cash_cover, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = asset_light_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
