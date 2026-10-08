"""
name:    VnMidCsSellingTaxTrend
summary: Buy mid caps whose selling cost per unit of profit is low and whose
         effective tax rate is falling, on a healthy uptrend. Selling
         efficiency level vote plus tax-rate-decline vote. Covers pair C+E:
         cost structure x tax trajectory.
idea:    C+E pair #31 - Cost discipline vs tax burden. Low selling cost per
         unit of profit signals operating efficiency; a declining effective
         tax rate frees more after-tax cash. Two orthogonal votes.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly_panel
        selling = self.data.fun_is_selling_expenses_quarterly_panel
        tax_current = self.data.fun_is_business_income_tax_current_quarterly_panel
        pre_tax = self.data.fun_is_net_accounting_profit_loss_before_tax_quarterly_panel

        selling_per_profit = self.feat.safe_divide_panel(selling, net_profit)
        tax_rate = self.feat.safe_divide_panel(tax_current, pre_tax)
        tax_rate_baseline = self.feat.rolling_mean_panel(tax_rate)
        tax_decline = tax_rate_baseline - tax_rate
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (pre_tax > 0)
            & (tax_current >= 0) & (net_profit > 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        selling_rank = self.op.rank_cs_panel(-selling_per_profit, mask=eligible)
        decline_rank = self.op.rank_cs_panel(tax_decline, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = selling_rank + decline_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
