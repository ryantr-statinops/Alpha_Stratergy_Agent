"""
name:    VnMidCsWorkingCapitalLean
summary: Buy mid caps with low working capital relative to fixed assets while
         the uptrend holds. Lean-net-WC vote plus trend vote. Covers pair
         H+I: working capital efficiency vs asset base.
idea:    H+I pair #85 - Total asset efficiency. Low
         (receivables+inventories-payables)/tangible_fixed_assets means lean
         working capital that is not starving asset efficiency. Minimal
         external WC funding, fewer hidden receivables/inventory risks.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        receivables = self.data.fun_bs_accounts_receivable_quarterly_panel
        inventories = self.data.fun_bs_inventories_quarterly_panel
        payables = self.data.fun_bs_trade_accounts_payable_quarterly_panel
        fixed_assets = self.data.fun_bs_tangible_fixed_assets_quarterly_panel

        working_capital = receivables + inventories - payables
        wc_intensity = self.feat.safe_divide_panel(working_capital, fixed_assets)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (working_capital >= 0)
            & (fixed_assets > 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        lean_rank = self.op.rank_cs_panel(-wc_intensity, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = lean_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
