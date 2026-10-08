"""
name:    VnMidCsAccrualQualityRank
summary: Buy mid caps whose cash conversion improves against their own
         baseline while the uptrend holds. CFO/Net Profit improvement vote
         plus trend vote. Retrofitted from success_alpha vote-basis.
idea:    H09 - Low accruals indicate earnings backed by cash, not accounting
         choices. LowAccruals PASS Sharpe 1.61 on SMALL. Success_alpha lesson:
         measure improvement vs. own history and combine with an uptrend vote.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly_panel
        cfo = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel

        accrual_quality = self.feat.safe_divide_panel(cfo, net_profit)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (net_profit > 0)
            & (total_assets > 0) & (equity > 0) & (capital_strength > 0.15)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        accrual_baseline = self.feat.rolling_mean_panel(accrual_quality)
        accrual_improve = accrual_quality - accrual_baseline
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        improve_rank = self.op.rank_cs_panel(accrual_improve, mask=eligible)
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = improve_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)