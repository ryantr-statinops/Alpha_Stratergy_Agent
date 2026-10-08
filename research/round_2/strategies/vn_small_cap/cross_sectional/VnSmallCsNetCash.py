"""
name:    VnSmallCsNetCash
summary: Net-cash rank tilt on the validated value-trend return engine.
idea:    The independent net-cash factor tilts the validated
         value-trend return engine; it does not claim independent PnL.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        equity_q = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets_q = self.data.fun_bs_total_assets_quarterly_panel
        cash = self.data.fun_bs_cash_and_cash_equivalents_annual_panel
        short_debt = self.data.fun_bs_short_term_loans_annual_panel
        long_debt = self.data.fun_bs_long_term_loans_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel

        net_cash = cash - short_debt - long_debt
        net_cash_ratio = self.feat.safe_divide_panel(net_cash, total_assets)
        earnings_yield = self.feat.safe_divide_panel(eps, close)
        capital_strength = self.feat.safe_divide_panel(equity_q, total_assets_q)
        close_ema = self.feat.ema_panel(close)
        trend_ratio = self.feat.safe_divide_panel(close, close_ema)
        base_eligible = (
            (eps > 0) & (close > 0) & (volume > 0) & (equity_q > 0)
            & (total_assets_q > 0) & (close_ema > 0)
            & (capital_strength > 0.15) & (cash >= 0) & (short_debt >= 0)
            & (long_debt >= 0) & (total_assets > 0)
            & ((net_cash_ratio >= 0) | (net_cash_ratio < 0))
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        net_cash_rank = self.op.rank_cs_panel(net_cash_ratio, mask=base_eligible)
        tilt = 0.5 + net_cash_rank
        eligible = base_eligible & (liquidity_rank > 0.40)

        core = (
            earnings_yield * trend_ratio * trend_ratio * trend_ratio
            * trend_ratio * trend_ratio * trend_ratio * trend_ratio
            * trend_ratio * trend_ratio * trend_ratio * trend_ratio
        )
        signal = core * tilt
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
