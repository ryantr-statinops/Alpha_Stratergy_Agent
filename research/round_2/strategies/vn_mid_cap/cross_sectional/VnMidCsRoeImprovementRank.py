"""
name:    VnMidCsRoeImprovementRank
summary: Buy mid caps whose ROE keeps improving relative to its own rolling
         baseline while the uptrend holds. ROE momentum vote plus trend vote.
         Retrofitted from success_alpha vote-basis.
idea:    H15 - Firms with improving ROE signal operational turnaround.
         RoeImprovement PASS Sharpe 2.10. Success_alpha lesson: improvement
         vs. own history combined with an uptrend vote.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel

        roe = self.feat.safe_divide_panel(net_profit, equity)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (equity > 0)
            & (total_assets > 0) & (capital_strength > 0.15)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        roe_baseline = self.feat.rolling_mean_panel(roe)
        roe_improve = roe - roe_baseline
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        improve_rank = self.op.rank_cs_panel(roe_improve, mask=eligible)
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = improve_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)