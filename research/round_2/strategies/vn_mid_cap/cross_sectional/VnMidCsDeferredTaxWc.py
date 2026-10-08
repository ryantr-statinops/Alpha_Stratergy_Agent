"""
name:    VnMidCsDeferredTaxWc
summary: Buy mid caps with low deferred tax relative to working capital while
         the uptrend holds. Deferred-tax vote plus trend vote. Covers pair
         E+H: deferred tax vs working capital.
idea:    E+H pair #57 - Deferred tax vs WC. Low tax_deferred/working_capital
         means the firm does not rely on postponed tax as a cheap funding
         source; earnings quality is higher when tax timing is transparent.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        tax_deferred = self.data.fun_is_business_income_tax_deferred_quarterly_panel
        receivables = self.data.fun_bs_accounts_receivable_quarterly_panel
        inventories = self.data.fun_bs_inventories_quarterly_panel
        payables = self.data.fun_bs_trade_accounts_payable_quarterly_panel

        working_capital = receivables + inventories - payables
        tax_ratio = self.feat.safe_divide_panel(tax_deferred, working_capital)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (tax_deferred >= 0)
            & (working_capital > 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        deferral_rank = self.op.rank_cs_panel(-tax_ratio, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = deferral_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
