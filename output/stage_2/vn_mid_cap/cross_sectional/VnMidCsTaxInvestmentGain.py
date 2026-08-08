"""
name:    VnMidCsTaxInvestmentGain
summary: Buy mid caps with low current tax relative to investment gains while
         the uptrend holds. Tax-vs-investing vote plus trend vote. Covers
         pair E+N: tax on investment gains.
idea:    E+N pair #63 - Tax on investment gains. Low tax_current/profit_from_investing
         means a small tax bill relative to investment income, a sign that
         realized gains are not creating a heavy tax drag. Anchors the E x N
         interaction without trading the asset base itself.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        tax_current = self.data.fun_is_business_income_tax_current_quarterly_panel
        investing_gain = self.data.fun_cf_profit_loss_from_investing_activities_quarterly_panel

        tax_ratio = self.feat.safe_divide_panel(tax_current, investing_gain)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (tax_current >= 0)
            & (investing_gain > 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        tax_rank = self.op.rank_cs_panel(-tax_ratio, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = tax_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
