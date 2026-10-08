"""
name:    VnMidCsEnterpriseEarningsYield
summary: Enterprise-yield tilt on a MID value-trend return engine.
idea:    Enterprise-adjusted earnings yield supplies an independent bounded
         tilt while positive EPS and trend provide the return engine.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual_panel
        shares = self.data.fun_bs_common_shares_quarterly_panel
        short_debt = self.data.fun_bs_short_term_loans_quarterly_panel
        long_debt = self.data.fun_bs_long_term_loans_quarterly_panel
        cash = self.data.fun_bs_cash_and_cash_equivalents_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel

        market_value = close * shares
        enterprise_value = market_value + short_debt + long_debt - cash
        enterprise_yield = self.feat.safe_divide_panel(net_profit, enterprise_value)
        earnings_yield = self.feat.safe_divide_panel(eps, close)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        close_ema = self.feat.ema_panel(close)
        trend_ratio = self.feat.safe_divide_panel(close, close_ema)
        base_eligible = (
            (close > 0) & (volume > 0) & (eps > 0) & (net_profit > 0) & (shares > 0)
            & (short_debt >= 0) & (long_debt >= 0) & (cash >= 0)
            & (enterprise_value > 0) & (equity > 0) & (total_assets > 0)
            & (close_ema > 0) & (capital_strength > 0.15)
            & ((enterprise_yield >= 0) | (enterprise_yield < 0))
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        enterprise_rank = self.op.rank_cs_panel(enterprise_yield, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.30)

        core = earnings_yield * trend_ratio * trend_ratio
        signal = core * (0.9 + enterprise_rank * 0.2)
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
