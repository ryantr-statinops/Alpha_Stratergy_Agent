"""
name:    VnMidCsDeferredTaxQuality
summary: Buy mid caps with low deferred-tax accruals relative to current tax
         while the uptrend holds. Deferred-tax quality vote plus trend vote.
         Covers pair C+E: little deferred tax means reported earnings are not
         pushed forward; lean cost base confirms operating quality.
idea:    C+E pair #31 - Cost discipline vs tax burden. High deferred tax
         relative to current tax can signal earnings managed across periods;
         low deferred tax = current profit is real. Scores that ratio.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        selling = self.data.fun_is_selling_expenses_quarterly_panel
        admin = self.data.fun_is_general_and_admin_expenses_quarterly_panel
        tax_current = self.data.fun_is_business_income_tax_current_quarterly_panel
        tax_deferred = self.data.fun_is_business_income_tax_deferred_quarterly_panel

        deferred_ratio = self.feat.safe_divide_panel(tax_deferred, tax_current)
        cost_burden = self.feat.safe_divide_panel(selling + admin, total_assets)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (tax_current > 0)
            & (cost_burden >= 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        deferred_rank = self.op.rank_cs_panel(-deferred_ratio, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = deferred_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
