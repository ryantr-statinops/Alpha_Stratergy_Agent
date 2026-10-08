"""
name:    VnMidCsValueQualityComposite
summary: Buy mid caps combining improving ROE with cheap valuation and a
         healthy uptrend. Three-vote composite: ROE improvement vs. own
         baseline, earnings-yield level, and price trend vs. own EMA.
         Retrofitted from success_alpha vote-basis.
idea:    Combine H02 (Earnings Yield) and H07 (ROE). EarningsYieldTrend PASS
         Sharpe 2.18, RoeQuality PASS Sharpe 2.30 on SMALL. Success_alpha
         lesson: measure improvement vs. own history and vote the trend
         instead of ranking absolute composite level.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel

        earnings_yield = self.feat.safe_divide_panel(eps, close)
        roe = self.feat.safe_divide_panel(net_profit, equity)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (eps > 0) & (close > 0) & (volume > 0)
            & (equity > 0) & (total_assets > 0) & (capital_strength > 0.15)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        roe_baseline = self.feat.rolling_mean_panel(roe)
        roe_improve = roe - roe_baseline
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        roe_improve_rank = self.op.rank_cs_panel(roe_improve, mask=eligible)
        value_rank = self.op.rank_cs_panel(earnings_yield, mask=eligible)
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = roe_improve_rank + value_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)