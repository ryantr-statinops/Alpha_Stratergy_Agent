"""
name:    VnMidCsFinancialExpenseTax
summary: Buy mid caps with low financial expense burden and a plausible
         effective tax rate, on a healthy uptrend. Low interest-cost vote
         plus tax-rate-normality vote. Covers pair C+E: financing cost x tax.
idea:    C+E pair #31 - Cost discipline vs tax burden. Low financial expenses
         relative to assets indicates a light debt load; a normal effective
         tax rate confirms earnings quality. Two independent votes.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        fin_expenses = self.data.fun_is_financial_expenses_quarterly_panel
        tax_current = self.data.fun_is_business_income_tax_current_quarterly_panel
        pre_tax = self.data.fun_is_net_accounting_profit_loss_before_tax_quarterly_panel

        fin_burden = self.feat.safe_divide_panel(fin_expenses, total_assets)
        tax_rate = self.feat.safe_divide_panel(tax_current, pre_tax)
        tax_dev = tax_rate - 0.2
        tax_distance = tax_dev * tax_dev
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (pre_tax > 0)
            & (tax_current >= 0) & (fin_expenses >= 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        fin_rank = self.op.rank_cs_panel(-fin_burden, mask=eligible)
        norm_rank = self.op.rank_cs_panel(-tax_distance, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = fin_rank + norm_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
