"""
name:    VnSmallCsFreeSupplierCredit
summary: Free-supplier-credit rank tilt on the validated value-trend engine.
idea:    Payables and customer advances financing inventories is free credit
         that reduces reliance on banks. Higher supplier/customer funding
         tilts the validated earnings-yield x trend core toward firms with
         low-cost working-capital financing.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        equity_q = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets_q = self.data.fun_bs_total_assets_quarterly_panel
        payables = self.data.fun_bs_trade_accounts_payable_quarterly_panel
        advances = self.data.fun_bs_advances_from_customers_quarterly_panel
        inventories = self.data.fun_bs_inventories_net_quarterly_panel

        supplier_credit = self.feat.safe_divide_panel(
            payables + advances, inventories
        )
        earnings_yield = self.feat.safe_divide_panel(eps, close)
        capital_strength = self.feat.safe_divide_panel(equity_q, total_assets_q)
        close_ema = self.feat.ema_panel(close)
        trend_ratio = self.feat.safe_divide_panel(close, close_ema)
        base_eligible = (
            (eps > 0) & (close > 0) & (volume > 0) & (equity_q > 0)
            & (total_assets_q > 0) & (close_ema > 0)
            & (capital_strength > 0.15) & (inventories > 0)
            & ((payables >= 0) | (payables < 0))
            & ((advances >= 0) | (advances < 0))
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
        credit_rank = self.op.rank_cs_panel(supplier_credit, mask=base_eligible)
        tilt = 0.9 + credit_rank * 0.2
        eligible = base_eligible & (liquidity_rank > 0.40)

        core = (
            earnings_yield * trend_ratio * trend_ratio * trend_ratio
            * trend_ratio * trend_ratio * trend_ratio * trend_ratio
            * trend_ratio * trend_ratio * trend_ratio * trend_ratio
        )
        signal = core * tilt
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
