"""
name:    VnMidCsCostEfficiencyTaxShield
summary: Buy mid caps whose net profit per unit of operating cost is rising
         and whose effective tax rate is stable, on a healthy uptrend. Cost
         efficiency improvement vote plus tax-stability vote. Covers pair
         C+E: cost leverage x tax quality.
idea:    C+E pair #31 - Cost discipline vs tax burden. Net profit produced per
         unit of (selling+GAE) cost measures efficiency directly; a stable tax
         rate confirms earnings are genuine. Two independent votes.
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
        admin = self.data.fun_is_general_and_admin_expenses_quarterly_panel
        tax_current = self.data.fun_is_business_income_tax_current_quarterly_panel
        pre_tax = self.data.fun_is_net_accounting_profit_loss_before_tax_quarterly_panel

        cost = selling + admin
        cost_efficiency = self.feat.safe_divide_panel(net_profit, cost)
        tax_rate = self.feat.safe_divide_panel(tax_current, pre_tax)
        tax_stability = self.feat.rolling_std_panel(tax_rate)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (pre_tax > 0)
            & (tax_current >= 0) & (cost > 0) & (net_profit > 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        eff_baseline = self.feat.rolling_mean_panel(cost_efficiency)
        eff_improve = cost_efficiency - eff_baseline
        improve_rank = self.op.rank_cs_panel(eff_improve, mask=eligible)
        stability_rank = self.op.rank_cs_panel(-tax_stability, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = improve_rank + stability_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
