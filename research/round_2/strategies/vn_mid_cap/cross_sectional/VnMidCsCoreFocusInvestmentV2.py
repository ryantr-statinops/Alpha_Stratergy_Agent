"""
name:    VnMidCsCoreFocusInvestmentV2
summary: Long mid caps with low non-core investment relative to capex, only
         while the name trades above its EMA (long-bias trend gate). Flat when
         no eligible name is above trend. v2: trend as eligibility gate (not a
         rank vote) so the book goes flat in downtrends.
idea:    J+N pair #103 (v2) - Low investments_in_other_entities/capex flags a
         firm concentrating capital on the core fixed-asset base. v1 failed
         OOS with a forced short leg (demean_l1); v2 restricts to trend-up
         names only, letting the book go flat (cash) when the trend breaks.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        investments = self.data.fun_cf_investments_in_other_entities_quarterly_panel
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_quarterly_panel

        invest_outflow = 0 - investments
        capex_outflow = 0 - capex
        focus_ratio = self.feat.safe_divide_panel(invest_outflow, capex_outflow)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (investments <= 0)
            & (capex < 0) & (trend > 1.0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        focus_rank = self.op.rank_cs_panel(-focus_ratio, mask=eligible)
        weights = self.op.portfolio_weights_panel(focus_rank, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)