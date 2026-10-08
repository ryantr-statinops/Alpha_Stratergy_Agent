"""
name:    VnMidCsSellingCostDiscipline
summary: Buy mid caps whose selling-expense burden falls relative to their own
         baseline while the uptrend holds. Cost-discipline improvement vote
         plus trend vote. Covers pair C+E (cost x tax): lean selling costs
         paired with stable tax rate is the tilt of the C1 composite core.
idea:    C+E pair #31 - Cost discipline vs tax burden. Lean (selling+GAE)
         relative to assets signals operating discipline; stable effective tax
         confirms real earnings. This variant scores selling-expense leverage
         improvement on top of the standard value-trend engine.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        selling = self.data.fun_is_selling_expenses_quarterly_panel
        tax_current = self.data.fun_is_business_income_tax_current_quarterly_panel
        pre_tax = self.data.fun_is_net_accounting_profit_loss_before_tax_quarterly_panel

        selling_burden = self.feat.safe_divide_panel(selling, total_assets)
        tax_rate = self.feat.safe_divide_panel(tax_current, pre_tax)
        tax_stability = self.feat.rolling_std_panel(tax_rate)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (pre_tax > 0)
            & (tax_current >= 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        lean_selling = -selling_burden
        selling_baseline = self.feat.rolling_mean_panel(lean_selling)
        selling_improve = lean_selling - selling_baseline
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        improve_rank = self.op.rank_cs_panel(selling_improve, mask=eligible)
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = improve_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
