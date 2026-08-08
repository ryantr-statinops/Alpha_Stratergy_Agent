"""
name:    VnMidCsTaxDebtShield
summary: Buy mid caps with a strong debt tax shield while the uptrend holds.
         Tax-vs-financial-expense vote plus trend vote. Covers pair E+O:
         interest expense tax shield.
idea:    E+O pair #64 - Tax shield on debt. High financial_expenses/tax_current
         means a larger interest tax shield; debt financing offsets a bigger
         share of the tax bill. Anchors the E x O interaction. VnMidCsAssetDebtBearing
         keeps the leverage side in check.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        tax_current = self.data.fun_is_business_income_tax_current_quarterly_panel
        financial_expenses = self.data.fun_is_financial_expenses_quarterly_panel

        shield = self.feat.safe_divide_panel(financial_expenses, tax_current)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (tax_current > 0)
            & (financial_expenses >= 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        shield_rank = self.op.rank_cs_panel(shield, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = shield_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
