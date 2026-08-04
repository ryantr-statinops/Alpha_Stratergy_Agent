"""
name:    VnMidCsEnterpriseEarningsYieldRobust
summary: Filtered, concentrated enterprise-yield value-trend challenger.
idea:    Enterprise yield tilts the validated MID value-trend engine while
         volatility, price-impact, and signal-tail controls target better OOS
         stability and a smaller stock book.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        high = self.data.pv_high_panel
        low = self.data.pv_low_panel
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
        natr = self.feat.natr_panel(high, low, close)
        illiquidity = self.feat.amihud_illiquidity_panel(close, volume)

        base_eligible = (
            (high > 0) & (low > 0) & (close > 0) & (volume > 0) & (eps > 0)
            & (net_profit > 0) & (shares > 0) & (short_debt >= 0)
            & (long_debt >= 0) & (cash >= 0) & (enterprise_value > 0)
            & (equity > 0) & (total_assets > 0) & (close_ema > 0)
            & (capital_strength > 0.15)
            & ((enterprise_yield >= 0) | (enterprise_yield < 0))
            & ((natr >= 0) | (natr < 0))
            & ((illiquidity >= 0) | (illiquidity < 0))
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        volatility_rank = self.op.rank_cs_panel(natr, mask=base_eligible)
        illiquidity_rank = self.op.rank_cs_panel(illiquidity, mask=base_eligible)
        robust_eligible = (
            base_eligible & (liquidity_rank > 0.30)
            & (volatility_rank < 0.95) & (illiquidity_rank < 0.95)
        )

        enterprise_rank = self.op.rank_cs_panel(enterprise_yield, mask=robust_eligible)
        core = earnings_yield * trend_ratio * trend_ratio
        raw_signal = core * (0.9 + enterprise_rank * 0.2)
        signal = raw_signal

        weights = self.op.portfolio_weights_panel(
            signal, method='demean_l1', mask=robust_eligible
        )
        self.set_portfolio_positions(weights)
