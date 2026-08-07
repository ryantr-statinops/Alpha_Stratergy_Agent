"""
name:    VnMidCsRoaQualityRank
summary: Buy mid caps with improving return on assets on top of a healthy
         uptrend. Two-vote signal: ROA above its own trailing baseline plus
         close above its own EMA. Retrofitted from success_alpha vote-basis:
         self-baseline improvement replaces absolute cross-sectional level,
         trend is a second independent vote, conviction drives weight.
idea:    H06 - Firms that generate more profit per unit of assets outperform.
         ROA captures asset efficiency directly. Tested on SMALL with Sharpe 1.84.
         Success_alpha lesson: measure improvement vs. own history (factor >
         sma(factor)) and combine with an uptrend vote instead of ranking the
         absolute level.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel

        roa = self.feat.safe_divide_panel(net_profit, total_assets)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (eps > 0) & (close > 0) & (volume > 0)
            & (total_assets > 0) & (equity > 0) & (capital_strength > 0.15)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        roa_baseline = self.feat.rolling_mean_panel(roa)
        roa_improve = roa - roa_baseline
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        improve_rank = self.op.rank_cs_panel(roa_improve, mask=eligible)
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = improve_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)