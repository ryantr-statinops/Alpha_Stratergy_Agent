"""
name:    VnMidCsAntiLotteryMaxReturn
summary: Anti-lottery tilt on a validated MID value-trend return engine.
idea:    Negative maximum daily return is a bounded rank tilt, not independent
         PnL; positive EPS and trend supply the validated return engine.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        shares = self.data.fun_bs_common_shares_quarterly_panel

        daily_return = self.feat.returns_panel(close)
        max_return = self.feat.rolling_max_panel(daily_return)
        anti_lottery = 0 - max_return
        earnings_yield = self.feat.safe_divide_panel(eps, close)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        close_ema = self.feat.ema_panel(close)
        trend_ratio = self.feat.safe_divide_panel(close, close_ema)
        base_eligible = (
            (eps > 0) & (close > 0) & (volume > 0) & (equity > 0)
            & (total_assets > 0) & (close_ema > 0) & (capital_strength > 0.15)
            & (shares > 0)
            & ((max_return >= 0) | (max_return < 0))
            & ((anti_lottery >= 0) | (anti_lottery < 0))
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        factor_rank = self.op.rank_cs_panel(anti_lottery, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.30)

        core = earnings_yield * trend_ratio * trend_ratio
        tilt = 0.98 + factor_rank * 0.04
        signal = core * tilt
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
