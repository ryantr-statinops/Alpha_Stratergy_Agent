"""
name:    VnMidCsTaxRateLevel
summary: Buy mid caps whose effective tax rate sits near the statutory norm
         while the uptrend holds. Tax-rate-level vote (close to ~20%) plus
         trend vote. Covers pair C+E: a normal tax rate confirms real,
         reportable earnings; cost discipline reinforces quality.
idea:    C+E pair #31 - Cost discipline vs tax burden. Firms with a plausible
         effective tax rate (near 20%) are more likely reporting genuine
         profit; extreme rates flag tax planning or profit management.
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
        pre_tax = self.data.fun_is_net_accounting_profit_loss_before_tax_quarterly_panel

        tax_rate = self.feat.safe_divide_panel(tax_current, pre_tax)
        tax_dev = tax_rate - 0.2
        tax_distance = tax_dev * tax_dev
        cost_burden = self.feat.safe_divide_panel(selling + admin, total_assets)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (pre_tax > 0)
            & (tax_current >= 0) & (cost_burden >= 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        norm_rank = self.op.rank_cs_panel(-tax_distance, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = norm_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
