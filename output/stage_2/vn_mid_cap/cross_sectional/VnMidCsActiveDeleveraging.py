"""
name:    VnMidCsActiveDeleveraging
summary: Deleveraging tilt on a validated MID value-trend return engine.
idea:    Active debt reduction is a bounded rank tilt, not independent PnL;
         positive EPS and trend supply the validated return engine.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        short_debt = self.data.fun_bs_short_term_loans_annual_panel
        long_debt = self.data.fun_bs_long_term_loans_annual_panel
        assets = self.data.fun_bs_total_assets_annual_panel

        debt = short_debt + long_debt
        debt_change = self.feat.rolling_sum_panel(
            self.feat.safe_divide_panel(self.feat.delta_panel(debt), assets)
        )
        deleveraging = 0 - debt_change
        earnings_yield = self.feat.safe_divide_panel(eps, close)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        close_ema = self.feat.ema_panel(close)
        trend_ratio = self.feat.safe_divide_panel(close, close_ema)
        base_eligible = (
            (eps > 0) & (close > 0) & (volume > 0) & (equity > 0)
            & (total_assets > 0) & (close_ema > 0) & (capital_strength > 0.15)
            & (short_debt >= 0) & (long_debt >= 0) & (assets > 0)
            & ((debt_change >= 0) | (debt_change < 0))
            & ((deleveraging >= 0) | (deleveraging < 0))
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        factor_rank = self.op.rank_cs_panel(deleveraging, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.30)

        core = earnings_yield * trend_ratio * trend_ratio
        tilt = 0.9 + factor_rank * 0.2
        signal = core * tilt
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
