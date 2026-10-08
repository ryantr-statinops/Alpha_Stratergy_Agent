"""
name:    VnMidCsInternallyFundedInvestment
summary: Internal-funding tilt on a validated MID value-trend return engine.
idea:    Internal funding is a bounded rank tilt, not independent PnL. CAPEX is
         assumed non-positive; positive EPS and trend supply the return engine.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        cfo = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual_panel
        borrowing_proceeds = self.data.fun_cf_proceeds_from_borrowings_annual_panel
        share_issuance = self.data.fun_cf_proceeds_from_issue_of_shares_annual_panel
        assets = self.data.fun_bs_total_assets_annual_panel

        internal_gap = self.feat.safe_divide_panel(
            cfo + capex - borrowing_proceeds - share_issuance, assets
        )
        earnings_yield = self.feat.safe_divide_panel(eps, close)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        close_ema = self.feat.ema_panel(close)
        trend_ratio = self.feat.safe_divide_panel(close, close_ema)
        base_eligible = (
            (eps > 0) & (close > 0) & (volume > 0) & (equity > 0)
            & (total_assets > 0) & (close_ema > 0) & (capital_strength > 0.15)
            & (assets > 0) & (capex <= 0)
            & (borrowing_proceeds >= 0) & (share_issuance >= 0)
            & ((cfo >= 0) | (cfo < 0))
            & ((internal_gap >= 0) | (internal_gap < 0))
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        factor_rank = self.op.rank_cs_panel(internal_gap, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.30)

        core = earnings_yield * trend_ratio * trend_ratio
        tilt = 0.9 + factor_rank * 0.2
        signal = core * tilt
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
