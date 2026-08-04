"""
name:    VnSmallCsLeanWorkingCapital
summary: Lean-working-capital gate on the validated value-trend return engine.
idea:    The independent working-capital factor acts as a gate on the validated
         value-trend return engine; it does not claim independent PnL.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        equity_q = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets_q = self.data.fun_bs_total_assets_quarterly_panel
        receivables = self.data.fun_bs_trade_accounts_receivable_annual_panel
        inventories = self.data.fun_bs_inventories_net_annual_panel
        payables = self.data.fun_bs_trade_accounts_payable_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel

        operating_wc = receivables + inventories - payables
        wc_burden = self.feat.safe_divide_panel(operating_wc, total_assets)
        earnings_yield = self.feat.safe_divide_panel(eps, close)
        capital_strength = self.feat.safe_divide_panel(equity_q, total_assets_q)
        close_ema = self.feat.ema_panel(close)
        trend_ratio = self.feat.safe_divide_panel(close, close_ema)
        base_eligible = (
            (eps > 0) & (close > 0) & (volume > 0) & (equity_q > 0)
            & (total_assets_q > 0) & (close_ema > 0)
            & (capital_strength > 0.15) & (receivables >= 0) & (inventories >= 0)
            & (payables >= 0) & (total_assets > 0)
            & ((wc_burden >= 0) | (wc_burden < 0))
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40) & (wc_burden < 0.30)

        core = (
            earnings_yield * trend_ratio * trend_ratio * trend_ratio
            * trend_ratio * trend_ratio * trend_ratio * trend_ratio
            * trend_ratio * trend_ratio * trend_ratio * trend_ratio
        )
        signal = core
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
