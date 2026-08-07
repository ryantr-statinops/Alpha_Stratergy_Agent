"""
name:    VnMidCsCurrentLiquidityRank
summary: Buy mid caps whose current ratio improves against their own baseline
         while the uptrend holds. Current ratio improvement vote plus trend
         vote. Retrofitted from success_alpha vote-basis.
idea:    H20 - Liquid firms are less likely to face distress. CurrentLiquidity
         PASS Sharpe 1.81. Success_alpha lesson: improvement vs. own history,
         not absolute level.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        current_assets = self.data.fun_bs_current_assets_quarterly_panel
        current_liabilities = self.data.fun_bs_current_liabilities_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel

        current_ratio = self.feat.safe_divide_panel(current_assets, current_liabilities)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (current_liabilities > 0) & (equity > 0) & (current_assets > 0)
            & (capital_strength > 0.15)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        ratio_baseline = self.feat.rolling_mean_panel(current_ratio)
        ratio_improve = current_ratio - ratio_baseline
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        improve_rank = self.op.rank_cs_panel(ratio_improve, mask=eligible)
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = improve_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)