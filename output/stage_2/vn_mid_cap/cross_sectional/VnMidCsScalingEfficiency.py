"""
name:    VnMidCsScalingEfficiency
summary: Scaling-efficiency tilt on a validated MID value-trend return engine.
idea:    Profit growth net of asset growth is a bounded rank tilt, not
         independent PnL; positive EPS and trend supply the return engine.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual_panel
        assets = self.data.fun_bs_total_assets_annual_panel

        profit_change = self.feat.delta_panel(net_profit)
        asset_change = self.feat.delta_panel(assets)
        scaled_profit_change = self.feat.safe_divide_panel(profit_change, assets)
        scaled_asset_change = self.feat.safe_divide_panel(asset_change, assets)
        profit_news = self.feat.rolling_sum_panel(scaled_profit_change)
        asset_news = self.feat.rolling_sum_panel(scaled_asset_change)
        efficiency = profit_news - asset_news
        earnings_yield = self.feat.safe_divide_panel(eps, close)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        close_ema = self.feat.ema_panel(close)
        trend_ratio = self.feat.safe_divide_panel(close, close_ema)
        base_eligible = (
            (eps > 0) & (close > 0) & (volume > 0) & (equity > 0)
            & (total_assets > 0) & (close_ema > 0) & (capital_strength > 0.15)
            & (assets > 0)
            & ((net_profit >= 0) | (net_profit < 0))
            & ((profit_news >= 0) | (profit_news < 0))
            & ((asset_news >= 0) | (asset_news < 0))
            & ((efficiency >= 0) | (efficiency < 0))
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        factor_rank = self.op.rank_cs_panel(efficiency, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.30)

        core = earnings_yield * trend_ratio * trend_ratio
        tilt = 0.9 + factor_rank * 0.2
        signal = core * tilt
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
