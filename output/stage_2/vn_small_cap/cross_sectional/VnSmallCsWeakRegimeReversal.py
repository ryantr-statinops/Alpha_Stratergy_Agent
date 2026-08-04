"""
name:    VnSmallCsWeakRegimeReversal
summary: Short-term reversal tilt on the validated value-trend return engine.
idea:    Cross-sectional short-term reversal tilts the validated
         value-trend return engine; it does not claim independent PnL.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        equity_q = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets_q = self.data.fun_bs_total_assets_quarterly_panel

        close_ema = self.feat.ema_panel(close)
        earnings_yield = self.feat.safe_divide_panel(eps, close)
        capital_strength = self.feat.safe_divide_panel(equity_q, total_assets_q)
        trend_ratio = self.feat.safe_divide_panel(close, close_ema)
        reversal = 0 - self.feat.returns_panel(close)
        base_eligible = (
            (eps > 0) & (close > 0) & (volume > 0) & (equity_q > 0)
            & (total_assets_q > 0) & (close_ema > 0)
            & (capital_strength > 0.15)
            & ((reversal >= 0) | (reversal < 0))
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        reversal_rank = self.op.rank_cs_panel(reversal, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        core = (
            earnings_yield * trend_ratio * trend_ratio * trend_ratio
            * trend_ratio * trend_ratio * trend_ratio * trend_ratio
            * trend_ratio * trend_ratio * trend_ratio * trend_ratio
        )
        signal = core * (0.9 + reversal_rank * 0.2)
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
