"""
name:    VnSmallCsProductiveReinvestment
summary: Productive-reinvestment gate on the validated value-trend return engine.
idea:    The independent reinvestment factor acts as a gate on the validated
         value-trend return engine; it does not claim independent PnL. Positive
         CFO, nonpositive CAPEX, and positive assets remain required.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        equity_q = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets_q = self.data.fun_bs_total_assets_quarterly_panel
        cfo = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel

        capex_intensity = self.feat.safe_divide_panel(0 - capex, total_assets)
        earnings_yield = self.feat.safe_divide_panel(eps, close)
        capital_strength = self.feat.safe_divide_panel(equity_q, total_assets_q)
        close_ema = self.feat.ema_panel(close)
        trend_ratio = self.feat.safe_divide_panel(close, close_ema)
        base_eligible = (
            (eps > 0) & (close > 0) & (volume > 0) & (equity_q > 0)
            & (total_assets_q > 0) & (close_ema > 0)
            & (capital_strength > 0.15) & (cfo > 0) & (capex <= 0)
            & (total_assets > 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40) & (capex_intensity > 0)

        core = (
            earnings_yield * trend_ratio * trend_ratio * trend_ratio
            * trend_ratio * trend_ratio * trend_ratio * trend_ratio
            * trend_ratio * trend_ratio * trend_ratio * trend_ratio
        )
        signal = core
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
