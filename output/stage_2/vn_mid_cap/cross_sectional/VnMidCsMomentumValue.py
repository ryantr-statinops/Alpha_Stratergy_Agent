"""
name:    VnMidCsMomentumValue
summary: Buy mid caps combining improving earnings yield with a healthy
         uptrend. Three-vote composite: value improvement vs. own baseline,
         price trend vs. own EMA, and earnings-yield level. Retrofitted from
         success_alpha vote-basis.
idea:    H02 + H14 - Earnings yield with EMA trend squared. ValueTrendP02
         PASS Sharpe 2.31-2.67, EarningsYieldTrend PASS Sharpe 2.18.
         Success_alpha lesson: measure improvement vs. own history and vote
         the trend instead of ranking absolute composite level.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel

        earnings_yield = self.feat.safe_divide_panel(eps, close)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (eps > 0) & (close > 0) & (volume > 0)
            & (equity > 0) & (total_assets > 0) & (capital_strength > 0.15)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        ey_baseline = self.feat.rolling_mean_panel(earnings_yield)
        ey_improve = earnings_yield - ey_baseline
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        ey_improve_rank = self.op.rank_cs_panel(ey_improve, mask=eligible)
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        ey_level_rank = self.op.rank_cs_panel(earnings_yield, mask=eligible)
        signal = ey_improve_rank + trend_rank + ey_level_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)