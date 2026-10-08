"""
name:    VnMidCsNetCashRank
summary: Buy mid caps whose net cash position strengthens relative to their
         own baseline while the uptrend holds. Cash/Assets improvement vote
         plus trend vote. Retrofitted from success_alpha vote-basis.
idea:    H18 - Firms with net cash (low net debt) outperform. NetCash PASS
         Sharpe 1.90. Success_alpha lesson: improvement vs. own history, not
         absolute level.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        cash = self.data.fun_bs_cash_and_cash_equivalents_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel

        cash_ratio = self.feat.safe_divide_panel(cash, total_assets)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (cash > 0) & (capital_strength > 0.15)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        cash_baseline = self.feat.rolling_mean_panel(cash_ratio)
        cash_improve = cash_ratio - cash_baseline
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        improve_rank = self.op.rank_cs_panel(cash_improve, mask=eligible)
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = improve_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)