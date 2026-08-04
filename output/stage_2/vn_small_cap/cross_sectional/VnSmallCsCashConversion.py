"""
name:    VnSmallCsCashConversion
summary: Cash-conversion rank tilt on the validated value-trend return engine.
idea:    The independent cash-conversion factor tilts the validated
         value-trend return engine; it does not claim independent PnL.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        equity_q = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets_q = self.data.fun_bs_total_assets_quarterly_panel
        cfo = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual_panel

        conversion = self.feat.safe_divide_panel(cfo, net_profit)
        earnings_yield = self.feat.safe_divide_panel(eps, close)
        capital_strength = self.feat.safe_divide_panel(equity_q, total_assets_q)
        close_ema = self.feat.ema_panel(close)
        trend_ratio = self.feat.safe_divide_panel(close, close_ema)
        base_eligible = (
            (eps > 0) & (close > 0) & (volume > 0) & (equity_q > 0)
            & (total_assets_q > 0) & (close_ema > 0)
            & (capital_strength > 0.15) & (net_profit > 0)
            & ((cfo >= 0) | (cfo < 0))
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        conversion_rank = self.op.rank_cs_panel(conversion, mask=base_eligible)
        tilt = 0.9 + conversion_rank * 0.2
        eligible = base_eligible & (liquidity_rank > 0.40)

        core = (
            earnings_yield * trend_ratio * trend_ratio * trend_ratio
            * trend_ratio * trend_ratio * trend_ratio * trend_ratio
            * trend_ratio * trend_ratio * trend_ratio * trend_ratio
        )
        signal = core * tilt
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
