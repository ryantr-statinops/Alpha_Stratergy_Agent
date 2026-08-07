"""
name:    VnMidCsLowLeverageRank
summary: Buy mid caps whose leverage falls relative to their own baseline
         while the uptrend holds. Low leverage improvement vote plus trend
         vote. Retrofitted from success_alpha vote-basis.
idea:    H17 - Conservatively financed firms outperform. LowLeverage PASS
         Sharpe 1.64. Success_alpha lesson: measure improvement vs. own
         history and combine with an uptrend vote.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        liabilities = self.data.fun_bs_liabilities_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel

        leverage = self.feat.safe_divide_panel(liabilities, total_assets)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0) & (equity > 0)
            & (capital_strength > 0.15)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        low_leverage = -leverage
        leverage_baseline = self.feat.rolling_mean_panel(low_leverage)
        leverage_improve = low_leverage - leverage_baseline
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        improve_rank = self.op.rank_cs_panel(leverage_improve, mask=eligible)
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = improve_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)