"""
name:    VnMidCsAssetDebtBearingV2
summary: Long mid-cap stocks with low long-term debt relative to fixed assets,
         only while the name trades above its EMA (long-bias trend gate). Flat
         when no eligible name is above trend. v2: trend as eligibility gate.
idea:    I+O pair #98 (v2) - Low long_term_liabilities/tangible_fixed_assets
         means the asset base is equity-funded, not debt-funded. v1 failed OOS
         under a forced short leg; v2 keeps only trend-up names and goes flat
         (cash) on a trend break.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        long_term_liabilities = self.data.fun_bs_long_term_liabilities_quarterly_panel
        fixed_assets = self.data.fun_bs_tangible_fixed_assets_quarterly_panel

        debt_ratio = self.feat.safe_divide_panel(long_term_liabilities, fixed_assets)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (long_term_liabilities >= 0)
            & (fixed_assets > 0) & (trend > 1.0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        debt_rank = self.op.rank_cs_panel(-debt_ratio, mask=eligible)
        weights = self.op.portfolio_weights_panel(debt_rank, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)