"""
name:    VnSmallCsRelatedPartyRisk
summary: Related-party-receivable rank tilt on the validated value-trend engine.
idea:    High other/intercompany receivables relative to assets signal related-
         party or tunneling risk common in VN small caps. Avoiding such names
         tilts the validated earnings-yield x trend core toward cleaner books.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        equity_q = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets_q = self.data.fun_bs_total_assets_quarterly_panel
        other_receiv = self.data.fun_bs_other_receivables_quarterly_panel
        intercompany = self.data.fun_bs_intercompany_receivables_quarterly_panel

        related_party = self.feat.safe_divide_panel(other_receiv + intercompany, total_assets_q)
        earnings_yield = self.feat.safe_divide_panel(eps, close)
        capital_strength = self.feat.safe_divide_panel(equity_q, total_assets_q)
        close_ema = self.feat.ema_panel(close)
        trend_ratio = self.feat.safe_divide_panel(close, close_ema)
        base_eligible = (
            (eps > 0) & (close > 0) & (volume > 0) & (equity_q > 0)
            & (total_assets_q > 0) & (close_ema > 0)
            & (capital_strength > 0.15)
            & ((other_receiv >= 0) | (other_receiv < 0))
            & ((intercompany >= 0) | (intercompany < 0))
            & ((related_party >= 0) | (related_party < 0))
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
        related_rank = self.op.rank_cs_panel(related_party, mask=base_eligible)
        clean_tilt = 1.5 - related_rank
        eligible = base_eligible & (liquidity_rank > 0.40)

        core = (
            earnings_yield * trend_ratio * trend_ratio * trend_ratio
            * trend_ratio * trend_ratio * trend_ratio * trend_ratio
            * trend_ratio * trend_ratio * trend_ratio * trend_ratio
        )
        signal = core * clean_tilt
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
