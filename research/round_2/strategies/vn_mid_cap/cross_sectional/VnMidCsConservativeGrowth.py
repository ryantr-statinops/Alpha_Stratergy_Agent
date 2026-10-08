"""
name:    VnMidCsConservativeGrowth
summary: Buy mid caps whose asset growth turns conservative relative to their
         own baseline while the uptrend holds. Negative asset growth
         improvement vote plus trend vote. Retrofitted from success_alpha
         vote-basis.
idea:    H13 - Firms that grow assets conservatively outperform aggressive
         growers. ConservativeAssetGrowth PASS Sharpe 2.09. Success_alpha
         lesson: improvement vs. own history, not absolute level.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel

        asset_growth = self.feat.safe_divide_panel(self.feat.delta_panel(total_assets), total_assets)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        conservatism = -asset_growth
        conservatism_baseline = self.feat.rolling_mean_panel(conservatism)
        conservatism_improve = conservatism - conservatism_baseline
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        improve_rank = self.op.rank_cs_panel(conservatism_improve, mask=eligible)
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = improve_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)