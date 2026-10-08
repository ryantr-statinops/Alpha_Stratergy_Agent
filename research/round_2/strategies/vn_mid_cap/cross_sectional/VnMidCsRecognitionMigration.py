"""
name:    VnMidCsRecognitionMigration
summary: Recognition-migration tilt on a validated MID value-trend engine.
idea:    Improving liquidity and participation form a bounded rank tilt, not
         independent PnL; positive EPS and trend supply the return engine.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel

        amihud = self.feat.amihud_illiquidity_panel(close, volume)
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_improvement = 0 - self.feat.rolling_zscore_panel(amihud)
        participation = self.feat.rolling_zscore_panel(traded_value)
        recognition = liquidity_improvement + participation
        earnings_yield = self.feat.safe_divide_panel(eps, close)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        close_ema = self.feat.ema_panel(close)
        trend_ratio = self.feat.safe_divide_panel(close, close_ema)
        base_eligible = (
            (eps > 0) & (close > 0) & (volume > 0) & (equity > 0)
            & (total_assets > 0) & (close_ema > 0) & (capital_strength > 0.15)
            & ((amihud >= 0) | (amihud < 0))
            & ((traded_value >= 0) | (traded_value < 0))
            & ((liquidity_improvement >= 0) | (liquidity_improvement < 0))
            & ((participation >= 0) | (participation < 0))
            & ((recognition >= 0) | (recognition < 0))
        )
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        factor_rank = self.op.rank_cs_panel(recognition, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.30)

        core = earnings_yield * trend_ratio * trend_ratio
        tilt = 0.9 + factor_rank * 0.2
        signal = core * tilt
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
