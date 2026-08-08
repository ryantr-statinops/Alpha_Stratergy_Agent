"""
name:    VnMidCsEffectiveTaxStability
summary: Buy mid caps with a stable effective tax rate while the uptrend
         holds. Low tax-rate volatility vote plus trend vote. Covers pair
         C+E: stable tax signals real earnings, cost discipline confirms.
idea:    C+E pair #31 - Cost discipline vs tax burden. Erratic tax ratios flag
         profit management; stable effective tax rate (tax_current/pre_tax)
         indicates sustainable earnings. Precedent: VnSmallCsTaxStability.
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
        tax_stability = self.feat.rolling_std_panel(tax_rate)
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

        stability_rank = self.op.rank_cs_panel(-tax_stability, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = stability_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
