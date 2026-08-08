"""
name:    VnMidCsWcInvestmentLeakV2
summary: Long mid caps with low investment-outflow relative to working capital,
         only while the name trades above its EMA (long-bias trend gate). Flat
         when no eligible name is above trend. v2: trend as eligibility gate.
idea:    H+N pair #90 (v2) - Low investments_in_other_entities/working_capital
         keeps capital from leaking out of the core. v1 failed OOS under a
         forced short leg; v2 restricts to trend-up names and goes flat (cash)
         once the trend breaks.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        investments = self.data.fun_cf_investments_in_other_entities_quarterly_panel
        receivables = self.data.fun_bs_accounts_receivable_quarterly_panel
        inventories = self.data.fun_bs_inventories_quarterly_panel
        payables = self.data.fun_bs_trade_accounts_payable_quarterly_panel

        working_capital = receivables + inventories - payables
        outflow = 0 - investments
        leak_ratio = self.feat.safe_divide_panel(outflow, working_capital)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (investments <= 0)
            & (working_capital > 0) & (trend > 1.0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        leak_rank = self.op.rank_cs_panel(-leak_ratio, mask=eligible)
        weights = self.op.portfolio_weights_panel(leak_rank, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)