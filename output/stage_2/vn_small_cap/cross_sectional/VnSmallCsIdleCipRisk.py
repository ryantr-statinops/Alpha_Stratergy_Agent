"""
name:    VnSmallCsIdleCipRisk
summary: Idle-CIP rank tilt on the validated value-trend return engine.
idea:    Large construction-in-progress relative to assets traps capital in
         unproductive projects and signals execution risk. Favoring low CIP
         tilts the validated earnings-yield x trend core toward deployers.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        equity_q = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets_q = self.data.fun_bs_total_assets_quarterly_panel
        cip = self.data.fun_bs_construction_in_progress_quarterly_panel

        cip_burden = self.feat.safe_divide_panel(cip, total_assets_q)
        earnings_yield = self.feat.safe_divide_panel(eps, close)
        capital_strength = self.feat.safe_divide_panel(equity_q, total_assets_q)
        close_ema = self.feat.ema_panel(close)
        trend_ratio = self.feat.safe_divide_panel(close, close_ema)
        base_eligible = (
            (eps > 0) & (close > 0) & (volume > 0) & (equity_q > 0)
            & (total_assets_q > 0) & (close_ema > 0)
            & (capital_strength > 0.15)
            & ((cip >= 0) | (cip < 0))
            & ((cip_burden >= 0) | (cip_burden < 0))
        )
        gw_premium = self.data.fun_is_gross_written_premium_quarterly_panel
        claim_expense = self.data.fun_is_claim_and_maturity_payment_expenses_quarterly_panel
        unearned_reserve = self.data.fun_bs_unearned_premium_reserve_quarterly_panel
        st_loans_receiv = self.data.fun_bs_short_term_loans_receivables_quarterly_panel
        gov_bonds_recv = self.data.fun_bs_government_bonds_purchased_for_resale_receivable_quarterly_panel
        gov_bonds_pay = self.data.fun_bs_government_bonds_purchased_for_resale_payable_quarterly_panel

        is_financial = (
            (self.feat.safe_divide_panel(gw_premium, total_assets_q) > 0.03)
            | (self.feat.safe_divide_panel(claim_expense, total_assets_q) > 0.03)
            | (self.feat.safe_divide_panel(unearned_reserve, total_assets_q) > 0.05)
            | (self.feat.safe_divide_panel(st_loans_receiv, total_assets_q) > 0.03)
            | (self.feat.safe_divide_panel(gov_bonds_recv, total_assets_q) > 0.03)
            | (self.feat.safe_divide_panel(gov_bonds_pay, total_assets_q) > 0.03)
        )
        base_eligible = base_eligible & (~is_financial)
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        cip_rank = self.op.rank_cs_panel(cip_burden, mask=base_eligible)
        clean_tilt = 1.5 - cip_rank
        eligible = base_eligible & (liquidity_rank > 0.40)

        core = (
            earnings_yield * trend_ratio * trend_ratio * trend_ratio
            * trend_ratio * trend_ratio * trend_ratio * trend_ratio
            * trend_ratio * trend_ratio * trend_ratio * trend_ratio
        )
        signal = core * clean_tilt
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
