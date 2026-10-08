"""
name:    VnSmallCsValueTrendP02
summary: Value-trend family with EMA trend exponent p=2.
idea:    Earnings yield is multiplied by the EMA trend ratio exactly twice,
         expressing increasingly strong trend conviction within the family.
         Capital-strength and liquidity gates constrain fragile small caps.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel

        earnings_yield = self.feat.safe_divide_panel(eps, close)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        trend_ratio = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        base_eligible = (
            (eps > 0) & (close > 0) & (volume > 0) & (equity > 0)
            & (total_assets > 0) & (capital_strength > 0.15)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        signal = earnings_yield * trend_ratio * trend_ratio

        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
